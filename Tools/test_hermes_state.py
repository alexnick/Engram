import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import hermes_state  # pyright: ignore[reportImplicitRelativeImport]


JOURNEY = {
    "nodes": [
        {
            "id": "learned-one",
            "kind": "skill",
            "state": "active",
            "createdBy": "agent",
        },
        {
            "id": "bundled-one",
            "kind": "skill",
            "state": "active",
            "createdBy": "bundle",
        },
        {
            "id": "old-one",
            "kind": "skill",
            "state": "archived",
            "createdBy": "agent",
        },
        {"id": "memory:0", "kind": "memory", "state": "active"},
    ]
}


def write_skill(root: Path, relative: str, name: str, body: str = "Body\n") -> Path:
    skill_dir = root / "skills" / relative
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Test skill.\n---\n\n{body}",
        encoding="utf-8",
    )
    return skill_dir


class JourneyTests(unittest.TestCase):
    def test_selects_only_active_agent_created_skills(self) -> None:
        self.assertEqual(hermes_state.learned_skill_names(JOURNEY), ["learned-one"])


class CronWrapperTests(unittest.TestCase):
    def test_wrapper_runs_workspace_snapshot_tool(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            workspace = Path(temporary_directory)
            tools = workspace / "Tools"
            tools.mkdir()
            (tools / "hermes_state.py").write_text(
                "from pathlib import Path\nPath('wrapper-called').write_text('yes', encoding='utf-8')\n",
                encoding="utf-8",
            )
            wrapper = Path(__file__).with_name("hermes_state_cron.py")

            completed = subprocess.run([sys.executable, str(wrapper)], cwd=workspace)

            self.assertEqual(completed.returncode, 0)
            self.assertEqual((workspace / "wrapper-called").read_text(encoding="utf-8"), "yes")


class SnapshotTests(unittest.TestCase):
    def test_snapshot_copies_learned_skills_memory_and_recovery_guide(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            hermes_home = root / "hermes"
            workspace = root / "brain"
            learned = write_skill(hermes_home, "reasoning/learned-one", "learned-one")
            (learned / "references").mkdir()
            (learned / "references" / "details.md").write_text("details\n", encoding="utf-8")
            write_skill(hermes_home, "bundled/bundled-one", "bundled-one")
            (hermes_home / "memories").mkdir()
            (hermes_home / "memories" / "MEMORY.md").write_text("memory\n", encoding="utf-8")
            (hermes_home / "memories" / "USER.md").write_text("user\n", encoding="utf-8")

            result = hermes_state.snapshot(
                workspace=workspace,
                hermes_home=hermes_home,
                profile="default",
                journey=JOURNEY,
            )

            state = workspace / "Agent-State" / "Hermes" / "default"
            self.assertGreater(result.changed_files, 0)
            self.assertTrue((state / "skills" / "reasoning" / "learned-one" / "SKILL.md").is_file())
            self.assertEqual(
                (state / "skills" / "reasoning" / "learned-one" / "references" / "details.md").read_text(encoding="utf-8"),
                "details\n",
            )
            self.assertFalse((state / "skills" / "bundled" / "bundled-one").exists())
            self.assertEqual((state / "memories" / "MEMORY.md").read_text(encoding="utf-8"), "memory\n")
            self.assertTrue((state / "RECOVERY.md").is_file())
            self.assertIn("hermes_state_cron.py", (state / "RECOVERY.md").read_text(encoding="utf-8"))
            manifest = json.loads((state / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["skills"][0]["name"], "learned-one")
            self.assertNotIn(str(hermes_home), json.dumps(manifest))

    def test_second_identical_snapshot_is_a_noop(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            hermes_home = root / "hermes"
            workspace = root / "brain"
            write_skill(hermes_home, "reasoning/learned-one", "learned-one")
            (hermes_home / "memories").mkdir()
            (hermes_home / "memories" / "MEMORY.md").write_text("memory\n", encoding="utf-8")
            (hermes_home / "memories" / "USER.md").write_text("user\n", encoding="utf-8")

            hermes_state.snapshot(workspace, hermes_home, "default", JOURNEY)
            result = hermes_state.snapshot(workspace, hermes_home, "default", JOURNEY)

            self.assertEqual(result.changed_files, 0)

    def test_snapshot_fails_when_a_learned_skill_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            hermes_home = root / "hermes"
            (hermes_home / "skills").mkdir(parents=True)
            (hermes_home / "memories").mkdir()
            (hermes_home / "memories" / "MEMORY.md").write_text("memory\n", encoding="utf-8")
            (hermes_home / "memories" / "USER.md").write_text("user\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "learned-one"):
                hermes_state.snapshot(root / "brain", hermes_home, "default", JOURNEY)


class StatusAndRestoreTests(unittest.TestCase):
    def create_snapshot(self, root: Path) -> tuple[Path, Path]:
        hermes_home = root / "hermes"
        workspace = root / "brain"
        write_skill(hermes_home, "reasoning/learned-one", "learned-one")
        (hermes_home / "memories").mkdir()
        (hermes_home / "memories" / "MEMORY.md").write_text("memory\n", encoding="utf-8")
        (hermes_home / "memories" / "USER.md").write_text("user\n", encoding="utf-8")
        hermes_state.snapshot(workspace, hermes_home, "default", JOURNEY)
        return workspace, hermes_home

    def test_status_detects_live_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            workspace, hermes_home = self.create_snapshot(Path(temporary_directory))
            (hermes_home / "memories" / "MEMORY.md").write_text("changed\n", encoding="utf-8")

            result = hermes_state.status(workspace, hermes_home, "default", JOURNEY)

            self.assertFalse(result.in_sync)
            self.assertIn("memories/MEMORY.md", result.changed)

    def test_restore_recreates_memory_and_skills_in_empty_home(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            workspace, _ = self.create_snapshot(root)
            restored = root / "restored"

            result = hermes_state.restore(workspace, restored, "default")

            self.assertGreater(result.changed_files, 0)
            self.assertEqual((restored / "memories" / "MEMORY.md").read_text(encoding="utf-8"), "memory\n")
            self.assertTrue((restored / "skills" / "reasoning" / "learned-one" / "SKILL.md").is_file())

    def test_restored_skills_remain_tracked_without_journey_history(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            workspace, _ = self.create_snapshot(root)
            restored = root / "restored"
            hermes_state.restore(workspace, restored, "default")
            empty_journey = {"nodes": []}

            status = hermes_state.status(workspace, restored, "default", empty_journey)
            snapshot = hermes_state.snapshot(workspace, restored, "default", empty_journey)

            self.assertTrue(status.in_sync)
            self.assertEqual(snapshot.skill_count, 1)
            self.assertEqual(snapshot.changed_files, 0)

    def test_restore_refuses_to_overwrite_different_live_files_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            workspace, _ = self.create_snapshot(root)
            restored = root / "restored"
            (restored / "memories").mkdir(parents=True)
            (restored / "memories" / "MEMORY.md").write_text("newer\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "--force"):
                hermes_state.restore(workspace, restored, "default")

            self.assertEqual((restored / "memories" / "MEMORY.md").read_text(encoding="utf-8"), "newer\n")


if __name__ == "__main__":
    unittest.main()
