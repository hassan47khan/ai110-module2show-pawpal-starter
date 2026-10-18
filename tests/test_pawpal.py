"""Tests for PawPal+ core behaviors."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_sets_task_to_done():
    """mark_complete() should flip a task's status to completed."""
    task = Task(1, "Morning walk", 30, priority="high")
    assert task.completed is False  # starts incomplete

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    """Adding a task to a pet should grow its task list by one."""
    pet = Pet(name="Mochi", species="dog")
    assert len(pet.get_tasks()) == 0  # starts with no tasks

    pet.add_task(Task(1, "Feeding", 10, priority="high"))

    assert len(pet.get_tasks()) == 1


def test_sort_by_time_returns_chronological_order():
    """sort_by_time() should order tasks by their HH:MM scheduled_time."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    # Added out of order on purpose.
    pet.add_task(Task(1, "Evening", 10, scheduled_time="18:00"))
    pet.add_task(Task(2, "Morning", 10, scheduled_time="07:30"))
    pet.add_task(Task(3, "Midday", 10, scheduled_time="12:15"))

    ordered = Scheduler(owner).sort_by_time(pet.get_tasks())

    times = [t.scheduled_time for t in ordered]
    assert times == ["07:30", "12:15", "18:00"]


def test_completing_daily_task_creates_next_day_occurrence():
    """Completing a daily task should spawn a new task due the next day."""
    pet = Pet(name="Mochi", species="dog")
    original = Task(
        1, "Walk", 30, frequency="daily", due_date=date(2026, 1, 1)
    )
    pet.add_task(original)

    follow_up = pet.complete_task(original.id)

    assert original.completed is True  # the original is now done
    assert follow_up is not None  # a recurrence was created
    assert follow_up.completed is False  # the new one is still pending
    assert follow_up.due_date == date(2026, 1, 2)  # one day later
    assert len(pet.get_tasks()) == 2  # original + new occurrence


def test_detect_conflicts_flags_duplicate_times():
    """detect_conflicts() should report two tasks sharing a scheduled_time."""
    owner = Owner(name="Jordan")
    dog = Pet(name="Mochi", species="dog")
    cat = Pet(name="Luna", species="cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task(1, "Dog breakfast", 10, scheduled_time="07:30"))
    cat.add_task(Task(2, "Cat breakfast", 10, scheduled_time="07:30"))
    cat.add_task(Task(3, "Nap", 5, scheduled_time="09:00"))  # no conflict

    conflicts = Scheduler(owner).detect_conflicts()

    assert len(conflicts) == 1  # only the 07:30 slot clashes
    assert "07:30" in conflicts[0]


def test_empty_schedule_has_no_tasks_or_conflicts():
    """An owner with no pets/tasks should schedule nothing and flag nothing."""
    scheduler = Scheduler(Owner(name="Jordan"))

    plan = scheduler.build_plan()

    assert plan.entries == []  # nothing to schedule
    assert scheduler.detect_conflicts() == []  # nothing can conflict
