from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from hangarinorg.models import Category, Priority, Task, SubTask, Note 


class Command(BaseCommand):
    help = 'Generate fake data for the hangarinorg app'

    def handle(self, *args, **kwargs):
        self.create_tasks(10)
        self.create_notes(10)
        self.create_subtasks(10)

    def create_tasks(self, count):
        fake = Faker()
        for _ in range(count):
            Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(
                    fake.date_time_between(start_date="+1d", end_date="+30d")
                ),
                status=fake.random_element(
                    elements=['Pending', 'In Progress', 'Completed']
                ),
                category=Category.objects.order_by('?').first(),
                priority=Priority.objects.order_by('?').first(),
            )
        self.stdout.write(self.style.SUCCESS(f'{count} fake tasks created.'))

    def create_notes(self, count):
        fake = Faker()
        for _ in range(count):
            Note.objects.create(
                task=Task.objects.order_by('?').first(),
                content=fake.paragraph(nb_sentences=3),
            )
        self.stdout.write(self.style.SUCCESS(f'{count} fake notes created.'))

    def create_subtasks(self, count):
        fake = Faker()
        for _ in range(count):
            SubTask.objects.create(
                parent_task=Task.objects.order_by('?').first(),
                title=fake.sentence(nb_words=5),
                status=fake.random_element(
                    elements=['Pending', 'In Progress', 'Completed']
                ),
            )
        self.stdout.write(self.style.SUCCESS(f'{count} fake subtasks created.'))