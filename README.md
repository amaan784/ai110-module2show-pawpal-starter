# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

Beyond basic priority-based scheduling, PawPal+ includes:

- **Sort by time** — tasks with a `scheduled_time` (HH:MM) are sorted chronologically for a clear daily timeline
- **Filter by status or pet** — view only pending tasks, or narrow down to a specific pet's tasks
- **Recurring tasks** — daily or weekly tasks automatically generate the next occurrence when marked complete
- **Conflict detection** — warns when two tasks are scheduled at the exact same time

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest tests/test_pawpal.py -v
```

The tests cover:

- **Task completion** — `mark_complete()` changes task status
- **Task addition** — adding a task to a pet increases its task count
- **Sorting correctness** — `sort_by_time()` returns tasks in chronological order
- **Recurrence logic** — marking a daily task complete creates a new task due the next day
- **Conflict detection** — flags duplicate scheduled times, no false positives for different times
- **Time limit** — scheduler stops adding tasks when time budget is exceeded
- **Empty pet** — scheduler handles a pet with no tasks gracefully

**Confidence Level: 4/5** — All core scheduling behaviors are tested including happy paths and edge cases. The main gap is that overlapping durations (not just exact time matches) are not tested because the scheduler does not yet support duration-aware conflict detection.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
