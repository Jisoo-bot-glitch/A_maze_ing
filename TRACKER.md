# A-Maze-ing — Team Tracker

> Who does what. Update your rows in the same commit as the work.
> Owners: `@your_login` = Elvira, `@jisobaek` = jisoo (replace with real 42 / GitHub logins).

**Status legend:** ⬜ To do · 🟡 In progress · 🔍 In review · ✅ Done · ⛔ Blocked
**Priority:** 🔴 High · 🟠 Medium · 🟢 Low

---

## Phase 0 — Agree on interfaces (together, day 1)

| ID | Task | Owner | Status | Priority | Branch | Files | Due | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T00 | Agree `MazeConfig` fields | both | ⬜ | 🔴 | `main` | `app/config.py` |  | Freeze before parallel work |
| T01 | Agree `MazeGenerator` public API | both | ⬜ | 🔴 | `main` | `mazegen/generator.py` |  | Stub methods + docstrings |
| T02 | Repo skeleton, `.gitignore`, default `config.txt` | @teammate_login | ⬜ | 🔴 | `setup` | root |  |  |

## Phase 1 — Parsing & app (Jisoo)

| ID | Task | Owner | Status | Priority | Branch | Files | Due | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T10 | Config parser (KEY=VALUE, comments, duplicates) | @jisobaek | 🟡 | 🔴 | `feat/config` | `app/config.py` |  | Already started |
| T11 | Value validation (ints, coords, bool, bounds, entry ≠ exit) | @jisobaek | ⬜ | 🔴 | `feat/config` | `app/config.py` |  |  |
| T12 | `ConfigError` / `MazeError` | @jisobaek | ⬜ | 🟠 | `feat/config` | `app/errors.py` |  |  |
| T13 | BFS shortest path + NESW string | @jisobaek | ⬜ | 🔴 | `feat/solver` | `mazegen/solver.py` |  |  |
| T14 | `main()` + error printing to stderr | @jisobaek | ⬜ | 🔴 | `feat/main` | `a_maze_ing.py` |  | Never crash |
| T15 | Output writer (hex grid, entry, exit, path) | @jisobaek | ✅ | 🔴 | `feat/writer` | `app/writer.py` |  |  |
| T16 | ASCII render + colors | @jisobaek | ⬜ | 🟠 | `feat/display` | `app/display.py` |  | Start on a hard-coded grid |
| T17 | Menu: regen / path / colors / quit | @jisobaek | ⬜ | 🟠 | `feat/display` | `app/display.py` |  | Handle Ctrl+C / Ctrl+D |
| T18 | Makefile (install, run, debug, clean, lint, lint-strict) | @jisobaek | ⬜ | 🟠 | `chore/makefile` | `Makefile` |  | Tabs, not spaces |

## Phase 2 — Generator package (Elvira)

| ID | Task | Owner | Status | Priority | Branch | Files | Due | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T20 | Grid model + wall bits helpers | @your_login | ⬜ | 🔴 | `feat/generator` | `mazegen/generator.py` |  |  |
| T21 | "42" pattern placement + too-small warning | @your_login | ⬜ | 🔴 | `feat/generator` | `mazegen/generator.py` |  | Gap column = centre |
| T22 | Perfect maze — iterative DFS with seed | @your_login | ⬜ | 🔴 | `feat/generator` | `mazegen/generator.py` |  |  |
| T23 | Pac-Man mode — braiding, no 3×3, corners + centre | @your_login | ⬜ | 🔴 | `feat/pacman` | `mazegen/generator.py` |  | Cycles ≥ 2 |
| T24 | Self-validation (`_validate`) | @your_login | ⬜ | 🟠 | `feat/generator` | `mazegen/generator.py` |  |  |
| T25 | `pyproject.toml` + build `.whl` at root | @your_login | ⬜ | 🟠 | `chore/package` | `pyproject.toml` |  | Test in clean venv |
| T26 | `LICENSE.md` | @your_login | ⬜ | 🟢 | `chore/package` | `LICENSE.md` |  | MIT |

## Phase 3 — Integration & delivery (together)

| ID | Task | Owner | Status | Priority | Branch | Files | Due | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T30 | Merge all branches, end-to-end run | both | ⬜ | 🔴 | `main` | — |  |  |
| T31 | `maze_analyzer.py` passes (both modes) | @your_login | ⬜ | 🔴 | `main` | — |  |  |
| T32 | `make lint` clean (flake8 + mypy) | both | ⬜ | 🔴 | `main` | — |  | Each fixes own files |
| T33 | Tests: config | @teammate_login | ⬜ | 🟢 | `test/config` | `tests/test_config.py` |  | Not graded |
| T34 | Tests: generator | @your_login | ⬜ | 🟢 | `test/generator` | `tests/test_generator.py` |  | Not graded |
| T35 | README (description, instructions, resources, AI use, algorithm, reuse) | both | ⬜ | 🟠 | `docs/readme` | `README.md` |  | First line italic with logins |
| T36 | Defense prep: each explains the whole code | both | ⬜ | 🟠 | — | — |  | Live modification possible |

---

## How to add a new field (column)

1. In the header row of a table, add `| Field name |` at the end.
2. In the `| --- |` row below it, add one more `| --- |`.
3. Add one more cell `|  |` at the end of every row of that table (it can stay empty).

Example: adding **Reviewer**

```
| ID | Task | Owner | Status | Reviewer |
| --- | --- | --- | --- | --- |
| T10 | Config parser | @teammate_login | 🟡 | @your_login |
```

## How to add a new task

Copy any row, give it the next free ID in its phase (T18, T28…), and fill in the cells.

## Decisions log

| Date | Decision | Who |
| --- | --- | --- |
|  |  |  |
