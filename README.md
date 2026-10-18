# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
