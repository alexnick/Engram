# Quickstart

Engram keeps durable knowledge in Markdown. Chat is where you think; the Engram is what survives the conversation.

## 1. Open the workspace

Clone the repository and open the folder in an agent harness that reads `AGENTS.md`.

```bash
git clone https://github.com/alexnick/Engram.git engram
cd engram
```

The agent should load the workspace rules automatically. You should not need to explain the storage model in every session.

## 2. Preserve a thought

Say:

```text
Save this exact thought: optimization can remove the choices that make a game interesting.
```

Or use the short command:

```text
/capture Optimization can remove the choices that make a game interesting.
```

Expected result: a new raw capture under `Engram/Inbox/`. The original wording remains unchanged. The capture is evidence of what you said, not proof that the statement is true.

## 3. Ask the Engram

```text
What does the Engram know about optimization and player choice? Link the pages you use.
```

Query is read-only. It should cite durable pages and say when the Engram does not yet contain an answer.

## 4. Develop the idea

```text
Help me explore when optimization reduces meaningful choice. Ask one question at a time.
```

Explore may keep a temporary session note, but it does not silently turn conclusions into durable knowledge.

For a larger effort, start a Project Map instead:

```text
Create a project map for redesigning this game system from high-level goals to an implementation plan.
```

## 5. Save the result

When the discussion reaches a useful conclusion:

```text
Show me a Sync proposal for the durable changes. Do not write anything until I approve it.
```

The agent should name the files and claims it wants to change. Approve all, approve selected items, revise the proposal, or reject it.

## 6. Check the workspace

```bash
python Tools/engram.py status
python Tools/engram.py index
python Tools/engram.py lint
python Tools/test_engram.py
```

`Engram/INDEX.md` is generated. Do not edit it by hand.

## What to say when you are unsure

```text
I do not know whether this should be a capture, an exploration, or a durable update. Choose the safest workflow and explain why.
```

```text
Show me exactly what you plan to write before you change the Engram.
```

```text
List the files changed in this session and explain each change.
```

Next: [User Guide](USER-GUIDE.md).
