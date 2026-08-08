from __future__ import annotations

import io
import re
import tempfile
import unittest
from contextlib import redirect_stderr
from datetime import date
from pathlib import Path
from urllib.parse import unquote

import brain  # pyright: ignore[reportImplicitRelativeImport]
import product_sync  # pyright: ignore[reportImplicitRelativeImport]


class FrontmatterParserTests(unittest.TestCase):
    def test_parses_scalars_inline_lists_and_block_lists(self) -> None:
        document = """---
type: knowledge
title: "A title"
topics: [python, "personal knowledge"]
sources:
  - https://example.com/article
  - Brain/Sources/example.md
---

# Fallback title

Body text.
"""

        parsed = brain.parse_frontmatter(document)

        self.assertTrue(parsed.has_frontmatter)
        self.assertIsNone(parsed.error)
        self.assertEqual(parsed.metadata["type"], "knowledge")
        self.assertEqual(parsed.metadata["title"], "A title")
        self.assertEqual(parsed.metadata["topics"], ["python", "personal knowledge"])
        self.assertEqual(
            parsed.metadata["sources"],
            ["https://example.com/article", "Brain/Sources/example.md"],
        )
        self.assertIn("# Fallback title", parsed.body)

    def test_reports_unterminated_and_malformed_frontmatter(self) -> None:
        unterminated = brain.parse_frontmatter("---\ntype: knowledge\n# no closing delimiter")
        malformed = brain.parse_frontmatter("---\ntype knowledge\n---\n# Title")

        self.assertEqual(unterminated.error, "unterminated YAML frontmatter")
        self.assertIn("key: value", malformed.error or "")
        self.assertEqual(malformed.error_line, 2)


class IndexTests(unittest.TestCase):
    def test_index_is_stable_and_contains_resolvable_relative_links(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            knowledge = root / "Brain" / "Knowledge"
            project = root / "Projects" / "Example Project"
            knowledge.mkdir(parents=True)
            project.mkdir(parents=True)
            (knowledge / "alpha note.md").write_text(
                "---\ntype: knowledge\ntitle: Alpha\nstatus: unprocessed\n"
                "sources: [https://example.com]\n---\n\n"
                "# Ignored H1\n\nFirst meaningful paragraph.\n",
                encoding="utf-8",
            )
            (project / "CONTEXT.md").write_text(
                "# Example Context\n\nProject summary.\n", encoding="utf-8"
            )

            first = brain.build_index(root)
            second = brain.build_index(root)

            self.assertEqual(first, second)
            self.assertIn(brain.GENERATED_MARKER, first)
            self.assertNotRegex(first, r"Generated at|\d{2}:\d{2}:\d{2}")
            self.assertIn("status: `unprocessed`", first)
            self.assertIn("First meaningful paragraph.", first)

            destinations = re.findall(r"\[[^]]+\]\(([^)]+)\)", first)
            self.assertEqual(len(destinations), 2)
            for destination in destinations:
                resolved = root / "Brain" / unquote(destination)
                self.assertTrue(resolved.exists(), destination)

    def test_index_check_detects_stale_content_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "Brain" / "Knowledge").mkdir(parents=True)
            (root / "Projects").mkdir()
            (root / "Brain" / "Knowledge" / "note.md").write_text(
                "# Knowledge\n\nSummary.\n", encoding="utf-8"
            )
            index_path = root / "Brain" / "INDEX.md"
            index_path.write_text("stale\n", encoding="utf-8")

            error_output = io.StringIO()
            with redirect_stderr(error_output):
                result = brain.update_index(root, check=True)

            self.assertEqual(result, 1)
            self.assertIn("INDEX.md is stale", error_output.getvalue())
            self.assertEqual(index_path.read_text(encoding="utf-8"), "stale\n")


class LintTests(unittest.TestCase):
    def test_non_english_provenance_heading_is_supported_without_changing_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            knowledge = root / "Brain" / "Knowledge"
            knowledge.mkdir(parents=True)
            (root / "Projects").mkdir()
            heading = "\u041f\u0440\u043e\u0438\u0441\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u0435"
            note = knowledge / "note.md"
            note.write_text(
                "---\ntype: knowledge\nstatus: active\n---\n\n"
                f"# Note\n\n## {heading}\n\nUser-provided source record.\n",
                encoding="utf-8",
            )

            issues = brain.lint_workspace(root)

            self.assertFalse([issue for issue in issues if "provenance" in issue.message])

    def test_broken_relative_link_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            knowledge = root / "Brain" / "Knowledge"
            (root / "Projects").mkdir(parents=True)
            knowledge.mkdir(parents=True)
            note = knowledge / "note.md"
            note.write_text(
                "# Note\n\n[Missing document](missing.md)\n", encoding="utf-8"
            )

            issues = brain.lint_workspace(root)

            broken = [issue for issue in issues if "broken relative link" in issue.message]
            self.assertEqual(len(broken), 1)
            self.assertEqual(broken[0].severity, "ERROR")
            self.assertEqual(broken[0].path, note)
            self.assertEqual(broken[0].line, 3)

    def test_broken_link_in_root_document_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "Brain").mkdir()
            readme = root / "README.md"
            readme.write_text("# Workspace\n\n[Missing guide](missing.md)\n", encoding="utf-8")

            issues = brain.lint_workspace(root)

            broken = [issue for issue in issues if "broken relative link" in issue.message]
            self.assertEqual(len(broken), 1)
            self.assertEqual(broken[0].path, readme)

    def test_external_and_existing_relative_links_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            knowledge = root / "Brain" / "Knowledge"
            (root / "Projects").mkdir(parents=True)
            knowledge.mkdir(parents=True)
            (knowledge / "target.md").write_text("# Target\n", encoding="utf-8")
            (knowledge / "note.md").write_text(
                "# Note\n\n[Target](target.md) and [Web](https://example.com).\n",
                encoding="utf-8",
            )

            issues = brain.lint_workspace(root)

            self.assertFalse([issue for issue in issues if issue.severity == "ERROR"])

    def test_binary_artifact_with_valid_manifest_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            raw = root / "Brain" / "Sources" / "Raw"
            raw.mkdir(parents=True)
            (raw / "source.bin").write_bytes(b"\x00\xff\x10binary")
            (raw / "source.md").write_text(
                "---\nsource_url: https://example.com/source\nretrieved_at: 2026-07-14\n"
                "artifact_path: source.bin\ncontent_hash: sha256:test\n---\n\n# Source manifest\n",
                encoding="utf-8",
            )

            issues = brain.lint_workspace(root)

            self.assertFalse([issue for issue in issues if issue.severity == "ERROR"])
            self.assertFalse([issue for issue in issues if "content_hash" in issue.message])

    def test_artifact_without_content_hash_is_only_a_warning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            raw = root / "Brain" / "Sources" / "Raw"
            raw.mkdir(parents=True)
            (raw / "source.bin").write_bytes(b"\x00\xffbinary")
            (raw / "source.md").write_text(
                "---\nsource_url: https://example.com/source\nretrieved_at: 2026-07-14\n"
                "artifact_path: source.bin\n---\n\n# Source manifest\n",
                encoding="utf-8",
            )

            issues = brain.lint_workspace(root)

            self.assertFalse([issue for issue in issues if issue.severity == "ERROR"])
            hash_warnings = [issue for issue in issues if "content_hash" in issue.message]
            self.assertEqual(len(hash_warnings), 1)
            self.assertEqual(hash_warnings[0].severity, "WARN")

    def test_locator_only_manifest_does_not_require_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            raw = root / "Brain" / "Sources" / "Raw"
            raw.mkdir(parents=True)
            (raw / "locator.md").write_text(
                "---\nsource_url: https://example.com/source\nretrieved_at: 2026-07-14\n---\n\n"
                "# Locator-only manifest\n",
                encoding="utf-8",
            )

            issues = brain.lint_workspace(root)

            self.assertFalse([issue for issue in issues if issue.severity == "ERROR"])

    def test_binary_artifact_without_manifest_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            raw = root / "Brain" / "Sources" / "Raw"
            raw.mkdir(parents=True)
            artifact = raw / "orphan.pdf"
            artifact.write_bytes(b"%PDF-\x00\xff")

            issues = brain.lint_workspace(root)

            orphan_errors = [issue for issue in issues if "has no Markdown manifest" in issue.message]
            self.assertEqual(len(orphan_errors), 1)
            self.assertEqual(orphan_errors[0].severity, "ERROR")
            self.assertEqual(orphan_errors[0].path, artifact)

    def test_manifest_with_missing_artifact_is_an_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            raw = root / "Brain" / "Sources" / "Raw"
            raw.mkdir(parents=True)
            manifest = raw / "missing.md"
            manifest.write_text(
                "---\nsource_url: https://example.com/source\nretrieved_at: 2026-07-14\n"
                "artifact_path: missing.bin\n---\n\n# Missing artifact\n",
                encoding="utf-8",
            )

            issues = brain.lint_workspace(root)

            missing_errors = [issue for issue in issues if "artifact_path does not exist" in issue.message]
            self.assertEqual(len(missing_errors), 1)
            self.assertEqual(missing_errors[0].severity, "ERROR")
            self.assertEqual(missing_errors[0].path, manifest)

    def test_source_record_raw_materials_is_a_locator(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            sources = root / "Brain" / "Sources"
            sources.mkdir(parents=True)
            (sources / "record.md").write_text(
                "---\ntype: source\nraw_materials: [Raw/source.md]\n---\n\n# Source record\n",
                encoding="utf-8",
            )

            issues = brain.lint_workspace(root)

            self.assertFalse([issue for issue in issues if "no raw locator" in issue.message])


class LogTests(unittest.TestCase):
    def test_log_writes_metadata_only_and_normalizes_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            brain.append_log(
                root,
                operation="sync",
                title="Update context",
                files=[str(root / "Brain" / "Knowledge" / "note.md")],
                note="No file contents included",
                today=date(2026, 7, 14),
            )

            content = (root / "Brain" / "LOG.md").read_text(encoding="utf-8")
            self.assertIn("## [2026-07-14] sync | Update context", content)
            self.assertIn("`Brain/Knowledge/note.md`", content)
            self.assertIn("Note: No file contents included", content)

    def test_external_absolute_path_is_rejected_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            external = root.parent / "outside-workspace.bin"

            with self.assertRaisesRegex(ValueError, "outside workspace"):
                brain.append_log(
                    root,
                    operation="sync",
                    title="Reject external path",
                    files=[str(external.resolve())],
                )

            self.assertFalse((root / "Brain" / "LOG.md").exists())

    def test_log_field_lengths_are_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            with self.assertRaises(ValueError):
                brain.append_log(root, operation="o" * 41, title="Title")
            with self.assertRaises(ValueError):
                brain.append_log(root, operation="sync", title="t" * 161)
            with self.assertRaises(ValueError):
                brain.append_log(root, operation="sync", title="Title", note="n" * 241)

            self.assertFalse((root / "Brain" / "LOG.md").exists())


class ProductSyncTests(unittest.TestCase):
    def test_identical_roots_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)

            with self.assertRaisesRegex(ValueError, "must be different"):
                product_sync.validate_roots(root, root)

    def test_nested_roots_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            child = root / "child"
            child.mkdir()

            with self.assertRaisesRegex(ValueError, "must not be nested"):
                product_sync.validate_roots(root, child)
            with self.assertRaisesRegex(ValueError, "must not be nested"):
                product_sync.validate_roots(child, root)

    def test_directory_copy_preserves_target_specific_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "source"
            target = root / "target"
            (source / "Templates").mkdir(parents=True)
            (target / "Templates").mkdir(parents=True)
            (source / "Templates" / "Product.md").write_text("product\n", encoding="utf-8")
            private_file = target / "Templates" / "Private.md"
            private_file.write_text("private\n", encoding="utf-8")

            result = product_sync.copy_path(source, target, "Templates", dry_run=False)

            self.assertEqual(result, "copied: Templates")
            self.assertEqual(
                (target / "Templates" / "Product.md").read_text(encoding="utf-8"),
                "product\n",
            )
            self.assertEqual(private_file.read_text(encoding="utf-8"), "private\n")


if __name__ == "__main__":
    unittest.main()
