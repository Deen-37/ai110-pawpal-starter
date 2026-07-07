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
  `"HH:MM"` start time. It does **not** account for overlapping durations. For
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
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
