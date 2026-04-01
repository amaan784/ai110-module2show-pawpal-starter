from pawpal_system import Task, Pet


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
