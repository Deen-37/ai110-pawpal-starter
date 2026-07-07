from pawpal_system import Owner, Pet, Scheduler, Task


def test_priority_score_maps_levels():
    assert Task("Walk", 30, "high").priority_score() == 3
    assert Task("Brush", 20, "medium").priority_score() == 2
    assert Task("Play", 25, "low").priority_score() == 1
    assert Task("Nap", 10, "unknown").priority_score() == 0


def test_scheduler_respects_available_minutes():
    owner = Owner("Jordan", "jordan@example.com", available_minutes=40)
    owner.add_task(Task("Feed", 15, "high"))
    owner.add_task(Task("Walk", 30, "high"))
    owner.add_task(Task("Groom", 20, "low"))

    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner)

    # Only tasks that fit in 40 minutes are scheduled (Feed 15 + Groom 20 = 35).
    scheduled_titles = [task.title for task in plan]
    assert scheduled_titles == ["Feed", "Groom"]
    assert [task.title for task in scheduler.skipped_tasks] == ["Walk"]


def test_mark_complete_changes_status():
    task = Task("Feed", 15, "high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog", age=3)
    assert len(pet.care_tasks) == 0

    pet.add_task(Task("Walk", 30, "high"))

    assert len(pet.care_tasks) == 1


def test_sort_by_time_returns_chronological_order():
    # Added deliberately out of order, including a non-padded hour.
    tasks = [
        Task("Playtime", 25, "low", time="16:00"),
        Task("Walk", 30, "high", time="08:30"),
        Task("Vet", 20, "high", time="9:00"),
        Task("Feed", 15, "high", time="07:00"),
    ]

    scheduler = Scheduler()
    ordered_titles = [task.title for task in scheduler.sort_by_time(tasks)]

    assert ordered_titles == ["Feed", "Walk", "Vet", "Playtime"]


def test_completing_daily_task_creates_next_occurrence():
    owner = Owner("Jordan", "jordan@example.com")
    pet = Pet("Mochi", "dog", age=3)
    owner.add_pet(pet)

    feeding = Task("Feed", 15, "high", time="07:00", frequency="daily")
    pet.add_task(feeding)
    owner.add_task(feeding)

    scheduler = Scheduler()
    next_task = scheduler.complete_task(owner, feeding)

    # The original is now complete...
    assert feeding.completed is True
    # ...and a fresh, uncompleted copy was created for the next occurrence.
    assert next_task is not None
    assert next_task is not feeding
    assert next_task.completed is False
    assert next_task.title == "Feed"
    assert next_task.time == "07:00"
    assert next_task.frequency == "daily"
    # The new task is registered on both the owner and the pet.
    assert next_task in owner.get_tasks()
    assert next_task in pet.care_tasks


def test_detect_conflicts_flags_duplicate_times():
    dog = Pet("Mochi", "dog", age=3)
    cat = Pet("Luna", "cat", age=5)

    grooming = Task("Brush Luna", 20, "medium", time="13:15")
    vet_call = Task("Vet check-up", 30, "high", time="13:15")
    cat.add_task(grooming)
    dog.add_task(vet_call)
    walk = Task("Walk", 30, "high", time="08:30")

    scheduler = Scheduler()
    warnings = scheduler.detect_conflicts([walk, grooming, vet_call])

    # Exactly one slot (13:15) is over-booked; 08:30 is fine.
    assert len(warnings) == 1
    assert "13:15" in warnings[0]
    assert "Brush Luna" in warnings[0]
    assert "Vet check-up" in warnings[0]


def test_detect_conflicts_empty_when_no_duplicates():
    scheduler = Scheduler()
    tasks = [
        Task("Feed", 15, "high", time="07:00"),
        Task("Walk", 30, "high", time="08:30"),
    ]

    assert scheduler.detect_conflicts(tasks) == []
