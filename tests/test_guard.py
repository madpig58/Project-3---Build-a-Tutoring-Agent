"""Tests of the tutor's keys guard, tutor/.claude/hooks/keys_guard.py.

Each test writes a sample PreToolUse hook input to the script's stdin, as Claude Code does, and
checks the exit code: 2 blocks the call, 0 lets it run. The workspace is a temporary folder with
keys/, quizzes/, lessons/ and drafts/ in it, given to the hook as its cwd.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "tutor" / ".claude" / "hooks" / "keys_guard.py"
SETTINGS = ROOT / "tutor" / ".claude" / "settings.json"


class GuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.ws = cls._tmp.name
        for folder in ("keys", "quizzes", "lessons", "drafts", "learning-records"):
            os.makedirs(os.path.join(cls.ws, folder))
        Path(cls.ws, "keys", "0001.json").write_text('{"id": "0001", "items": []}', encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def run_hook(self, tool, tool_input, agent=None, raw=None):
        if raw is None:
            data = {"hook_event_name": "PreToolUse", "cwd": self.ws, "tool_name": tool, "tool_input": tool_input}
            if agent:
                data["agent_type"] = agent
                data["agent_id"] = "a1"
            raw = json.dumps(data)
        data = raw if isinstance(raw, bytes) else raw.encode("utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT)], input=data, capture_output=True, timeout=30)
        result.stderr = result.stderr.decode("utf-8", errors="replace")
        return result

    def assertBlocked(self, *args, **kwargs):
        result = self.run_hook(*args, **kwargs)
        self.assertEqual(result.returncode, 2, f"expected blocked: {args} {kwargs}\n{result.stderr}")
        self.assertIn("keys guard", result.stderr)

    def assertAllowed(self, *args, **kwargs):
        result = self.run_hook(*args, **kwargs)
        self.assertEqual(result.returncode, 0, f"expected allowed: {args} {kwargs}\n{result.stderr}")

    # the main conversation's reads of keys/, with each tool

    def test_main_read_blocked(self):
        self.assertBlocked("Read", {"file_path": "keys/0001.json"})

    def test_main_read_path_forms_blocked(self):
        for path in ("./keys/0001.json", "keys\\0001.json", ".\\keys\\0001.json", "KEYS/0001.json",
                     os.path.join(self.ws, "keys", "0001.json"), "lessons/../keys/0001.json"):
            with self.subTest(path=path):
                self.assertBlocked("Read", {"file_path": path})

    def test_main_grep_blocked(self):
        self.assertBlocked("Grep", {"pattern": "answer", "path": "keys"})
        self.assertBlocked("Grep", {"pattern": "answer", "path": "keys/0001.json"})
        self.assertBlocked("Grep", {"pattern": "answer", "glob": "keys/*.json"})

    def test_main_grep_over_root_blocked(self):
        self.assertBlocked("Grep", {"pattern": "answer"})
        self.assertBlocked("Grep", {"pattern": "answer", "path": "."})
        self.assertBlocked("Grep", {"pattern": "answer", "path": self.ws})
        self.assertBlocked("Grep", {"pattern": "answer", "glob": "*.json"})
        self.assertBlocked("Grep", {"pattern": "answer", "type": "json"})

    def test_main_glob_blocked(self):
        self.assertBlocked("Glob", {"pattern": "keys/*.json"})
        self.assertBlocked("Glob", {"pattern": "*.json", "path": "keys"})

    def test_main_bash_blocked(self):
        for command in ("cat keys/0001.json", "cat ./keys/0001.json", "cd keys && cat 0001.json",
                        "head -n 5 keys/*", "cat */0001.json", "cat k*/0001.json",
                        "grep -rn answer .", "grep -R answer", "rg answer", "git grep answer",
                        "git show HEAD:keys/0001.json", "find . -name '*.json' -exec cat {} +",
                        f"cat {self.ws}/keys/0001.json"):
            with self.subTest(command=command):
                self.assertBlocked("Bash", {"command": command})

    def test_main_powershell_blocked(self):
        for command in ("Get-Content keys/0001.json", "Get-Content .\\keys\\0001.json", "gc keys\\0001.json",
                        "type keys\\0001.json", "Get-ChildItem -Recurse | Select-String answer",
                        "Select-String -Path * -Pattern answer -Recurse", "findstr /s answer *.json"):
            with self.subTest(command=command):
                self.assertBlocked("PowerShell", {"command": command})

    def test_other_subagents_blocked(self):
        for agent in ("lesson-reviewer", "lesson-planner", "general-purpose", "Explore", "Quiz-Reviewer"):
            with self.subTest(agent=agent):
                self.assertBlocked("Read", {"file_path": "keys/0001.json"}, agent=agent)

    # the allowed grading workflow

    def test_grader_allowed(self):
        self.assertAllowed("Read", {"file_path": "keys/0001.json"}, agent="grader")
        self.assertAllowed("Grep", {"pattern": "answer", "path": "keys"}, agent="grader")
        self.assertAllowed("Bash", {"command": "cat keys/0001.json"}, agent="grader")

    def test_grade_reviewer_allowed(self):
        self.assertAllowed("Read", {"file_path": "keys/0001.json"}, agent="grade-reviewer")

    def test_quiz_reviewer_allowed(self):
        self.assertAllowed("Read", {"file_path": "keys/0001.json"}, agent="quiz-reviewer")
        self.assertAllowed("Glob", {"pattern": "keys/*.json"}, agent="quiz-reviewer")
        self.assertAllowed("Grep", {"pattern": "distractors", "path": "keys"}, agent="quiz-reviewer")

    def test_windows_path_forms_blocked(self):
        # Windows opens keys./0001.json as keys/0001.json
        for path in ("keys./0001.json", "keys::$INDEX_ALLOCATION/0001.json", "drafts./key-0002.json", "drafts/key-0002.json::$DATA"):
            with self.subTest(path=path):
                self.assertBlocked("Read", {"file_path": path})
                self.assertBlocked("Bash", {"command": f"cat {path}"})
        self.assertBlocked("Grep", {"pattern": "answer", "path": "keys."})
        self.assertBlocked("Grep", {"pattern": "answer", "path": "drafts."})

    def test_brace_lists_blocked(self):
        for command in ("cat {keys,lessons}/0001.json", "tail drafts/{key,quiz}-0002.json"):
            with self.subTest(command=command):
                self.assertBlocked("Bash", {"command": command})

    # draft keys: the same answers, in drafts/

    def test_draft_key_read_blocked(self):
        for path in ("drafts/key-0002.json", "./drafts/key-0002.json", "drafts\\key-0002.json", "DRAFTS/KEY-0002.json",
                     os.path.join(self.ws, "drafts", "key-0002.json"), "lessons/../drafts/key-0002.json",
                     "drafts/key-0002-v2.json", "drafts/quiz-key.json"):
            with self.subTest(path=path):
                self.assertBlocked("Read", {"file_path": path})
                self.assertBlocked("Read", {"file_path": path}, agent="lesson-reviewer")

    def test_draft_key_grep_blocked(self):
        for extra in ({"path": "drafts"}, {"path": "drafts/key-0002.json"}, {"path": "drafts", "glob": "*.json"},
                      {"path": "drafts", "glob": "key-0003.json"}, {"glob": "drafts/*"}, {"glob": "key-*"},
                      {"glob": "!keys/**"}, {"glob": "!keys/** *.json"}, {"glob": "**/key*.json"},
                      {"path": os.path.join(self.ws, "drafts")}, {"path": "drafts", "type": "json"}):
            with self.subTest(extra=extra):
                self.assertBlocked("Grep", {"pattern": "answer", **extra})

    def test_keys_grep_globs_blocked(self):
        for glob in ("*.html *.json", "*.html,*.json", "0003.json", "!keys/0001.json", "!*.json keys/*", "{lessons,keys}/*"):
            with self.subTest(glob=glob):
                self.assertBlocked("Grep", {"pattern": "answer", "glob": glob})

    def test_draft_key_shell_blocked(self):
        for command in ("cat drafts/key-0002.json", "cd drafts && cat key-0002.json", "cat drafts/*", "cat drafts/k*",
                        "cat d*/k*.json", "cd drafts; cat *", "grep -rn answer drafts", "grep -r answer ./drafts/",
                        "cp -r drafts out", "cp drafts/key-0002.json x.json", "ls drafts | xargs cat",
                        "python -c \"print(open('drafts/key-0002.json').read())\""):
            with self.subTest(command=command):
                self.assertBlocked("Bash", {"command": command})
        for command in ("Get-Content drafts\\key-0002.json", "Get-Content (Get-ChildItem drafts)", "gc .\\drafts\\*.json",
                        "Copy-Item drafts out -Recurse"):
            with self.subTest(command=command):
                self.assertBlocked("PowerShell", {"command": command})

    def test_draft_shell_allowed(self):
        for command in ("ls drafts", "ls -la drafts/", "mkdir -p drafts", "cat drafts/quiz-0002.json",
                        "cat drafts/grade-0001-s1.json", "cat drafts/lesson-0003.html"):
            with self.subTest(command=command):
                self.assertAllowed("Bash", {"command": command})

    def test_quiz_reviewer_reads_draft_key(self):
        self.assertAllowed("Read", {"file_path": "drafts/key-0002.json"}, agent="quiz-reviewer")

    # reads that must still work for the main conversation

    def test_main_other_reads_allowed(self):
        self.assertAllowed("Read", {"file_path": "quizzes/0001.json"})
        self.assertAllowed("Read", {"file_path": "MISSION.md"})
        self.assertAllowed("Read", {"file_path": "drafts/quiz-0002.json"})
        self.assertAllowed("Read", {"file_path": "drafts/grade-0001-s1.json"})
        self.assertAllowed("Read", {"file_path": "drafts/lesson-0003-key-ideas.html"})
        self.assertAllowed("Read", {"file_path": ".claude/skills/teach/references/QUIZZES.md"})
        self.assertAllowed("Glob", {"pattern": "lessons/*.html"})
        self.assertAllowed("Glob", {"pattern": "**/*.md"})
        self.assertAllowed("Grep", {"pattern": "O2", "path": "lessons"})
        self.assertAllowed("Grep", {"pattern": "O2", "glob": "*.html"})
        self.assertAllowed("Grep", {"pattern": "O2", "glob": "!*.json"})
        self.assertAllowed("Grep", {"pattern": "O2", "glob": "!keys/** !drafts/**"})
        self.assertAllowed("Grep", {"pattern": "O2", "glob": "quizzes/*.json"})
        self.assertAllowed("Grep", {"pattern": "O2", "path": "drafts", "glob": "grade-*.json"})
        self.assertAllowed("Grep", {"pattern": "O2", "path": "drafts", "glob": "*.html"})
        self.assertAllowed("Glob", {"pattern": "drafts/*"})
        self.assertAllowed("Grep", {"pattern": "O2", "type": "html"})

    def test_main_other_commands_allowed(self):
        for tool, command in (("Bash", "ls lessons"), ("Bash", "ls"), ("Bash", "cat quizzes/0001.json"),
                              ("Bash", "grep -rn answer lessons"), ("Bash", "python -c \"print({}.keys())\""),
                              ("Bash", "ls -R"), ("PowerShell", "Get-Content quizzes/0001.json"),
                              ("PowerShell", "Get-ChildItem lessons")):
            with self.subTest(tool=tool, command=command):
                self.assertAllowed(tool, {"command": command})

    def test_non_ascii_input_decided_not_refused(self):
        # Claude Code sends UTF-8 whatever the console's code page is
        self.assertAllowed("Read", {"file_path": "lessons/0001-한글-노트.html"})
        self.assertAllowed("Bash", {"command": "ls lessons  # A* — 경로"})
        self.assertBlocked("Read", {"file_path": "keys/0001-한글.json"})

    # input it cannot read is refused on purpose

    def test_unreadable_input_blocked(self):
        for raw in ("", "not json", "[]", '{"tool_input": {}}'):
            with self.subTest(raw=raw):
                self.assertBlocked("Read", {}, raw=raw)

    def test_invalid_utf8_blocked(self):
        # cp949 bytes for a Korean path, and a stray byte: not UTF-8, so refused rather than guessed
        good = '{"tool_name": "Read", "tool_input": {"file_path": "lessons/한글.html"}}'
        for raw in (good.encode("cp949"), b'{"tool_name": "Read", "tool_input": {"file_path": "quizzes/\xff.json"}}'):
            with self.subTest(raw=raw):
                self.assertBlocked("Read", {}, raw=raw)

    # the hook is registered where the bench runs it

    def test_registered_in_settings(self):
        settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
        entries = settings["hooks"]["PreToolUse"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(set(entries[0]["matcher"].split("|")), {"Read", "Grep", "Glob", "Bash", "PowerShell"})
        hook = entries[0]["hooks"][0]
        self.assertEqual(hook["type"], "command")
        self.assertEqual(hook.get("onFailure"), "block")
        self.assertIn("$CLAUDE_PROJECT_DIR/.claude/hooks/keys_guard.py", hook["command"])
        self.assertEqual(settings["permissions"]["deny"], ["Agent(p3-guide)"])


if __name__ == "__main__":
    unittest.main()
