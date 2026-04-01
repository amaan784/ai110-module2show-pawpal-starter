from pawpal_system import Owner, Pet, Task, Scheduler, today


# Create an owner
owner = Owner(name="Jordan", available_minutes=90)

# Create two pets
mochi = Pet(name="Mochi", species="dog", age=3)
mochi.add_need("joint supplement with breakfast")

whiskers = Pet(name="Whiskers", species="cat", age=7)
whiskers.add_need("daily thyroid medication")

owner.add_pet(mochi)
owner.add_pet(whiskers)

# Add tasks for Mochi (out of time order, with scheduled times)
mochi.add_task(Task(title="Play fetch", duration_minutes=20, priority="medium", category="enrichment", scheduled_time="17:00"))
mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", category="walk", scheduled_time="07:00", frequency="daily"))
mochi.add_task(Task(title="Breakfast + supplement", duration_minutes=10, priority="high", category="feeding", scheduled_time="08:00", frequency="daily"))

# Add tasks for Whiskers
whiskers.add_task(Task(title="Brush fur", duration_minutes=15, priority="low", category="grooming", scheduled_time="18:00"))
whiskers.add_task(Task(title="Thyroid medication", duration_minutes=5, priority="high", category="meds", scheduled_time="07:30", frequency="daily"))
whiskers.add_task(Task(title="Feed breakfast", duration_minutes=10, priority="high", category="feeding", scheduled_time="08:00", frequency="daily"))

# Generate and display schedule for each pet
for pet in owner.pets:
    print(pet.get_summary())
    print()

    scheduler = Scheduler(owner=owner, pet=pet, date=today())
    schedule = scheduler.generate_schedule()

    print(schedule.display())
    print()
    print(scheduler.explain(schedule))
    print()

# --- Demo: Sort by time ---
print("=" * 45)
print("SORTING BY TIME (Mochi's tasks)")
print("=" * 45)
scheduler = Scheduler(owner=owner, pet=mochi, date=today())
sorted_tasks = scheduler.sort_by_time()
for t in sorted_tasks:
    print(f"  {t.scheduled_time or 'N/A':>5}  {t}")
print()

# --- Demo: Filtering ---
print("=" * 45)
print("FILTERING (all owner tasks, pending only)")
print("=" * 45)
all_scheduler = Scheduler(owner=owner, pet=mochi, available_tasks=owner.get_all_tasks(), date=today())
pending = all_scheduler.filter_tasks(completed=False)
for t in pending:
    print(f"  {t}")
print()

# Filter by pet name
print("Filtering by pet name (Whiskers only):")
whiskers_tasks = all_scheduler.filter_tasks(pet_name="Whiskers")
for t in whiskers_tasks:
    print(f"  {t}")
print()

# --- Demo: Conflict detection ---
print("=" * 45)
print("CONFLICT DETECTION")
print("=" * 45)
# Mochi already has "Breakfast + supplement" at 08:00 — add another at the same time
mochi.add_task(Task(title="Grooming session", duration_minutes=15, priority="low", category="grooming", scheduled_time="08:00"))
scheduler = Scheduler(owner=owner, pet=mochi, date=today())
conflicts = scheduler.detect_conflicts()
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found.")
# Remove the conflicting task so it doesn't affect later demos
mochi.tasks.pop()
print()

# --- Demo: Recurring tasks ---
print("=" * 45)
print("RECURRING TASKS")
print("=" * 45)
walk = mochi.tasks[1]  # Morning walk (daily)
print(f"Before: {walk} | due: {walk.due_date} | freq: {walk.frequency}")
print(f"Mochi task count: {len(mochi.tasks)}")

scheduler = Scheduler(owner=owner, pet=mochi, date=today())
scheduler.mark_task_complete(walk)

print(f"After:  {walk} | due: {walk.due_date} | freq: {walk.frequency}")
print(f"Mochi task count: {len(mochi.tasks)}")
new_walk = mochi.tasks[-1]
print(f"New task: {new_walk} | due: {new_walk.due_date}")
