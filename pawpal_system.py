from dataclasses import dataclass, field
from datetime import date

VALID_PRIORITIES = ("low", "medium", "high")
PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    category: str = "general"
    completed: bool = False

    def __post_init__(self):
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {VALID_PRIORITIES}, got '{self.priority}'")

    def is_high_priority(self) -> bool:
        return self.priority == "high"

    def __str__(self) -> str:
        status = "done" if self.completed else "pending"
        return f"[{self.priority.upper()}] {self.title} ({self.duration_minutes} min, {self.category}) - {status}"


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    special_needs: list = field(default_factory=list)
    tasks: list = field(default_factory=list)

    def add_need(self, need: str) -> None:
        self.special_needs.append(need)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def get_summary(self) -> str:
        needs = ", ".join(self.special_needs) if self.special_needs else "none"
        return f"{self.name} ({self.species}, age {self.age}) — special needs: {needs}"


@dataclass
class Owner:
    name: str
    available_minutes: int = 60
    preferences: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)

    def set_preferences(self, prefs: dict) -> None:
        self.preferences.update(prefs)

    def get_available_time(self) -> int:
        return self.available_minutes

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Schedule:
    date: str
    owner: Owner
    pet: Pet
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks.remove(task)

    def get_total_duration(self) -> int:
        return sum(t.duration_minutes for t in self.tasks)

    def display(self) -> str:
        lines = []
        lines.append(f"=== Schedule for {self.pet.name} ({self.date}) ===")
        lines.append(f"Owner: {self.owner.name} | Available: {self.owner.available_minutes} min")
        lines.append("-" * 45)
        if not self.tasks:
            lines.append("  No tasks scheduled.")
        else:
            for i, task in enumerate(self.tasks, 1):
                lines.append(f"  {i}. {task}")
        lines.append("-" * 45)
        lines.append(f"Total: {self.get_total_duration()} min")
        return "\n".join(lines)


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, available_tasks: list = None, time_limit: int = None, date: str = ""):
        self.owner = owner
        self.pet = pet
        self.available_tasks = available_tasks if available_tasks is not None else pet.tasks
        self.time_limit = time_limit if time_limit is not None else owner.available_minutes
        self.date = date or str(date if date else today())

    def generate_schedule(self) -> Schedule:
        sorted_tasks = sorted(
            self.available_tasks,
            key=lambda t: PRIORITY_RANK.get(t.priority, 0),
            reverse=True,
        )
        schedule = Schedule(date=self.date, owner=self.owner, pet=self.pet)
        remaining = self.time_limit
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                schedule.add_task(task)
                remaining -= task.duration_minutes
        return schedule

    def explain(self, schedule: Schedule) -> str:
        lines = []
        lines.append("Schedule reasoning:")
        skipped = [t for t in self.available_tasks if t not in schedule.tasks]
        for task in schedule.tasks:
            lines.append(f"  + {task.title}: included (priority={task.priority}, {task.duration_minutes} min)")
        for task in skipped:
            lines.append(f"  - {task.title}: skipped (not enough time remaining)")
        lines.append(f"Time used: {schedule.get_total_duration()} / {self.time_limit} min")
        return "\n".join(lines)


def today() -> str:
    return str(date.today())
