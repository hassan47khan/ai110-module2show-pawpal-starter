"""PawPal+ domain model and scheduling logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

# How important each priority is when ranking (lower sorts first).
_PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    """A single pet care activity (walk, feeding, meds, ...)."""

    id: int
    description: str
    duration_minutes: int  # how long the task takes ("time")
    frequency: str = "daily"  # e.g. "daily", "weekly"
    priority: str = "medium"  # "low" | "medium" | "high"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def edit(
        self,
        description: str | None = None,
        duration_minutes: int | None = None,
        frequency: str | None = None,
        priority: str | None = None,
    ) -> None:
        """Update any field that is given; leave the rest unchanged."""
        if description is not None:
            self.description = description
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if frequency is not None:
            self.frequency = frequency
        if priority is not None:
            self.priority = priority


@dataclass
class Pet:
    """A pet and the care tasks that belong to it."""

    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        """Remove the task with the given id (no error if it isn't there)."""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        return self.tasks


@dataclass
class Owner:
    """The pet owner; holds the daily time budget and their pets."""

    name: str
    available_minutes: int = 60
    preferences: dict = field(default_factory=dict)  # e.g. {"start_time": "08:00"}
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets, in one list."""
        all_tasks: list[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


@dataclass
class PlanEntry:
    """One scheduled task: what, when, and why."""

    task: Task
    start_time: str
    reason: str


@dataclass
class DailyPlan:
    """The scheduler's output: scheduled entries plus what was left out."""

    entries: list[PlanEntry] = field(default_factory=list)
    skipped: list[tuple[Task, str]] = field(default_factory=list)  # (task, reason)
    total_minutes: int = 0

    def add_entry(self, entry: PlanEntry) -> None:
        """Append a scheduled entry and update the running total."""
        self.entries.append(entry)
        self.total_minutes += entry.task.duration_minutes

    def summary(self) -> str:
        """Return a human-readable summary of the plan."""
        lines = [f"Daily plan ({self.total_minutes} min scheduled):"]
        if self.entries:
            for entry in self.entries:
                lines.append(
                    f"  {entry.start_time} - {entry.task.description} "
                    f"({entry.task.duration_minutes} min) [{entry.reason}]"
                )
        else:
            lines.append("  (nothing scheduled)")
        if self.skipped:
            lines.append("Not scheduled:")
            for task, reason in self.skipped:
                lines.append(f"  {task.description} - {reason}")
        return "\n".join(lines)


class Scheduler:
    """Builds a DailyPlan from an owner's tasks and time budget."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler bound to one owner."""
        self.owner = owner

    def build_plan(self) -> DailyPlan:
        """Choose and order tasks that fit the owner's available time.

        Tasks are read through the owner's aggregation method so the scheduler
        never reaches into a single pet directly.
        """
        plan = DailyPlan()

        # Only unfinished tasks need scheduling; completed ones are done.
        pending = [t for t in self.owner.get_all_tasks() if not t.completed]
        ranked = self._rank_tasks(pending)

        remaining = self.owner.available_minutes
        start_str = self.owner.preferences.get("start_time", "08:00")
        clock = datetime.strptime(start_str, "%H:%M")

        for task in ranked:
            if task.duration_minutes <= remaining:
                reason = self._explain(task, scheduled=True, remaining=remaining)
                plan.add_entry(PlanEntry(task, clock.strftime("%H:%M"), reason))
                clock += timedelta(minutes=task.duration_minutes)
                remaining -= task.duration_minutes
            else:
                reason = self._explain(task, scheduled=False, remaining=remaining)
                plan.skipped.append((task, reason))

        return plan

    def _rank_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority, then by shorter duration as a tiebreaker."""
        return sorted(
            tasks,
            key=lambda t: (_PRIORITY_RANK.get(t.priority, 1), t.duration_minutes),
        )

    def _explain(self, task: Task, scheduled: bool, remaining: int) -> str:
        """Produce the human-readable reason for a scheduling decision."""
        if scheduled:
            return f"{task.priority} priority"
        return f"needs {task.duration_minutes} min but only {remaining} min left"
