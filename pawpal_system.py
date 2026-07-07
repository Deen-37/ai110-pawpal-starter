from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Owner:
    name: str
    email: str
    available_minutes: int = 60
    pets: list[Pet] = field(default_factory=list)
    tasks: list[Task] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def add_task(self, task: Task) -> None:
        """Add a care task to this owner's task list."""
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> None:
        """Remove all tasks matching the given title from this owner."""
        self.tasks = [task for task in self.tasks if task.title != task_title]

    def get_tasks(self) -> list[Task]:
        """Return this owner's list of tasks."""
        return self.tasks


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    care_tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assign a task to this pet and add it to the pet's care tasks."""
        task.assign_to_pet(self)
        self.care_tasks.append(task)

    def get_profile(self) -> str:
        """Return a short human-readable description of this pet."""
        return f"{self.name} is a {self.age}-year-old {self.species}."


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    time: str = "00:00"
    frequency: str = "once"
    is_required: bool = True
    completed: bool = False
    pet: Pet | None = None

    def assign_to_pet(self, pet: Pet) -> None:
        """Associate this task with the given pet."""
        self.pet = pet

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def is_recurring(self) -> bool:
        """Return True if this task repeats on a daily or weekly schedule."""
        return self.frequency.lower() in ("daily", "weekly")

    def next_occurrence(self) -> Task | None:
        """Return a fresh, uncompleted copy of this task for its next occurrence.

        Returns None for one-off tasks. The copy keeps the same details and pet
        but resets ``completed`` to False so it represents the upcoming instance.
        """
        if not self.is_recurring():
            return None
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            time=self.time,
            frequency=self.frequency,
            is_required=self.is_required,
            pet=self.pet,
        )

    def priority_score(self) -> int:
        """Return the numeric priority score (low=1, medium=2, high=3, else 0)."""
        scores = {"low": 1, "medium": 2, "high": 3}
        return scores.get(self.priority.lower(), 0)

    def get_summary(self) -> str:
        """Return a one-line summary of the task's details and status."""
        status = "complete" if self.completed else "incomplete"
        return f"{self.title} - {self.duration_minutes} min, {self.priority} priority, {status}"


@dataclass
class Scheduler:
    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)

    def generate_plan(self, owner: Owner) -> list[Task]:
        """Build a schedule of the owner's tasks that fits their available time."""
        self.scheduled_tasks = []
        self.skipped_tasks = []

        remaining_minutes = owner.available_minutes
        sorted_tasks = self.sort_tasks_by_priority(owner.get_tasks())

        for task in sorted_tasks:
            if task.duration_minutes <= remaining_minutes:
                self.scheduled_tasks.append(task)
                remaining_minutes -= task.duration_minutes
            else:
                self.skipped_tasks.append(task)

        return self.scheduled_tasks

    def sort_tasks_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Return the tasks sorted from highest to lowest priority."""
        return sorted(tasks, key=lambda task: task.priority_score(), reverse=True)

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return the tasks sorted from earliest to latest scheduled time.

        Each task's "HH:MM" time is converted to minutes-since-midnight before
        comparing, so non-padded hours (e.g. "9:00") still sort correctly.
        """
        def to_minutes(task: Task) -> int:
            hours, minutes = task.time.split(":")
            return int(hours) * 60 + int(minutes)

        return sorted(tasks, key=to_minutes)

    def filter_tasks(
        self,
        tasks: list[Task],
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """Return the tasks matching the given completion status and/or pet name.

        Each criterion is optional: pass ``completed`` to keep only tasks with
        that status, ``pet_name`` to keep only tasks assigned to that pet, or
        both to require both. Omitting a criterion leaves it unfiltered.
        """
        return [
            task
            for task in tasks
            if (completed is None or task.completed == completed)
            and (pet_name is None or (task.pet is not None and task.pet.name == pet_name))
        ]

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return a warning for each time slot holding more than one task.

        Lightweight check: tasks are grouped by their scheduled "HH:MM" time,
        and any slot with two or more tasks is flagged, whether the tasks belong
        to the same pet or different pets. Returns an empty list when there are
        no conflicts, so callers can warn without the program crashing.
        """
        by_time: dict[str, list[Task]] = {}
        for task in tasks:
            by_time.setdefault(task.time, []).append(task)

        warnings: list[str] = []
        for time, slot_tasks in sorted(by_time.items()):
            if len(slot_tasks) > 1:
                details = ", ".join(
                    f"{t.title} ({t.pet.name if t.pet else 'no pet'})"
                    for t in slot_tasks
                )
                warnings.append(f"Warning: {len(slot_tasks)} tasks scheduled at {time} -> {details}")
        return warnings

    def complete_task(self, owner: Owner, task: Task) -> Task | None:
        """Mark a task complete and, if it recurs, register its next occurrence.

        The new instance is added to the owner's task list and, when the task is
        assigned to a pet, to that pet's care tasks. Returns the newly created
        task, or None if the task does not recur.
        """
        task.mark_complete()

        next_task = task.next_occurrence()
        if next_task is None:
            return None

        owner.add_task(next_task)
        if next_task.pet is not None:
            next_task.pet.add_task(next_task)

        return next_task

    def explain_plan(self, plan: list[Task]) -> str:
        """Return a newline-separated summary of the scheduled tasks."""
        if not plan:
            return "No tasks were scheduled."

        return "\n".join(task.get_summary() for task in plan)
