from dataclasses import dataclass, field
from datetime import date, timedelta

VALID_PRIORITIES = ("low", "medium", "high")
PRIORITY_RANK = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """Represents a single pet care activity with duration, priority, and status."""
    title: str
    duration_minutes: int
    priority: str = "medium"
    category: str = "general"
    completed: bool = False
    scheduled_time: str = ""
    frequency: str = "once"
    due_date: str = ""

    def __post_init__(self):
        """Validate that priority is one of the allowed values."""
        if self.priority not in VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {VALID_PRIORITIES}, got '{self.priority}'")
        if not self.due_date:
            self.due_date = str(date.today())

    def mark_complete(self):
        """Mark this task as completed. Returns a new Task if recurring, else None."""
        self.completed = True
        if self.frequency == "daily":
            next_due = date.fromisoformat(self.due_date) + timedelta(days=1)
            return Task(
                title=self.title, duration_minutes=self.duration_minutes,
                priority=self.priority, category=self.category,
                scheduled_time=self.scheduled_time, frequency=self.frequency,
                due_date=str(next_due),
            )
        elif self.frequency == "weekly":
            next_due = date.fromisoformat(self.due_date) + timedelta(weeks=1)
            return Task(
                title=self.title, duration_minutes=self.duration_minutes,
                priority=self.priority, category=self.category,
                scheduled_time=self.scheduled_time, frequency=self.frequency,
                due_date=str(next_due),
            )
        return None

    def is_high_priority(self) -> bool:
        """Return True if this task has high priority."""
        return self.priority == "high"

    def __str__(self) -> str:
        """Return a formatted string showing priority, title, duration, and status."""
        status = "done" if self.completed else "pending"
        return f"[{self.priority.upper()}] {self.title} ({self.duration_minutes} min, {self.category}) - {status}"


@dataclass
class Pet:
    """Stores pet details and a list of care tasks."""
    name: str
    species: str
    age: int = 0
    special_needs: list = field(default_factory=list)
    tasks: list = field(default_factory=list)

    def add_need(self, need: str) -> None:
        """Add a special need to this pet's list."""
        self.special_needs.append(need)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def get_summary(self) -> str:
        """Return a readable summary of the pet's info and special needs."""
        needs = ", ".join(self.special_needs) if self.special_needs else "none"
        return f"{self.name} ({self.species}, age {self.age}) — special needs: {needs}"


@dataclass
class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    name: str
    available_minutes: int = 60
    preferences: dict = field(default_factory=dict)
    pets: list = field(default_factory=list)

    def set_preferences(self, prefs: dict) -> None:
        """Update the owner's care preferences."""
        self.preferences.update(prefs)

    def get_available_time(self) -> int:
        """Return the owner's available time budget in minutes."""
        return self.available_minutes

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list:
        """Collect and return all tasks across all of the owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


@dataclass
class Schedule:
    """A daily plan containing an ordered list of tasks for a specific pet."""
    date: str
    owner: Owner
    pet: Pet
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to the schedule."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the schedule."""
        self.tasks.remove(task)

    def get_total_duration(self) -> int:
        """Return the sum of all task durations in minutes."""
        return sum(t.duration_minutes for t in self.tasks)

    def display(self) -> str:
        """Return a formatted string representation of the full schedule."""
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
    """The scheduling engine that selects and orders tasks within time constraints."""

    def __init__(self, owner: Owner, pet: Pet, available_tasks: list = None, time_limit: int = None, date: str = ""):
        """Initialize the scheduler with an owner, pet, tasks, and constraints."""
        self.owner = owner
        self.pet = pet
        self.available_tasks = available_tasks if available_tasks is not None else pet.tasks
        self.time_limit = time_limit if time_limit is not None else owner.available_minutes
        self.date = date or str(date if date else today())

    def generate_schedule(self) -> Schedule:
        """Sort tasks by priority and fill the schedule within the time limit."""
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

    def sort_by_time(self, tasks: list = None) -> list:
        """Sort tasks by their scheduled_time in HH:MM format."""
        task_list = tasks if tasks is not None else self.available_tasks
        return sorted(task_list, key=lambda t: t.scheduled_time if t.scheduled_time else "99:99")

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> list:
        """Filter available tasks by completion status and/or pet name."""
        result = self.available_tasks
        if completed is not None:
            result = [t for t in result if t.completed == completed]
        if pet_name is not None:
            pet = next((p for p in self.owner.pets if p.name == pet_name), None)
            if pet:
                result = [t for t in result if t in pet.tasks]
        return result

    def detect_conflicts(self) -> list:
        """Check for tasks scheduled at the exact same time and return warnings."""
        warnings = []
        timed = [t for t in self.available_tasks if t.scheduled_time]
        seen = {}
        for task in timed:
            if task.scheduled_time in seen:
                other = seen[task.scheduled_time]
                warnings.append(
                    f"Conflict at {task.scheduled_time}: "
                    f"'{task.title}' and '{other.title}' are both scheduled at the same time"
                )
            else:
                seen[task.scheduled_time] = task
        return warnings

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task complete and auto-add the next occurrence if recurring."""
        next_task = task.mark_complete()
        if next_task is not None:
            self.pet.add_task(next_task)

    def explain(self, schedule: Schedule) -> str:
        """Return a reasoning summary of why each task was included or skipped."""
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
    """Return today's date as a string."""
    return str(date.today())
