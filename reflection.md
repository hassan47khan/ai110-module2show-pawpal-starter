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

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

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
