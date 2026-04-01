# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to perform:

1. **Add a pet** — The user enters basic owner and pet information (pet name, type, any special needs) so the system knows who it's planning care for.
2. **Add/edit care tasks** — The user creates and manages pet care tasks (walks, feeding, meds, enrichment, grooming) with at least a duration and priority level, so the scheduler has work items to plan around.
3. **Generate a daily plan** — The user requests a daily schedule that organizes their tasks based on available time, priority, and preferences, and the system explains why it chose that arrangement.

Main objects (classes), their attributes, and methods:

**Owner**
- Attributes: `name`, `available_minutes` (time budget per day), `preferences` (e.g., preferred walk times), `pets` (list of Pet objects)
- Methods: `set_preferences()` — update care preferences; `get_available_time()` — return daily time budget; `add_pet()` — register a pet to this owner
- Responsibility: Represents the human user and their constraints (how much time they have, what they prefer)

**Pet**
- Attributes: `name`, `species`, `age`, `special_needs` (list of notes like medications or dietary restrictions)
- Methods: `add_need()` — add a special need; `get_summary()` — return a readable description of the pet
- Responsibility: Holds all information about the pet that might influence task selection or scheduling

**Task**
- Attributes: `title`, `duration_minutes`, `priority` (low/medium/high, validated), `category` (walk, feeding, meds, grooming, enrichment)
- Methods: `is_high_priority()` — check if priority is high; `__str__()` — return a human-readable description
- Responsibility: Represents a single unit of pet care work with its time cost and importance

**Schedule**
- Attributes: `date`, `owner`, `pet`, `tasks` (ordered list)
- Methods: `add_task()` — append a task; `remove_task()` — remove a task; `get_total_duration()` — sum durations of all tasks; `display()` — render the plan as readable output
- Responsibility: The output artifact — a concrete daily plan that can be displayed to the user

**Scheduler**
- Attributes: `owner`, `pet`, `available_tasks`, `time_limit`, `date`
- Methods: `generate_schedule()` — sort and filter tasks by priority and time constraints, return a Schedule; `explain()` — provide reasoning for why tasks were included and ordered
- Responsibility: The decision-making engine that takes inputs (owner, pet, tasks, constraints) and produces an optimized Schedule

**b. Design changes**

After reviewing the skeleton code, three changes were made:

1. **Added `pets` list and `add_pet()` to Owner** — The UML showed Owner owns Pets, but the original skeleton had no way to link them. Without this, there was no way to associate an owner with their pets in code.

2. **Added `date` parameter to Scheduler** — The Scheduler creates a Schedule which requires a date, but had no date to pass. This was a missing data flow between the two classes.

3. **Added `VALID_PRIORITIES` constant** — Priority was a free-form string with no validation, meaning typos like `"hi"` or `"urgent"` would silently pass through. A constant tuple of allowed values makes validation straightforward.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
