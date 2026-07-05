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
