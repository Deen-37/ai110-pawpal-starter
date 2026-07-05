from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner("Jordan", "jordan@example.com", available_minutes=75)

    dog = Pet("Mochi", "dog", age=3)
    cat = Pet("Luna", "cat", age=5)

    owner.add_pet(dog)
    owner.add_pet(cat)

    walk = Task("Morning walk", 30, "high")
    feeding = Task("Feed pets", 15, "high")
    grooming = Task("Brush Luna", 20, "medium")
    playtime = Task("Playtime", 25, "low")

    dog.add_task(walk)
    dog.add_task(feeding)
    cat.add_task(grooming)
    cat.add_task(playtime)

    owner.add_task(walk)
    owner.add_task(feeding)
    owner.add_task(grooming)
    owner.add_task(playtime)

    scheduler = Scheduler()
    today_schedule = scheduler.generate_plan(owner)

    print("Today's Schedule")
    print("----------------")

    for task in today_schedule:
        pet_name = task.pet.name if task.pet else "No pet assigned"
        print(f"- {task.title} for {pet_name}: {task.duration_minutes} min ({task.priority})")

    if scheduler.skipped_tasks:
        print("\nSkipped Tasks")
        print("-------------")
        for task in scheduler.skipped_tasks:
            pet_name = task.pet.name if task.pet else "No pet assigned"
            print(f"- {task.title} for {pet_name}: not enough time")


if __name__ == "__main__":
    main()
