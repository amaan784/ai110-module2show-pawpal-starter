from dataclasses import dataclass, field

VALID_PRIORITIES = ("low", "medium", "high")


@dataclass
class Owner:
    name: str
    available_minutes: int = 60
    preferences: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)

    def set_preferences(self, prefs: dict) -> None:
        pass

    def get_available_time(self) -> int:
        pass

    def add_pet(self, pet) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    special_needs: list = field(default_factory=list)

    def add_need(self, need: str) -> None:
        pass

    def get_summary(self) -> str:
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    category: str = "general"

    def is_high_priority(self) -> bool:
        pass

    def __str__(self) -> str:
        pass


@dataclass
class Schedule:
    date: str
    owner: Owner
    pet: Pet
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_total_duration(self) -> int:
        pass

    def display(self) -> str:
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, available_tasks: list, time_limit: int, date: str = ""):
        self.owner = owner
        self.pet = pet
        self.available_tasks = available_tasks
        self.time_limit = time_limit
        self.date = date

    def generate_schedule(self) -> Schedule:
        pass

    def explain(self, schedule: Schedule) -> str:
        pass
