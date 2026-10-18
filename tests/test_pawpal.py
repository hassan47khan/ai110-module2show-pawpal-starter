"""Tests for PawPal+ core behaviors."""

from pawpal_system import Pet, Task


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
