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

# Add tasks for Mochi
mochi.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", category="walk"))
mochi.add_task(Task(title="Breakfast + supplement", duration_minutes=10, priority="high", category="feeding"))
mochi.add_task(Task(title="Play fetch", duration_minutes=20, priority="medium", category="enrichment"))

# Add tasks for Whiskers
whiskers.add_task(Task(title="Feed breakfast", duration_minutes=10, priority="high", category="feeding"))
whiskers.add_task(Task(title="Thyroid medication", duration_minutes=5, priority="high", category="meds"))
whiskers.add_task(Task(title="Brush fur", duration_minutes=15, priority="low", category="grooming"))

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
    print()
