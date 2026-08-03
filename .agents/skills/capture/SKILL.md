---
name: capture
description: Preserves a raw thought, observation, fact, health record, or fragment immediately without rewriting its payload. Use when the user says save this, capture this, remember this, store this, do not lose this, invokes /capture, or clearly asks to put something into the Brain without developing it first.
---

# Capture

## Goal

Prevent information loss with minimal friction while keeping the original payload immutable.

## Input

Use text following `/capture`, the current user message, a clearly identified passage from the conversation, selected text, or a named local file. If the target is genuinely ambiguous, ask one short clarification question. Otherwise do not interview the user.

## Procedure

1. Preserve the user's exact wording and original language.
2. Determine whether the content is ordinary or explicitly health-related.
3. Generate a neutral short title, one to five lightweight topic labels, zero to three possible contexts, and a one-sentence search hint.
4. Do not develop, improve, argue with, translate, or summarize away the thought.
5. Use the Capture template to create:

   * `Brain/Inbox/YYYY-MM-DD-HHmm--short-slug.md` for ordinary captures;
   * `Brain/Health/Inbox/YYYY-MM-DD-HHmm--short-slug.md` for explicit health captures.
6. Set `status: unprocessed`, the actual local timestamp, detected language, source, and sensitivity.
7. Search only for an exact or obvious near-duplicate.
8. If an obvious duplicate exists, append a separately dated `Additional Raw Capture` containing the new exact payload. Never edit the previous payload.
9. After the raw write, keep `Brain/INDEX.md` complete for the navigable corpus and add permitted processing references without changing the payload. Append a `Brain/LOG.md` entry containing only date, operation, a short non-sensitive title, affected workspace-relative paths, and an optional bounded non-sensitive note. Never copy capture content or external absolute paths into the log.
10. Report the saved path and title in one concise sentence.

## Immutability

After initial write, text under `Raw Capture` and every `Additional Raw Capture` heading is immutable. Later operations may add or correct metadata, processing status, and links around the payload. If the user corrects the thought, preserve the original and append a dated correction or create a derived page through Sync.

## Rules

* Capture writes immediately because preservation was explicitly requested.
* Never require the user to classify the thought.
* Never ask follow-up questions merely to improve metadata.
* Never create a full Knowledge, Decision, or context update during Capture.
* A capture must remain understandable without the current chat.
* Preserve exact stated dates, values, units, medication names, and dosages in health captures; do not interpret them.
* Do not create or propose a Git checkpoint merely because a capture was saved.
