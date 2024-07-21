import json
from django.core.management.base import BaseCommand
from main.models import User, Tweet


class Command(BaseCommand):
    help = "Load data from JSON file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to JSON file")

    def handle(self, *args, **options):
        file_path = options["file_path"]
        with open(file_path) as f:
            data = json.load(f)

        for user_data in data["users"]:
            user = User(**user_data)
            user.save()

        for tweet_data in data["tweets"]:
            user = User.objects.get(id=tweet_data["user_id"])
            tweet = Tweet(user=user, **tweet_data)
            tweet.save()

        self.stdout.write(self.style.SUCCESS("Data loaded successfully"))
