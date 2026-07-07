from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan", "jordan@example.com", available_minutes=75)

    dog = Pet("Mochi", "dog", age=3)
    cat = Pet("Luna", "cat", age=5)

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Deliberately added out of chronological order to prove sort_by_time works.
    playtime = Task("Playtime", 25, "low", time="16:00")
    walk = Task("Morning walk", 30, "high", time="08:30", frequency="weekly")
    grooming = Task("Brush Luna", 20, "medium", time="13:15")
    feeding = Task("Feed pets", 15, "high", time="07:00", frequency="daily")
    # Deliberately clashes with grooming at 13:15, for a different pet.
    vet_call = Task("Vet check-up", 30, "high", time="13:15")

    dog.add_task(walk)
    dog.add_task(feeding)
    dog.add_task(vet_call)
    cat.add_task(grooming)
    cat.add_task(playtime)

    owner.add_task(playtime)
    owner.add_task(walk)
    owner.add_task(grooming)
    owner.add_task(feeding)
    owner.add_task(vet_call)

    scheduler = Scheduler()

    # Lightweight conflict detection: warn about tasks sharing a time slot.
    print("Schedule conflict check")
    print("-----------------------")
    conflicts = scheduler.detect_conflicts(owner.get_tasks())
    if conflicts:
        for warning in conflicts:
            print(warning)
    else:
        print("No conflicts found.")
    print()

    # Completing a recurring task auto-creates its next occurrence.
    print("Completing tasks (recurring ones spawn a next occurrence)")
    print("---------------------------------------------------------")
    for task in (feeding, walk, grooming):
        new_task = scheduler.complete_task(owner, task)
        if new_task is None:
            print(f"- Completed {task.title} ({task.frequency}) - no repeat")
        else:
            print(f"- Completed {task.title} ({task.frequency}) - queued next: "
                  f"{new_task.title} at {new_task.time}")
    print()

    print("Tasks in the order they were added")
    print("----------------------------------")
    for task in owner.get_tasks():
        print(f"- {task.time}  {task.title}")

    print("\nSorted by time (earliest first)")
    print("-------------------------------")
    for task in scheduler.sort_by_time(owner.get_tasks()):
        print(f"- {task.time}  {task.title}")

    print("\nFilter: completed tasks only")
    print("----------------------------")
    for task in scheduler.filter_tasks(owner.get_tasks(), completed=True):
        print(f"- {task.time}  {task.title} ({task.get_summary()})")

    print("\nFilter: incomplete tasks only")
    print("-----------------------------")
    for task in scheduler.filter_tasks(owner.get_tasks(), completed=False):
        print(f"- {task.time}  {task.title}")

    print("\nFilter: tasks for Luna")
    print("----------------------")
    for task in scheduler.filter_tasks(owner.get_tasks(), pet_name="Luna"):
        print(f"- {task.time}  {task.title}")

    print("\nFilter: incomplete tasks for Mochi")
    print("----------------------------------")
    for task in scheduler.filter_tasks(owner.get_tasks(), completed=False, pet_name="Mochi"):
        print(f"- {task.time}  {task.title}")


if __name__ == "__main__":
    main()
