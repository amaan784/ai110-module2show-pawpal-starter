```mermaid
classDiagram
    class Owner {
        +str name
        +int available_minutes
        +dict preferences
        +list pets
        +set_preferences(prefs) None
        +get_available_time() int
        +add_pet(pet) None
        +get_all_tasks() list
    }

    class Pet {
        +str name
        +str species
        +int age
        +list special_needs
        +list tasks
        +add_need(need) None
        +add_task(task) None
        +get_summary() str
    }

    class Task {
        +str title
        +int duration_minutes
        +str priority
        +str category
        +bool completed
        +str scheduled_time
        +str frequency
        +str due_date
        +mark_complete() Task or None
        +is_high_priority() bool
        +__str__() str
    }

    class Schedule {
        +str date
        +Owner owner
        +Pet pet
        +list tasks
        +add_task(task) None
        +remove_task(task) None
        +get_total_duration() int
        +display() str
    }

    class Scheduler {
        +Owner owner
        +Pet pet
        +list available_tasks
        +int time_limit
        +str date
        +generate_schedule() Schedule
        +sort_by_time(tasks) list
        +filter_tasks(completed, pet_name) list
        +detect_conflicts() list
        +mark_task_complete(task) None
        +explain(schedule) str
    }

    Owner "1" --> "1..*" Pet : owns
    Pet "1" --> "0..*" Task : has
    Schedule "1" --> "1" Owner : belongs to
    Schedule "1" --> "1" Pet : for
    Schedule "1" --> "0..*" Task : contains
    Scheduler "1" --> "1" Owner : uses
    Scheduler "1" --> "1" Pet : uses
    Scheduler "1" --> "0..*" Task : selects from
    Scheduler "1" ..> "1" Schedule : creates
```
