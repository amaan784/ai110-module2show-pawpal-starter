# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to perform:

1. **Add a pet.** The user enters owner and pet info so the system knows who it's planning care for.
2. **Add or edit care tasks.** The user creates tasks like walks, feeding, or meds with a duration and priority level.
3. **Generate a daily plan.** The system organizes tasks by priority within the owner's time budget and explains why.

The system uses five classes. Owner holds the person's name, time budget, and list of pets. Pet stores the animal's details and its own task list. Task represents a single care activity with a title, duration, priority, category, scheduled time, and recurrence frequency. Schedule is the output, an ordered list of tasks for one pet on one day. Scheduler is the brain that sorts tasks by priority, fills the time budget, detects conflicts, and explains its decisions.

**b. Design changes**

Three things changed after the initial skeleton was built. First, Owner needed a pets list and an add_pet method because the UML showed ownership but the code had no way to link them. Second, Scheduler needed a date parameter because it creates a Schedule that requires a date, and there was no way to pass one in. Third, a VALID_PRIORITIES constant was added so that typos like "urgent" would raise an error instead of silently passing through.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler uses two constraints. Priority is the primary sort key, ranking high above medium above low. Time budget is the hard cap, the owner's available_minutes. Tasks are added in priority order until time runs out. Priority came first because a pet owner would rather skip grooming than miss medication.

**b. Tradeoffs**

Conflict detection only checks for exact time matches, not overlapping durations. A 30 minute task at 07:45 and another task at 08:00 would not be flagged even though they overlap by 15 minutes. This keeps the logic simple and works well enough for a personal planning tool where most tasks are short and scheduled at round times.

---

## 3. AI Collaboration

**a. How you used AI**

I used Claude Code throughout this project. For the early design phase I described the scenario and asked it to help brainstorm classes and their responsibilities. During implementation I gave it the skeleton file and asked it to flesh out the logic one class at a time. For testing I described the behaviors I wanted to verify and had it write the pytest functions. The most helpful prompts were the ones where I gave it a specific file and asked a focused question like "what's missing in this class" or "add conflict detection that returns warnings instead of crashing."

**b. Judgment and verification**

When the AI first generated the Scheduler class it did not include a date parameter. I noticed that Schedule requires a date but Scheduler had no way to provide one, so the generated code would have broken at runtime. I caught this by reading through the skeleton and tracing how data flows between classes. I asked the AI to fix it and verified the fix by running main.py end to end.

---

## 4. Testing and Verification

**a. What you tested**

Eight tests cover the core behaviors. Task completion verifies mark_complete flips the status. Task addition checks that a pet's task count increases. Sorting correctness confirms tasks come back in chronological order. Recurrence logic verifies a daily task spawns a new one due the next day. Conflict detection has both a positive test (same time flagged) and a negative test (different times not flagged). Time limit enforcement makes sure the scheduler stops adding tasks when the budget runs out. The empty pet test confirms the scheduler handles zero tasks without crashing.

**b. Confidence**

4 out of 5. Every core path is tested and all eight tests pass. If I had more time I would test overlapping durations, weekly recurrence, and what happens when two pets have tasks at the same time across different schedules.

---

## 5. Reflection

**a. What went well**

The class design held up well from start to finish. The five class structure made it easy to add new features like recurring tasks and conflict detection without rewriting existing code. The Scheduler class in particular worked well as a central place to put all the smart logic.

**b. What you would improve**

I would make conflict detection aware of task durations so it can catch overlapping tasks, not just exact time matches. I would also add the ability to drag and reorder tasks in the Streamlit UI instead of relying only on automatic sorting.

**c. Key takeaway**

The biggest lesson was that when working with AI tools you still have to be the one who understands how the pieces connect. The AI can write solid code for individual classes but it does not always see the gaps between them, like a missing parameter or a broken data flow. Being the lead architect means reviewing every suggestion against the full picture and catching the things the AI misses.
