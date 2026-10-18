"""Demo script for PawPal+: exercises sorting, filtering, and scheduling."""

from pawpal_system import Owner, Pet, Scheduler, Task

WIDTH = 56


def banner(title: str) -> None:
    """Print a section header."""
    print()
    print("=" * WIDTH)
    print(f"  {title}")
    print("=" * WIDTH)


def print_tasks(tasks: list[Task]) -> None:
    """Print a list of tasks as a readable table."""
    if not tasks:
        print("  (none)")
        return
    print(f"  {'TIME':<6} {'TASK':<20} {'MIN':>4}  {'DUE':<10} DONE")
    print(f"  {'-' * 6} {'-' * 20} {'-' * 4}  {'-' * 10} {'-' * 4}")
    for t in tasks:
        time = t.scheduled_time or "--:--"
        done = "yes" if t.completed else "no"
        print(
            f"  {time:<6} {t.description:<20} {t.duration_minutes:>4}  "
            f"{t.due_date.isoformat():<10} {done}"
        )


def main() -> None:
    owner = Owner(name="Jordan", available_minutes=90, preferences={"start_time": "07:00"})

    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Add several tasks deliberately OUT OF chronological order.
    mochi.add_task(Task(1, "Evening walk", 30, priority="high", scheduled_time="18:00"))
    mochi.add_task(Task(2, "Breakfast", 10, priority="high", scheduled_time="07:30"))
    luna.add_task(Task(3, "Scoop litter box", 5, priority="medium", scheduled_time="12:15"))
    mochi.add_task(Task(4, "Midday play", 20, priority="medium", scheduled_time="09:05"))
    luna.add_task(
        Task(5, "Brush coat", 15, frequency="weekly", priority="low",
             scheduled_time="08:45")
    )
    # Two tasks at the EXACT same time (different pets) to trigger a conflict.
    luna.add_task(Task(6, "Cat breakfast", 10, priority="high", scheduled_time="07:30"))

    scheduler = Scheduler(owner)

    banner("ALL TASKS (as entered, out of order)")
    print_tasks(owner.get_all_tasks())

    banner("SORTED BY TIME (sort_by_time)")
    print_tasks(scheduler.sort_by_time(owner.get_all_tasks()))

    banner("FILTER: Mochi's tasks only (filter_tasks pet_name='Mochi')")
    print_tasks(scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Mochi")))

    banner("FILTER: still to do (filter_tasks completed=False)")
    print_tasks(scheduler.sort_by_time(scheduler.filter_tasks(completed=False)))

    banner("CONFLICT CHECK (detect_conflicts)")
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for message in conflicts:
            print(f"  WARNING: {message}")
    else:
        print("  No conflicts found.")

    banner("RECURRING TASK (complete a weekly task -> next occurrence)")
    brush = next(t for t in owner.get_all_tasks() if t.description == "Brush coat")
    print(f"  Completing '{brush.description}' due {brush.due_date.isoformat()} (weekly)...")
    follow_up = scheduler.mark_task_complete(brush)
    if follow_up is not None:
        print(
            f"  -> Auto-created next '{follow_up.description}' "
            f"due {follow_up.due_date.isoformat()}"
        )
    print_tasks(scheduler.sort_by_time(scheduler.filter_tasks(pet_name="Luna")))

    banner("TODAY'S PLAN (build_plan, by priority within 90 min)")
    print(Scheduler(owner).build_plan().summary())
    print()


if __name__ == "__main__":
    main()
