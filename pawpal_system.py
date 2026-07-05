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
    is_required: bool = True
    completed: bool = False
    pet: Pet | None = None

    def assign_to_pet(self, pet: Pet) -> None:
        """Associate this task with the given pet."""
        self.pet = pet

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

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

    def explain_plan(self, plan: list[Task]) -> str:
        """Return a newline-separated summary of the scheduled tasks."""
        if not plan:
            return "No tasks were scheduled."

        return "\n".join(task.get_summary() for task in plan)
