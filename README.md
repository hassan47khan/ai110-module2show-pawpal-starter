# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

- **Owner / pet / task model** — one owner manages multiple pets, each with its own care tasks (description, duration, priority, frequency, optional time of day).
- **Priority-based daily plan** — `build_plan()` ranks tasks by priority (shorter duration breaks ties) and fits as many as possible into the owner's available minutes, assigning each a start time.
- **Explainable output** — every scheduled task comes with a reason, and tasks that don't fit are listed with why they were skipped.
- **Sort by time** — `sort_by_time()` returns tasks in chronological order by their `"HH:MM"` time.
- **Filtering** — `filter_tasks()` narrows tasks by completion status, by pet, or both.
- **Conflict warnings** — `detect_conflicts()` flags any two tasks booked at the same time (same or different pets) without crashing.
- **Daily / weekly recurrence** — completing a recurring task auto-creates its next occurrence, advancing the due date by one day or one week.
- **Streamlit UI** — add pets and tasks, then generate a formatted schedule with conflict warnings in the browser.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🧩 Implementation Summary

PawPal+ is built from four core classes that hand work to each other in one direction, so no
class has to know how the others do their jobs:

- **`Task`** is one care activity — a description, how long it takes (`duration_minutes`), how
  often it recurs (`frequency`), a priority, and whether it's completed. It can mark itself done
  or edit its own fields.
- **`Pet`** holds a pet's details and its own list of `Task` objects, with methods to add,
  remove, and return them.
- **`Owner`** manages one or more `Pet` objects and exposes `get_all_tasks()`, which gathers
  every pet's tasks into a single list. This is the one place the whole day's work is assembled.
- **`Scheduler`** is the brain. It reads tasks **only** through `owner.get_all_tasks()` (never
  from a pet directly), ranks them by priority with shorter tasks breaking ties, and fits as many
  as possible into the owner's `available_minutes`. It returns a `DailyPlan` of `PlanEntry`
  objects — each a task, a start time, and the reason it was placed — plus a list of tasks that
  were skipped and why.

In short: `Owner` owns `Pet`s, each `Pet` owns `Task`s, and the `Scheduler` reads the owner's
aggregated tasks to produce an explainable `DailyPlan`. See [main.py](main.py) for a runnable
demo and `tests/test_pawpal.py` for the behavior tests.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest
```

The tests live in `tests/test_pawpal.py` and cover:

- **Task completion** — `mark_complete()` flips a task's status to done.
- **Task addition** — adding a task to a pet grows its task list.
- **Sorting correctness** — `sort_by_time()` returns tasks in chronological order.
- **Recurrence logic** — completing a daily task creates a new task due the next day.
- **Conflict detection** — `detect_conflicts()` flags two tasks at the same time.
- **Empty-schedule edge case** — an owner with no pets schedules nothing and flags nothing.

Sample test output:

```text
# Paste your pytest output here
```

**Confidence Level (1–5 ⭐):** <!-- e.g. ⭐⭐⭐⭐ — explain in a sentence why -->

## 📐 Smarter Scheduling

Beyond the basic daily plan, PawPal+ adds four scheduling behaviors:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks chronologically by their `"HH:MM"` `scheduled_time`; tasks with no time sort to the end. `build_plan()` separately orders by priority (then shorter duration). |
| Filtering | `Scheduler.filter_tasks(completed, pet_name)` | Returns tasks filtered by completion status, by pet name, or both; no filters returns everything. |
| Conflict detection | `Scheduler.detect_conflicts()` | Groups tasks by `scheduled_time` and returns a warning string for any slot shared by two or more tasks (same or different pets). Returns a list, never raises. |
| Recurring tasks | `Pet.complete_task()` / `Scheduler.mark_task_complete()` | Completing a `"daily"` or `"weekly"` task auto-creates its next occurrence, advancing `due_date` by `timedelta(days=1)` or `timedelta(weeks=1)`. |

## 📸 Demo Walkthrough

Follow these steps to run and demo the app end to end.

**Workflow steps:**

1. <!-- e.g. Launch the app: `streamlit run app.py` -->
2. <!-- e.g. Set the owner name and available minutes for the day -->
3. <!-- e.g. Add two pets -->
4. <!-- e.g. Add several tasks, including two at the same time of day -->
5. <!-- e.g. Click "Generate schedule" and point out the conflict warning -->
6. <!-- e.g. Read the resulting plan table and the "left out" list -->

**CLI demo (`python main.py`):**

```text
# Paste the terminal output of `python main.py` here
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
