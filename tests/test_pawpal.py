from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete():
    task = Task(title="Morning walk", duration_minutes=30, priority="high", category="walk")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet():
    pet = Pet(name="Mochi", species="dog", age=3)
    assert len(pet.tasks) == 0
    pet.add_task(Task(title="Feed breakfast", duration_minutes=10, priority="high", category="feeding"))
    assert len(pet.tasks) == 1


def test_sort_by_time():
    owner = Owner(name="Jordan", available_minutes=90)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Evening play", duration_minutes=20, priority="medium", scheduled_time="17:00"))
    pet.add_task(Task(title="Morning walk", duration_minutes=30, priority="high", scheduled_time="07:00"))
    pet.add_task(Task(title="Lunch feed", duration_minutes=10, priority="high", scheduled_time="12:00"))
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-04-01")
    sorted_tasks = scheduler.sort_by_time()
    assert [t.scheduled_time for t in sorted_tasks] == ["07:00", "12:00", "17:00"]


def test_recurring_daily_task():
    pet = Pet(name="Mochi", species="dog")
    task = Task(title="Morning walk", duration_minutes=30, priority="high", frequency="daily", due_date="2026-04-01")
    pet.add_task(task)
    owner = Owner(name="Jordan", available_minutes=90)
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-04-01")
    scheduler.mark_task_complete(task)
    assert task.completed is True
    assert len(pet.tasks) == 2
    new_task = pet.tasks[-1]
    assert new_task.completed is False
    assert new_task.due_date == "2026-04-02"


def test_conflict_detection():
    owner = Owner(name="Jordan", available_minutes=90)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Breakfast", duration_minutes=10, priority="high", scheduled_time="08:00"))
    pet.add_task(Task(title="Grooming", duration_minutes=15, priority="low", scheduled_time="08:00"))
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-04-01")
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "08:00" in conflicts[0]


def test_no_conflicts_when_times_differ():
    owner = Owner(name="Jordan", available_minutes=90)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=30, priority="high", scheduled_time="07:00"))
    pet.add_task(Task(title="Feed", duration_minutes=10, priority="high", scheduled_time="08:00"))
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-04-01")
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 0


def test_schedule_respects_time_limit():
    owner = Owner(name="Jordan", available_minutes=30)
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=25, priority="high", scheduled_time="07:00"))
    pet.add_task(Task(title="Play", duration_minutes=20, priority="medium", scheduled_time="08:00"))
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-04-01")
    schedule = scheduler.generate_schedule()
    assert len(schedule.tasks) == 1
    assert schedule.tasks[0].title == "Walk"


def test_schedule_empty_pet():
    owner = Owner(name="Jordan", available_minutes=60)
    pet = Pet(name="Ghost", species="cat")
    scheduler = Scheduler(owner=owner, pet=pet, date="2026-04-01")
    schedule = scheduler.generate_schedule()
    assert len(schedule.tasks) == 0
    assert schedule.get_total_duration() == 0
