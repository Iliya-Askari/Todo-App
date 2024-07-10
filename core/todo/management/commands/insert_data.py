from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from datetime import datetime
import random
from accounts.models import Users , Profile
from todo.models import Task


category_list = [
    "Technology",
    "Sports",
    "Politics",
    "Business",
    "Health",
    "Science",
    "World",
    "Travel"
]
class Command(BaseCommand):
    help = "Inserting dummy data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        profiles = []
        for _ in range(10):
            user = Users.objects.create_user(email=self.fake.email(), password='Test@123456')
            profile = Profile.objects.get(user=user)
            profile.first_name = self.fake.first_name()
            profile.last_name = self.fake.last_name()
            profile.description = self.fake.paragraph(nb_sentences=3)
            profile.save()
            profiles.append(profile)
        
        for _ in range(10):
            Task.objects.create(
                user = random.choice(profiles),
                title = self.fake.paragraph(nb_sentences=1),
                complete = self.fake.boolean(),
            )