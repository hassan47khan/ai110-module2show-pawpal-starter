"""Demo script for PawPal+: builds a sample day and prints the schedule."""

from pawpal_system import DailyPlan, Owner, Pet, Scheduler, Task


def print_schedule(owner: Owner, plan: DailyPlan) -> None:
    """Print the day's plan to the terminal in a clear, readable layout."""
    width = 48
    print()
    print("=" * width)
    print(f"  TODAY'S SCHEDULE FOR {owner.name.upper()}".ljust(width))
    print(f"  Time available: {owner.available_minutes} min".ljust(width))
    print("=" * width)

    if plan.entries:
        for entry in plan.entries:
            task = entry.task
            print(f"  {entry.start_time}  {task.description}")
            print(
                f"          {task.duration_minutes} min"
                f"  |  {task.priority} priority"
                f"  |  why: {entry.reason}"
            )
    else:
        print("  Nothing could be scheduled today.")

    print("-" * width)
    print(f"  Scheduled: {len(plan.entries)} task(s), {plan.total_minutes} min used")

    if plan.skipped:
        print()
        print("  Left out (not enough time):")
        for task, reason in plan.skipped:
            print(f"    - {task.description} ({task.duration_minutes} min): {reason}")

    print("=" * width)
    print()


def main() -> None:
    # One owner with a daily time budget and a preferred start time.
    owner = Owner(
        name="Jordan",
        available_minutes=75,
        preferences={"start_time": "07:30"},
    )

    # Two pets.
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # At least three tasks, each with a different duration ("time").
    mochi.add_task(Task(1, "Morning walk", 30, priority="high"))
    mochi.add_task(Task(2, "Breakfast", 10, priority="high"))
    mochi.add_task(Task(3, "Fetch / training", 20, priority="medium"))
    luna.add_task(Task(4, "Scoop litter box", 5, priority="medium"))
    luna.add_task(Task(5, "Brush coat", 15, frequency="weekly", priority="low"))

    # Build and print the plan.
    plan = Scheduler(owner).build_plan()
    print_schedule(owner, plan)


if __name__ == "__main__":
    main()
