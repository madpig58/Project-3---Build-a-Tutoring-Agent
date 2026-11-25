"""The keys guard: a PreToolUse hook that keeps keys/ away from the tutor's main conversation.

Registered in .claude/settings.json for Read, Grep, Glob, Bash and PowerShell, with
"onFailure": "block". Claude Code sends the hook's input as JSON on stdin; exit 0 lets the tool
call run, exit 2 blocks it, and the model reads the message printed on stderr.

Who may read keys/ (the hook input's agent_type, the subagent's frontmatter name):
- grader: grading needs the key, and it grades in a subagent so the main conversation never
  holds an answer it could leak.
- grade-reviewer: it regrades every item from the key before it checks the grader's draft.
- quiz-reviewer: a new quiz must reuse the misconception ids the earlier keys already use, and
  in a fresh workspace those ids live only in keys/; the reviewer checks the draft key's ids
  against the earlier keys, so the quiz skill in the main conversation never has to open them.
Nobody else: the main conversation (no agent_type) and every other subagent. Each agent allowed
here is one more place a key could leak from.

What counts as reaching keys/, for the main conversation:
- Read: a file_path with a folder named keys in it (any case, / or \\, relative or absolute).
- Glob: a pattern or path with a keys folder in it. Glob returns file names only, so a pattern
  such as **/*.json that lists keys/0001.json without its contents is allowed.
- Grep: a path or glob that names keys, or a search whose scope holds keys/ (the workspace root,
  or a folder above it) unless its glob keeps keys/ out (such as *.html or !keys/**), since a
  search over the root returns lines from the keys.
- Bash and PowerShell: a word naming a keys folder (keys/0001.json, ./keys, keys\\0001.json, an
  absolute path, git show HEAD:keys/0001.json, cd keys); a wildcard folder that matches keys
  (*/0001.json, k*/*); or a recursive content search over a scope that holds keys/ (grep -r .,
  rg, git grep, findstr /s, Select-String or Get-Content with -Recurse, find with -exec or xargs).
- Draft keys (drafts/key-0002.json) are guarded the same way, because a draft stays behind with the
  same answers as the final key: Read, Grep over drafts/ or the root, and shell commands that name
  a draft key, match one with a wildcard, or do anything but list drafts/. Glob still lists names.
  The quiz skill needs no read: it wrote the draft, so it edits it or writes it again. Edit and
  Write are not hooked. Other drafts, such as lessons and grades, stay readable.
- Any other tool: any string in its input that names a keys folder.
Input the script cannot read is blocked on purpose, so a broken call never reads a key.

Known gaps, accepted: a shell command that builds the folder's name at run time (variables, string
concatenation, base64, an interpreter running inline code), or that copies the whole workspace
(cp -r . elsewhere) and reads the copy, gets past the word checks; a draft key
saved under another name or in another folder is not recognized; and the conversation that writes a
quiz has its answers in context until that session ends.
Tests: tests/test_guard.py at the repo root.
"""

from __future__ import annotations

import fnmatch
import json
import os
import re
import sys

ALLOWED_AGENTS = {"grader", "grade-reviewer", "quiz-reviewer"}
KEYS = "keys"
DRAFTS = "drafts"
# a draft key's file name: key as a whole word of the name, as in key-0002.json or quiz_key.json
KEY_NAME = re.compile(r"(?:^|[-_.])keys?(?:[-_.*?\[\d]|$)")
NOT_KEYS = (".html", ".md")
LISTING_COMMANDS = {"ls", "dir", "gci", "get-childitem", "mkdir", "new-item", "test-path", "echo", "pwd"}

# a keys folder named in a shell command: keys followed by a separator or the end, after a
# separator, quote, = or : (so dict.keys() and keys.json do not count)
KEYS_WORD = re.compile(r"(?:^|[\s/'\"=:;(|&<>,`])keys\.*(?:::|[/'\"\s;|&)<>,*?`]|$)")
WORD_SPLIT = re.compile(r"[\s'\";|&()<>=,`]+")
WILDCARD = re.compile(r"[*?\[]")
CONTENT_COMMANDS = {
    "cat", "type", "gc", "get-content", "more", "less", "head", "tail", "grep", "egrep", "fgrep",
    "rg", "findstr", "select-string", "sls", "xargs", "strings", "od", "xxd", "awk", "sed",
}
RECURSIVE_FLAG = re.compile(r"(?:^|\s)(?:-[a-z]*r[a-z]*|--recursive|-recurse|/s)(?:\s|$)")
ROOT_WORDS = {".", "./", "..", "../", "*", "**", "~", "/", "*.*", ".\\", "..\\"}


def norm(path: str) -> str:
    return path.replace("\\", "/").strip().lower()


def parts_of(path: str) -> list[str]:
    """The parts of a path as Windows opens them: it drops trailing dots and spaces from a name, and
    reads keys::$INDEX_ALLOCATION as keys."""
    out = []
    for part in norm(path).split("/"):
        if part not in (".", "..") and not re.fullmatch(r"[a-z]:", part):
            part = part.split(":")[0].rstrip(". ") if len(part) > 2 else part
        if part:
            out.append(part)
    return out


def expand_command(command: str) -> str:
    """The command with brace lists written out: cat {keys,x}/1 -> cat keys/1 x/1."""
    return " ".join(e for word in norm(command).split(" ") for e in expand_braces(word))


def has_keys_folder(path: str) -> bool:
    """True when a path names a folder called keys: keys, keys/0001.json, C:\\w\\keys\\0001.json."""
    return KEYS in parts_of(path)


def resolve(path: str, cwd: str) -> str:
    path = path.strip() or "."
    path = re.sub(r"(?<=[^./\s])[. ]+(?=/|$)", "", path.replace(chr(92), "/"))  # Windows drops trailing dots and spaces
    if not os.path.isabs(path):
        path = os.path.join(cwd, path)
    return os.path.normcase(os.path.normpath(path))


def scope_holds_keys(path: str, cwd: str) -> bool:
    """True when searching under path would reach cwd/keys: path is keys, inside it, or above it."""
    if has_keys_folder(path):
        return True
    target = resolve(path, cwd)
    keys_dir = os.path.normcase(os.path.normpath(os.path.join(cwd, KEYS)))
    return keys_dir == target or keys_dir.startswith(target.rstrip(os.sep) + os.sep)


def expand_braces(glob: str) -> list[str]:
    """a/{b,c}/*.json -> [a/b/*.json, a/c/*.json], for one level of braces at a time."""
    match = re.search(r"\{([^{}]*)\}", glob)
    if not match:
        return [glob]
    out: list[str] = []
    for choice in match.group(1).split(","):
        out.extend(expand_braces(glob[: match.start()] + choice + glob[match.end():]))
    return out


def split_globs(glob: str) -> list[str]:
    """Claude Code's Grep takes several globs in one string, split on spaces and commas."""
    out: list[str] = []
    for g in expand_braces(norm(glob)):
        out.extend(part for part in re.split(r"[\s,]+", g) if part)
    return out


def is_draft_key(path: str) -> bool:
    """True for a draft answer key: drafts/key-0002.json, C:\\w\\drafts\\key-0002.json."""
    parts = parts_of(os.path.normpath(path))
    return len(parts) > 1 and DRAFTS in parts[:-1] and bool(KEY_NAME.search(parts[-1])) and not parts[-1].endswith(NOT_KEYS)


def name_may_be_draft_key(name: str) -> bool:
    """Could a file name, which may hold wildcards, be a draft key's name?"""
    if name.endswith(NOT_KEYS):
        return False
    if KEY_NAME.search(name):
        return True
    wild = WILDCARD.search(name)
    if not wild:
        return False
    suffix = name.rsplit(".", 1)[-1] if "." in name else ""
    if suffix and not WILDCARD.search(suffix) and suffix != "json":
        return False
    prefix = name[: wild.start()]
    return "key".startswith(prefix) or prefix.startswith("key")


def glob_may_match(glob: str, folder: str) -> bool:
    """Could a Grep glob select a key file in folder (keys or drafts)?

    As in ripgrep, the last glob that matches decides. An exclusion counts only when it plainly
    leaves out the whole folder."""
    selected: bool | None = None
    positives = False
    for g in split_globs(glob):
        if g.startswith("!"):
            rest = g[1:].removeprefix("./").strip("/")
            if rest in (folder, f"{folder}/*", f"{folder}/**", f"**/{folder}/**", f"**/{folder}", "*.json", "**/*.json"):
                selected = False
            continue
        positives = True
        parts = [p for p in g.split("/") if p and p != "."]
        name = parts[-1] if parts else "*"
        folders = parts[:-1]
        suffix = name.rsplit(".", 1)[-1] if "." in name else ""
        if suffix and not WILDCARD.search(suffix) and suffix != "json":
            continue
        if folders and not any(p == "**" or fnmatch.fnmatch(folder, p) for p in folders):
            continue
        if folder == DRAFTS and name != DRAFTS and not name_may_be_draft_key(name):
            continue
        selected = True
    return selected if selected is not None else not positives


def wildcard_folder_matches_keys(command: str) -> bool:
    """*/0001.json or k*/*: a wildcard folder part (not the last part) that matches keys."""
    for word in WORD_SPLIT.split(norm(command)):
        parts = [p for p in word.split("/") if p]
        for part in parts[:-1]:
            if WILDCARD.search(part) and fnmatch.fnmatch(KEYS, part):
                return True
    return False


def recursive_search_reaches_keys(command: str, cwd: str) -> bool:
    """A recursive content search whose scope includes keys/.

    Allowed only when it names at least one existing folder below the workspace root that does not
    hold keys/, and nothing that stands for the root or a folder above it."""
    text = norm(command)
    words = [w for w in WORD_SPLIT.split(text) if w]
    names = {w.rsplit("/", 1)[-1].removesuffix(".exe") for w in words}
    recursive = (
        (names & {"grep", "egrep", "fgrep", "findstr", "select-string", "sls", "get-content", "gc", "cat", "type"}
         and RECURSIVE_FLAG.search(text))
        or "rg" in names
        or re.search(r"(?:^|\s)git\s+grep(?:\s|$)", text)
        or ("find" in names and ("-exec" in words or "xargs" in names))
        or (names & {"get-childitem", "gci", "ls", "dir"} and RECURSIVE_FLAG.search(text) and names & CONTENT_COMMANDS)
    )
    if not recursive:
        return False
    safe_folder = False
    for word in words:
        if word in ROOT_WORDS:
            return True
        if word.startswith("-") or word.startswith("/") and len(word) == 2:
            continue
        if "/" in word or os.path.isdir(os.path.join(cwd, word)):
            if scope_holds_keys(word, cwd) and (os.path.isabs(word) or word.startswith(".")):
                return True
            if os.path.isdir(os.path.join(cwd, word)) and not scope_holds_keys(word, cwd):
                safe_folder = True
    return not safe_folder


def shell_reaches_draft_key(command: str) -> bool:
    """A shell command that names a draft key, by name or wildcard, or does anything but list drafts/."""
    bare = False  # drafts/ named as a whole folder
    for word in WORD_SPLIT.split(expand_command(command)):
        parts = [p for p in parts_of(word) if p != "."]
        if not parts:
            continue
        name = parts[-1]
        in_drafts = any(fnmatch.fnmatch(DRAFTS, p) for p in parts[:-1])
        if in_drafts and name_may_be_draft_key(name):
            return True
        if re.match(r"keys?[-_.*?\[\d]", name) and not name.endswith(NOT_KEYS):  # cd drafts && cat key-0002.json
            return True
        bare = bare or name == DRAFTS or (name.startswith("d") and fnmatch.fnmatch(DRAFTS, name))
    if not bare:
        return False
    for segment in re.split(r"[;|&()`\n]+", norm(command)):
        first = segment.split()
        if first and first[0].rsplit("/", 1)[-1].removesuffix(".exe") not in LISTING_COMMANDS:
            return True
    return False


def shell_reaches_keys(command: str, cwd: str) -> bool:
    command = expand_command(command)
    text = norm(command)
    return bool(KEYS_WORD.search(text)) or wildcard_folder_matches_keys(command) or recursive_search_reaches_keys(command, cwd)


def strings_in(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in strings_in(v)]
    if isinstance(value, list):
        return [s for v in value for s in strings_in(v)]
    return []


def reason_blocked(tool: str, tool_input: dict, cwd: str) -> str | None:
    """Why this call by the main conversation reaches keys/, or None when it does not."""
    if tool == "Read":
        path = tool_input.get("file_path", "")
        return f"Read of {path}" if has_keys_folder(path) or is_draft_key(path) else None
    if tool == "Glob":
        for field in ("pattern", "path"):
            value = tool_input.get(field) or ""
            if has_keys_folder(value):
                return f"Glob over {value}"
        return None
    if tool == "Grep":
        path = tool_input.get("path") or "."
        glob = tool_input.get("glob") or ""
        if has_keys_folder(path) or (glob and has_keys_folder(glob)):
            return f"Grep in {path} {glob}".strip()
        if is_draft_key(path):
            return f"Grep in {path}"
        drafts_dir = os.path.normcase(os.path.normpath(os.path.join(cwd, DRAFTS)))
        target = resolve(path, cwd)
        takes_in = [KEYS] if scope_holds_keys(path, cwd) else []
        if drafts_dir == target or drafts_dir.startswith(target.rstrip(os.sep) + os.sep):
            takes_in.append(DRAFTS)
        for folder in takes_in:
            what = "keys/" if folder == KEYS else "the draft keys in drafts/"
            if glob:
                if glob_may_match(glob, folder):
                    return f"Grep over {path} with glob {glob}, which takes in {what}"
            elif (tool_input.get("type") or "").lower() in ("", "json"):
                return (f"Grep over {path}, which takes in {what}; search a folder such as lessons/ or "
                        "quizzes/, or add a glob that leaves the keys out, such as *.html or !*.json")
        return None
    if tool in ("Bash", "PowerShell"):
        command = tool_input.get("command", "")
        if shell_reaches_keys(command, cwd):
            return f"{tool} command that reaches keys/: {command}"
        return f"{tool} command that reaches a draft key in drafts/: {command}" if shell_reaches_draft_key(command) else None
    for value in strings_in(tool_input):
        if has_keys_folder(value) or is_draft_key(value):
            return f"{tool} with {value}"
    return None


def block(message: str) -> None:
    sys.stderr.write(
        f"Blocked by the keys guard: {message}. "
        "The answer keys in keys/ and the draft keys in drafts/ are readable only by the grader, grade-reviewer and quiz-reviewer subagents. "
        "Tutoring and showing a quiz need no key (read the quiz in quizzes/); grading reads the key "
        "through the grader subagent. To revise a draft key you wrote in this conversation, Edit it or "
        "Write it again in full from what you already have; do not read it back.\n"
    )
    sys.exit(2)


def main() -> None:
    try:
        # Claude Code sends UTF-8: read the raw bytes once and decode them strictly, since the
        # console's code page (cp949, cp1252...) would misread any non-ASCII path or command
        raw = sys.stdin.buffer.read()
        data = json.loads(raw.decode("utf-8", errors="strict") or "null")
    except (UnicodeDecodeError, ValueError):  # bytes that are not UTF-8, or text that is not JSON
        block("the hook's input could not be read, so the call is refused to be safe")
    if not isinstance(data, dict) or not isinstance(data.get("tool_name"), str):
        block("the hook's input had no tool name, so the call is refused to be safe")
    agent = data.get("agent_type")
    if isinstance(agent, str) and agent in ALLOWED_AGENTS:
        sys.exit(0)
    tool_input = data.get("tool_input")
    if not isinstance(tool_input, dict):
        tool_input = {}
    cwd = data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    reason = reason_blocked(data["tool_name"], tool_input, str(cwd))
    if reason:
        who = f"the {agent} subagent" if isinstance(agent, str) and agent else "the main conversation"
        block(f"{reason} (by {who})")
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:  # decide on purpose: an error never lets a call through
        block(f"the guard hit an error ({type(exc).__name__}), so the call is refused to be safe")
