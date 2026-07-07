# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
   PawPal+ should have cores action of adding a pet,  assigning a speficif task such as grooming, time schedule
- What classes did you include, and what responsibilities did you assign to each?
    The classes are Owner, Pet, and Task.
    Owner
        Attributes:
            Name
            Email
            Phone number
        Responsibilities:
            Own one or more pets
            View and manage pet tasks
    Pet
        Attributes:
            Name
            Age
             Sex
            Species (Dog, Cat, Bird, etc.)
            Breed
            Weight (optional)
        Responsibilities:
            Belongs to an owner
            Has multiple care tasks
    Task
        Attributes:
            Task name (e.g., Feed, Walk, Groom)
            Date
            Time
            Status (Pending/Completed)
            Notes (optional)
        Responsibilities:
            Assigned to a pet
            Can be marked as completed
    Reminder
        Attributes:
            Reminder date and time
            Notification message
            Repeat frequency (Daily, Weekly, Monthly)
        Responsibilities:
            Linked to a task
        Sends reminders to the owner

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

  The `detect_conflicts` method only flags tasks that share the exact same
  `"HH:MM"` start time. It does no account for overlapping durations. For
  example, a 30-minute "Vet check-up" starting at 13:00 and a "Brush Luna"
  starting at 13:15 actually overlap in real life, but the scheduler stays
  silent because their start strings differ. Detection is a simple
  group-by-start-time check rather than an interval-overlap comparison that
  would use each task's `duration_minutes`.

- Why is that tradeoff reasonable for this scenario?

  The goal was a *lightweight* warning that never crashes the program, not a
  full calendar solver. Grouping by start time is easy to read, runs in a
  single pass, and needs no time math, so it is easy to trust and to extend
  later. For a personal pet-care planner with only a handful of daily tasks,
  identical start times catch the most obvious double-bookings, and the cost of
  a missed partial overlap is low (a person can eyeball the printed schedule).
  If the tool ever managed back-to-back professional grooming appointments, the
  extra complexity of true interval-overlap detection would then be worth it.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

  I used the AI assistant across the whole build: brainstorming the class
  responsibilities, writing each `Scheduler` method incrementally, generating the
  pytest cases, and keeping the docs (README, UML, this reflection) in sync with
  the code. Most work was done one feature at a time — sorting, then filtering,
  then recurrence, then conflict detection — so each change was small enough to
  read and verify before moving on.

- What kinds of prompts or questions were most helpful?

  Narrow, single-responsibility prompts worked best: "add a `sort_by_time`
  method that sorts `HH:MM` strings" produced cleaner results than a vague "make
  the scheduler smarter." Asking *conceptual* questions first ("how does a lambda
  `key` work?") before asking for code helped me actually understand the output
  instead of pasting it blindly.

  **Most effective AI features:**
  - **Reading my existing file for context** — the assistant matched the house
    style (list comprehensions, type hints, docstrings) because it could see
    `sort_tasks_by_priority` before writing `sort_by_time`.
  - **Running code in the terminal to verify** — instead of claiming a method
    worked, it executed `main.py` / `pytest` and showed real output, which caught
    behavior I could see for myself.
  - **Multi-file edits in one step** — the recurrence feature touched `Task`,
    `Scheduler`, and `main.py` together, keeping them consistent.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

  Two examples. First, when adding recurrence the natural first idea was to put
  the "create the next occurrence" logic directly inside `Task.mark_complete()`.
  I rejected that because a `Task` has no reference to the `Owner`, so it
  couldn't register the new instance on the owner's list — it would have needed a
  messy back-reference. Instead we split the responsibility: `Task.next_occurrence()`
  knows *how* to copy itself, and `Scheduler.complete_task()` knows *where* to
  register the copy (owner + pet). That kept `Task` self-contained and the design
  clean. Second, I was offered an upgrade from exact-time conflict checks to full
  interval-overlap detection and chose to keep the lightweight version (see 2b)
  because it matched the scope of the project.

- How did you evaluate or verify what the AI suggested?

  I verified by running, not just reading. Every feature was exercised through
  `main.py` (deliberately adding tasks out of order and at clashing times) and
  through the pytest suite, and I checked the printed output matched what I
  expected — e.g. confirming a non-padded `"9:00"` sorted correctly and that the
  "incomplete tasks for Mochi" filter returned empty once his tasks were done.

**c. Working across phases**

- How did using separate chat sessions for different phases help you stay organized?

  Splitting the work into phase-focused sessions (design/UML → implementation →
  testing → documentation) kept each conversation's context tight. A session that
  was only about the scheduling algorithms didn't get cluttered with UI or README
  chatter, so the assistant's suggestions stayed on-topic and I could find past
  decisions again easily. It also created a natural checkpoint between phases: I
  finished and verified one concern before opening the next, which made it obvious
  when the UML diagram had drifted from the final code and needed a `uml_final.mmd`
  update.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
