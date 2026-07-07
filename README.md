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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
