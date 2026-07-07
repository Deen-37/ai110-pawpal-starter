# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
Today's Schedule
----------------
- Morning walk for Mochi: 30 min (high)
- Feed pets for Mochi: 15 min (high)
- Brush Luna for Luna: 20 min (medium)

Skipped Tasks
-------------
- Playtime for Luna: not enough time
```

## 🧪 Testing PawPal+

Run the full test suite from the `ai110-pawpal-starter` directory:

```bash
python -m pytest
```

### What the tests cover

The suite in `tests/test_pawpal.py` exercises both the base model and the
smarter scheduling features:

- **Priority scoring** — `high`/`medium`/`low`/unknown map to the right scores.
- **Available-minutes budget** — `generate_plan()` schedules only the tasks that
  fit and skips the rest.
- **Task completion** — `mark_complete()` flips the status flag.
- **Pet task assignment** — adding a task grows the pet's care-task list.
- **Sorting correctness** — `sort_by_time()` returns tasks in chronological
  order, including a non-padded hour (`"9:00"`).
- **Recurrence logic** — completing a `daily` task creates a fresh, uncompleted
  next occurrence registered on both the owner and the pet.
- **Conflict detection** — `detect_conflicts()` flags a shared time slot and
  returns an empty list when there are no conflicts.

### Successful test run

```
============================= test session starts =============================
platform win32 -- Python 3.14.5, pytest-9.1.0, pluggy-1.6.0 -- C:\Python314\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Selehadin\Documents\Codepath_New\AI\week5\ai110-pawpal-starter
plugins: anyio-4.14.0
collecting ... collected 8 items

tests/test_pawpal.py::test_priority_score_maps_levels PASSED             [ 12%]
tests/test_pawpal.py::test_scheduler_respects_available_minutes PASSED   [ 25%]
tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 37%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED   [ 50%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 62%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_occurrence PASSED [ 75%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_times PASSED [ 87%]
tests/test_pawpal.py::test_detect_conflicts_empty_when_no_duplicates PASSED [100%]

============================== 8 passed in 0.05s ==============================
```

### Confidence Level

**★★★★☆ (4 / 5)**

All 8 tests pass and cover the happy path of every scheduling feature. I held
back one star because the tests focus on core behavior and don't yet cover
edge cases such as malformed time strings (e.g. `"25:99"` or `"noon"`), weekly
vs. daily recurrence differences, or overlapping durations (the conflict check
only matches exact start times). Those would be the next tests to add.

## 📐 Smarter Scheduling

Beyond the base plan generator, PawPal+ adds several scheduling behaviors. Each
is implemented as a method on the `Scheduler` class (with supporting fields on
`Task`) in `pawpal_system.py`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority sorting | `Scheduler.sort_tasks_by_priority()` | Highest priority first (high=3, medium=2, low=1) |
| Time sorting | `Scheduler.sort_by_time()` | Earliest scheduled `time` first |
| Filtering | `Scheduler.filter_tasks()` | By completion status and/or pet name |
| Conflict detection | `Scheduler.detect_conflicts()` | Warns on tasks sharing a start time |
| Recurring tasks | `Scheduler.complete_task()`, `Task.next_occurrence()`, `Task.is_recurring()` | Daily/weekly tasks respawn on completion |

### Sorting behavior

- **`Scheduler.sort_by_time(tasks)`** returns the tasks ordered from earliest to
  latest. Each task's `"HH:MM"` `time` is converted to minutes-since-midnight
  before comparing, so non-zero-padded hours (e.g. `"9:00"`) still sort
  correctly.
- **`Scheduler.sort_tasks_by_priority(tasks)`** (original) orders tasks from
  highest to lowest priority using `Task.priority_score()`.

Both return new lists via Python's `sorted()` and leave the input untouched.

### Filtering behavior

- **`Scheduler.filter_tasks(tasks, completed=None, pet_name=None)`** returns only
  the tasks that match the given criteria. Both arguments are optional:
  - `completed=True` / `completed=False` — keep only tasks with that status.
  - `pet_name="Luna"` — keep only tasks assigned to that pet.
  - Passing both requires *both* to match; omitting an argument leaves that
    criterion unfiltered.

### Conflict detection logic

- **`Scheduler.detect_conflicts(tasks)`** is a lightweight check that groups
  tasks by their `"HH:MM"` start time and returns a warning string for any slot
  holding two or more tasks — whether they belong to the same pet or different
  pets. It returns an empty list when there are no conflicts, so the caller can
  print a warning **without the program crashing**. Note: it matches exact start
  times only and does not account for overlapping `duration_minutes`.

### Recurring task logic

- **`Task.frequency`** (`"once"`, `"daily"`, or `"weekly"`) marks how a task
  repeats, and **`Task.is_recurring()`** reports whether it repeats at all.
- **`Task.next_occurrence()`** returns a fresh, uncompleted copy of a recurring
  task for its next instance, or `None` for a one-off task.
- **`Scheduler.complete_task(owner, task)`** marks a task complete and, if it
  recurs, automatically creates the next occurrence and registers it on both the
  owner's task list and the assigned pet's care tasks. It returns the new task
  (or `None` if the task does not recur).

## 🎬 Demo Walkthrough

PawPal+ runs two ways: an interactive **Streamlit app** (`app.py`) and a
scripted **CLI demo** (`main.py`). This walkthrough covers the app UI, a typical
workflow, and the Scheduler behaviors you can watch happen.

### Main UI features (what a user can do)

- **Set owner details** — enter the owner's name and the minutes available today
  (this becomes the scheduling budget).
- **Add pets** — name, species, and age; each pet keeps its own care-task list.
- **Add tasks** — title, duration, priority, a **scheduled time**, and how often
  it **repeats** (once / daily / weekly), optionally assigned to a pet.
- **See tasks sorted by time** in a clean table, with a live **conflict warning**
  the moment two tasks share a time slot.
- **Generate a schedule** — the Scheduler fits tasks into the available minutes
  and shows the plan (and any skipped tasks) in chronological order.
- **Filter tasks** — by status (pending / completed) and/or by pet.
- **Complete a task** — marking a daily/weekly task done automatically schedules
  its next occurrence.

### Example workflow

1. Enter the owner (**Jordan**, 75 minutes available today).
2. **Add a pet** — "Mochi" the dog — then click *Add pet*.
3. **Add a task** — "Morning walk", 30 min, high priority, time `08:30`,
   repeats *weekly*, assigned to Mochi — then click *Add task*.
4. Add a few more tasks (feeding at `07:00`, grooming at `13:15`, …). The
   **Current tasks** table re-sorts by time automatically.
5. If two tasks land on the same time, an amber **conflict warning** appears
   naming the clashing tasks and pets.
6. Click **Generate schedule** to see today's plan, ordered earliest-first, with
   a green success banner summarizing how many tasks fit.
7. Use **Filter Tasks** to view just Mochi's pending tasks, then **Complete a
   Task** to mark the walk done and watch its next weekly occurrence appear.

### Key Scheduler behaviors shown

- **Time sorting** (`sort_by_time`) — every task list renders earliest-first.
- **Conflict warnings** (`detect_conflicts`) — same-time bookings are flagged
  without crashing the app.
- **Filtering** (`filter_tasks`) — narrow tasks by status and/or pet.
- **Recurrence** (`complete_task` + `next_occurrence`) — completing a recurring
  task spawns the next one on both the owner and the pet.

### Sample CLI output

Running the scripted demo shows the same behaviors in the terminal:

```bash
python main.py
```

```
Schedule conflict check
-----------------------
Warning: 2 tasks scheduled at 13:15 -> Brush Luna (Luna), Vet check-up (Mochi)

Completing tasks (recurring ones spawn a next occurrence)
---------------------------------------------------------
- Completed Feed pets (daily) - queued next: Feed pets at 07:00
- Completed Morning walk (weekly) - queued next: Morning walk at 08:30
- Completed Brush Luna (once) - no repeat

Tasks in the order they were added
----------------------------------
- 16:00  Playtime
- 08:30  Morning walk
- 13:15  Brush Luna
- 07:00  Feed pets
- 13:15  Vet check-up
- 07:00  Feed pets
- 08:30  Morning walk

Sorted by time (earliest first)
-------------------------------
- 07:00  Feed pets
- 07:00  Feed pets
- 08:30  Morning walk
- 08:30  Morning walk
- 13:15  Brush Luna
- 13:15  Vet check-up
- 16:00  Playtime

Filter: completed tasks only
----------------------------
- 08:30  Morning walk (Morning walk - 30 min, high priority, complete)
- 13:15  Brush Luna (Brush Luna - 20 min, medium priority, complete)
- 07:00  Feed pets (Feed pets - 15 min, high priority, complete)

Filter: incomplete tasks only
-----------------------------
- 16:00  Playtime
- 13:15  Vet check-up
- 07:00  Feed pets
- 08:30  Morning walk

Filter: tasks for Luna
----------------------
- 16:00  Playtime
- 13:15  Brush Luna

Filter: incomplete tasks for Mochi
----------------------------------
- 13:15  Vet check-up
- 07:00  Feed pets
- 08:30  Morning walk
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
