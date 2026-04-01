import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler, today

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown("A pet care planning assistant that helps you stay on top of daily tasks.")

# --- Session State Initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = None
if "selected_pet" not in st.session_state:
    st.session_state.selected_pet = None

# --- Owner Setup ---
st.subheader("Owner Info")

if st.session_state.owner is None:
    owner_name = st.text_input("Your name", value="Jordan")
    available = st.number_input("Available minutes today", min_value=10, max_value=480, value=90)
    if st.button("Set Owner"):
        st.session_state.owner = Owner(name=owner_name, available_minutes=int(available))
        st.rerun()
else:
    owner = st.session_state.owner
    st.success(f"Owner: **{owner.name}** | Available: **{owner.available_minutes} min**")

# --- Add Pets ---
if st.session_state.owner is not None:
    owner = st.session_state.owner
    st.divider()
    st.subheader("Pets")

    with st.form("add_pet_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            pet_name = st.text_input("Pet name", value="Mochi")
        with col2:
            species = st.selectbox("Species", ["dog", "cat", "other"])
        with col3:
            age = st.number_input("Age", min_value=0, max_value=30, value=3)
        if st.form_submit_button("Add Pet"):
            new_pet = Pet(name=pet_name, species=species, age=age)
            owner.add_pet(new_pet)
            st.rerun()

    if owner.pets:
        for pet in owner.pets:
            st.write(f"{pet.get_summary()}")

        pet_names = [p.name for p in owner.pets]
        selected = st.selectbox("Select a pet to manage tasks", pet_names)
        st.session_state.selected_pet = next(p for p in owner.pets if p.name == selected)
    else:
        st.info("No pets yet. Add one above.")

# --- Add Tasks to Selected Pet ---
if st.session_state.selected_pet is not None:
    pet = st.session_state.selected_pet
    owner = st.session_state.owner
    st.divider()
    st.subheader(f"Tasks for {pet.name}")

    with st.form("add_task_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            task_title = st.text_input("Task title", value="Morning walk")
        with col2:
            duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
        with col3:
            priority = st.selectbox("Priority", ["high", "medium", "low"])
        col4, col5 = st.columns(2)
        with col4:
            category = st.selectbox("Category", ["walk", "feeding", "meds", "enrichment", "grooming", "general"])
        with col5:
            scheduled_time = st.text_input("Scheduled time (HH:MM)", value="")
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        if st.form_submit_button("Add Task"):
            pet.add_task(Task(
                title=task_title, duration_minutes=int(duration), priority=priority,
                category=category, scheduled_time=scheduled_time, frequency=frequency,
            ))
            st.rerun()

    if pet.tasks:
        scheduler = Scheduler(owner=owner, pet=pet, date=today())
        sorted_tasks = scheduler.sort_by_time()
        st.table([
            {
                "Time": t.scheduled_time or "N/A",
                "Task": t.title,
                "Duration": f"{t.duration_minutes} min",
                "Priority": t.priority,
                "Category": t.category,
                "Frequency": t.frequency,
            }
            for t in sorted_tasks
        ])

        # Show conflict warnings
        conflicts = scheduler.detect_conflicts()
        for warning in conflicts:
            st.warning(f"Scheduling conflict: {warning}")
    else:
        st.info("No tasks yet. Add one above.")

    # --- Generate Schedule ---
    st.divider()
    st.subheader("Generate Schedule")

    if st.button("Build Today's Schedule"):
        if not pet.tasks:
            st.warning("Add some tasks first!")
        else:
            scheduler = Scheduler(owner=owner, pet=pet, date=today())
            schedule = scheduler.generate_schedule()

            st.code(schedule.display())
            st.markdown("### Reasoning")
            st.code(scheduler.explain(schedule))
