# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can track pet care tasks like walks, feeding, meds, enrichment, and grooming. It should consider constraints like time available, priority, and owner preferences. It should also produce a daily plan and explain why it chose that plan.

The system is designed first as a UML diagram, then implemented in Python, then connected to the Streamlit UI.

## Features

**Priority Based Scheduling** sorts all tasks from high to low priority and packs them into the owner's available time budget. High priority tasks like medication and feeding always come first.

**Sort by Time** arranges tasks in chronological order using their scheduled time in HH:MM format, so the daily plan reads like a real timeline.

**Filter by Status or Pet** lets you view only pending tasks or narrow the list down to a specific pet. Useful when an owner has multiple animals.

**Recurring Tasks** automatically generate the next occurrence when marked complete. A daily walk due today becomes a new pending task due tomorrow. Weekly tasks jump ahead by seven days.

**Conflict Detection** scans all scheduled tasks and warns you when two tasks land on the exact same time slot. The warning shows up in the UI so you can fix it before building the schedule.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

The tests cover task completion, task addition to pets, chronological sorting, daily recurrence logic, conflict detection with both positive and negative cases, time limit enforcement, and the edge case of scheduling for a pet with no tasks.

Confidence Level: 4 out of 5. All core scheduling behaviors are tested with both happy paths and edge cases. The main gap is that overlapping durations are not tested because the scheduler only checks for exact time matches, not whether two tasks actually overlap in real minutes.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running the app

```bash
streamlit run app.py
```

### Running tests

```bash
python -m pytest tests/test_pawpal.py -v
```
