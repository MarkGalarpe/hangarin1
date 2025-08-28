from django.core.management.base import BaseCommand
from faker import Faker
import random
from hangarinorg.models import Category, Priority, Task, Note, SubTask

fake = Faker()

class Command(BaseCommand):
    help = "Generate fake data for all models"

    def handle(self, *args, **kwargs):
        # --- Create Categories ---
        for _ in range(5):
            category, created = Category.objects.get_or_create(
                name=fake.word()
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))

        # --- Create Priorities ---
        for name in ["Low", "Medium", "High"]:
            priority, created = Priority.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created priority: {priority.name}"))

        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())

        # --- Create Tasks ---
        tasks = []
        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(nb_words=3),
                description=fake.text(max_nb_chars=50),
                deadline=fake.future_datetime(),
                status=random.choice(['Pending', 'In progress', 'Completed']),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )
            tasks.append(task)
            self.stdout.write(self.style.SUCCESS(f"Created task: {task.title}"))

        # --- Create Notes ---
        for task in tasks:
            for _ in range(random.randint(1, 3)):
                note = Note.objects.create(
                    task=task,
                    content=fake.sentence(nb_words=5)
                )
                self.stdout.write(self.style.SUCCESS(f"Created note for {task.title}: {note.content}"))

        # --- Create SubTasks ---
        for task in tasks:
            for _ in range(random.randint(1, 3)):
                subtask = SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=3),
                    status=random.choice(['Pending', 'In progress', 'Completed']),
                )
                self.stdout.write(self.style.SUCCESS(f"Created subtask for {task.title}: {subtask.title}"))
