# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

*Three core user actions*

Before drawing any classes, I decided what a user has to be able to do for PawPal+ to be
useful at all. These three actions are the whole point of the app; everything else is support.

1. **Set up the owner and their pet.** A user enters their own name and their pet's basic
   details (name, species, and anything that affects care, like age or energy level), plus
   how much time they realistically have for pet care on a given day. This is the first thing
   a user does, because every plan the app produces is relative to one pet and one owner's
   available time. Without it, the app has nothing to schedule against.

2. **Add and edit pet care tasks.** A user adds the things that actually need to happen —
   a morning walk, feeding, medication, grooming, enrichment — and for each one says how long
   it takes and how important it is. They can come back and change a task's duration or
   priority, or remove a task that no longer applies, because real routines change (a vet adds
   a medication, a walk gets shorter in winter). Duration and priority are required because
   those are the two things the scheduler has to reason about.

3. **Generate and read today's plan.** A user asks for a daily plan and gets back an ordered
   list of tasks that fits inside the time they said they had, with the most important care
   happening first. The plan tells them what to do and in what order, and it explains itself:
   why a task was placed where it was, and why anything was left out. This is the action that
   makes the app an assistant rather than a to-do list — the user brings messy constraints,
   and the app returns a decision plus its reasoning.

Taken together these form the flow of the app: describe the situation (action 1), describe the
work (action 2), then get a recommendation about it (action 3).

*Initial UML design*

My initial UML is a class diagram of six classes, built so that each one maps back to a core
action and no class does more than one job. The three "noun" classes describe the situation,
one class does the thinking, and two classes hold the result.

- **Owner** — the person using the app. Holds their name, the time they have for pet care that
  day (`available_minutes`), a `preferences` dict, and the list of `pets` they own. Its job is
  to be the single source of the daily time budget and to gather every task across all its pets
  (`get_all_tasks`). This backs core action 1.
- **Pet** — one animal. Holds name, species, age, and its own `tasks` list, and can add, remove,
  or return those tasks. Each pet owns its care tasks so that a multi-pet household stays
  organized. This backs core action 2.
- **Task** — one unit of care (a walk, a feeding, a dose of medication). Holds a title, a
  `duration_minutes`, a `priority`, and whether it's `completed`. Duration and priority are the
  two fields the scheduler actually reasons about. It can mark itself complete or edit its
  fields. Also part of core action 2.
- **Scheduler** — the one class with real logic. It reads an Owner, ranks that owner's tasks
  (`_rank_tasks`), and fits as many as it can into the available time, producing a plan
  (`build_plan`) with a reason for each decision (`_explain`). Keeping the algorithm in its own
  class means the data classes stay simple and the scheduling rules can change without touching
  them. This is the heart of core action 3.
- **DailyPlan** — the scheduler's output. Holds the ordered `entries`, the `skipped` tasks with
  the reason each was dropped, and the `total_minutes` used. It knows how to summarize itself
  for display. Separating the plan from the scheduler lets the UI show a result without caring
  how it was produced.
- **PlanEntry** — one line of the plan: a `task`, its `start_time`, and the `reason` it was
  placed there. This is what makes action 3 an explanation and not just a sorted list.

The relationships are deliberately simple: an Owner owns one or more Pets, a Pet has zero or
more Tasks, the Scheduler reads an Owner and creates a DailyPlan, and a DailyPlan contains
PlanEntries that each refer back to a Task. I left out classes I didn't need yet — there is no
Calendar, TimeSlot, or Priority class — because priority is just a string on Task and the day's
time budget is a single number on Owner.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
