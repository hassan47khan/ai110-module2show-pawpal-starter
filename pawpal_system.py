"""PawPal+ domain model: class skeletons only (no logic yet)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, ...)."""

    id: int
    title: str
    duration_minutes: int
    priority: str = "medium"  # "low" | "medium" | "high"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass

    def edit(
        self,
        title: str | None = None,
        duration_minutes: int | None = None,
        priority: str | None = None,
    ) -> None:
        """Update any of the editable fields."""
        pass


@dataclass
class Pet:
    """A pet and the care tasks that belong to it."""

    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a care task to this pet."""
        pass

    def remove_task(self, task_id: int) -> None:
        """Remove the task with the given id."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return this pet's tasks."""
        pass


@dataclass
class Owner:
    """The pet owner; holds the daily time budget and their pets."""

    name: str
    available_minutes: int = 60
    preferences: dict = field(default_factory=dict)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Register a pet with this owner."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        pass


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
        pass

    def summary(self) -> str:
        """Return a human-readable summary of the plan."""
        pass


class Scheduler:
    """Builds a DailyPlan from an owner's tasks and time budget."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def build_plan(self) -> DailyPlan:
        """Choose and order tasks that fit the owner's available time."""
        pass

    def _rank_tasks(self, tasks: list[Task]) -> list[Task]:
        """Order tasks by priority (and duration as a tiebreaker)."""
        pass

    def _explain(self, task: Task, reason: str) -> str:
        """Produce the human-readable reason for a scheduling decision."""
        pass
