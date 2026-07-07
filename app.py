import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input(
    "Available minutes today", min_value=0, max_value=1440, value=60
)

# Create the Owner once and keep it in the session vault so pets/tasks
# persist across Streamlit re-runs. Keep name/availability in sync each run.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, email="owner@example.com")

owner = st.session_state.owner
owner.name = owner_name
owner.available_minutes = int(available_minutes)

st.divider()

st.subheader("Add a Pet")
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_p2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col_p3:
    pet_age = st.number_input("Age", min_value=0, max_value=40, value=2)

if st.button("Add pet"):
    owner.add_pet(Pet(name=pet_name, species=species, age=int(pet_age)))

if owner.pets:
    st.write("Current pets:")
    for pet in owner.pets:
        st.markdown(f"- {pet.get_profile()}")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")
st.caption("Tasks feed into your scheduler below.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# Optionally attach the task to one of the owner's pets.
pet_choices = ["(none)"] + [pet.name for pet in owner.pets]
assigned_pet = st.selectbox("Assign to pet", pet_choices)

if st.button("Add task"):
    task = Task(title=task_title, duration_minutes=int(duration), priority=priority)
    if assigned_pet != "(none)":
        pet = next(p for p in owner.pets if p.name == assigned_pet)
        pet.add_task(task)  # links task <-> pet
    owner.add_task(task)

if owner.get_tasks():
    st.write("Current tasks:")
    st.table(
        [
            {
                "title": task.title,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "pet": task.pet.name if task.pet else "-",
            }
            for task in owner.get_tasks()
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Runs your Scheduler against the tasks above, within the owner's available time.")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner)

    st.markdown("#### Plan")
    if plan:
        st.text(scheduler.explain_plan(plan))
    else:
        st.warning("No tasks fit within the available time.")

    if scheduler.skipped_tasks:
        st.markdown("#### Skipped (not enough time)")
        st.text("\n".join(task.get_summary() for task in scheduler.skipped_tasks))
