from django.core.management.base import BaseCommand, CommandError
from faker import Faker
import random
from accounts.models import Users
from todo.models import Task


category_list = [
    "Technology",
    "Sports",
    "Politics",
    "Business",
    "Health",
    "Science",
    "World",
    "Travel",
]


class Command(BaseCommand):
    help = "Inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        users = []
        for _ in range(5):
            user = Users.objects.create_user(
                email=self.fake.email(), password="Test@123456"
            )
            users.append(user)

        for _ in range(5):
            Task.objects.create(
                user=random.choice(users),
                title=self.fake.paragraph(nb_sentences=1),
                complete=self.fake.boolean(),
            )
