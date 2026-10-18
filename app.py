import streamlit as st

# Step 1 — Imports: bring in the backend classes from pawpal_system.py.
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("A pet care planning assistant: add your pets and tasks, then build a daily plan.")

# Step 2 — State management: keep one Owner (and a task-id counter) in session_state
# so the data survives Streamlit's reruns on every interaction. Only create them once.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=60)
if "next_task_id" not in st.session_state:
    st.session_state.next_task_id = 1

owner = st.session_state.owner

st.divider()

# --- Owner settings -----------------------------------------------------------
st.subheader("1. Owner")
owner.name = st.text_input("Owner name", value=owner.name)
owner.available_minutes = st.number_input(
    "Time available today (minutes)", min_value=1, max_value=600, value=owner.available_minutes
)
owner.preferences["start_time"] = st.text_input(
    "Preferred start time (HH:MM)", value=owner.preferences.get("start_time", "08:00")
)

st.divider()

# --- Add a pet ----------------------------------------------------------------
st.subheader("2. Pets")
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    age = st.number_input("Age", min_value=0, max_value=50, value=1)

if st.button("Add pet"):
    if pet_name.strip():
        owner.add_pet(Pet(name=pet_name.strip(), species=species, age=int(age)))
        st.success(f"Added {pet_name}.")
    else:
        st.warning("Give the pet a name first.")

if owner.pets:
    st.write("Your pets:", ", ".join(f"{p.name} ({p.species})" for p in owner.pets))
else:
    st.info("No pets yet. Add one above.")

st.divider()

# --- Add a task to a pet ------------------------------------------------------
st.subheader("3. Tasks")
if owner.pets:
    pet_names = [p.name for p in owner.pets]
    target_name = st.selectbox("Which pet is this task for?", pet_names)

    tcol1, tcol2 = st.columns(2)
    with tcol1:
        task_title = st.text_input("Task description", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        start_time = st.text_input("Time of day (HH:MM, optional)", value="")
    with tcol2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["daily", "weekly"], index=0)

    if st.button("Add task"):
        pet = next(p for p in owner.pets if p.name == target_name)
        pet.add_task(
            Task(
                id=st.session_state.next_task_id,
                description=task_title,
                duration_minutes=int(duration),
                frequency=frequency,
                priority=priority,
                scheduled_time=start_time.strip(),
            )
        )
        st.session_state.next_task_id += 1
        st.success(f"Added '{task_title}' for {target_name}.")

    # Show every task across all pets (via the owner's aggregation method).
    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("All tasks:")
        st.table(
            [
                {
                    "description": t.description,
                    "minutes": t.duration_minutes,
                    "priority": t.priority,
                    "frequency": t.frequency,
                    "done": t.completed,
                }
                for t in all_tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first, then you can add tasks for it.")

st.divider()

# --- Build the schedule -------------------------------------------------------
st.subheader("4. Today's Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)

    # Warn about any tasks the owner booked at the same time of day.
    for message in scheduler.detect_conflicts():
        st.warning(f"⚠️ {message}")

    plan = scheduler.build_plan()

    if plan.entries:
        st.markdown(f"**{len(plan.entries)} task(s) scheduled — {plan.total_minutes} min used**")
        st.table(
            [
                {
                    "Time": entry.start_time,
                    "Task": entry.task.description,
                    "Minutes": entry.task.duration_minutes,
                    "Priority": entry.task.priority,
                    "Why": entry.reason,
                }
                for entry in plan.entries
            ]
        )
    else:
        st.info("Nothing could be scheduled in the time available.")

    if plan.skipped:
        st.markdown("**Left out (not enough time):**")
        st.table(
            [
                {"Task": task.description, "Minutes": task.duration_minutes, "Reason": reason}
                for task, reason in plan.skipped
            ]
        )
