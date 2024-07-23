import os
import json
from datetime import datetime
from django.db import transaction
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from main.models import User, Tweet


class Command(BaseCommand):
    help = "Load data from JSON files in a folder"

    def add_arguments(self, parser):
        parser.add_argument(
            "folder_path", type=str, help="Path to folder containing JSON files"
        )

    def handle(self, *args, **options):
        folder_path = options["folder_path"]
        files = os.listdir(folder_path)

        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path) as f:
                        data = json.load(f)

                    with transaction.atomic():
                        if not data:
                            print(f"No JSON data in file: {file_path}")
                            continue

                        user_data = data[0].get("user")
                        if user_data:
                            created_at_str = user_data.pop("created_at")
                            try:
                                created_at = datetime.strptime(
                                    created_at_str, "%a %b %d %H:%M:%S %z %Y"
                                )
                            except ValueError:
                                raise ValidationError(
                                    "Invalid date format: {}".format(created_at_str)
                                )
                            user_data["created_at"] = created_at
                            user, created = User.objects.get_or_create(
                                id=user_data["id"], defaults=user_data
                            )

                            tweet_data = {
                                k: v for k, v in data[0].items() if k != "user"
                            }
                            tweet_data["user"] = user
                            created_at_str = tweet_data.pop("created_at")
                            try:
                                created_at = datetime.strptime(
                                    created_at_str, "%a %b %d %H:%M:%S %z %Y"
                                )
                            except ValueError:
                                raise ValidationError(
                                    "Invalid date format: {}".format(created_at_str)
                                )
                            tweet_data["created_at"] = created_at

                            try:
                                tweet = Tweet.objects.get(id=tweet_data["id"])
                                for key, value in tweet_data.items():
                                    setattr(tweet, key, value)
                                tweet.save()
                            except Tweet.DoesNotExist:
                                tweet = Tweet(**tweet_data)
                                tweet.save()

                except json.JSONDecodeError as e:
                    print(f"Error loading JSON data from file: {file_path}")
                    print(f"Error message: {str(e)}")
                    continue

                os.remove(file_path)

        self.stdout.write(self.style.SUCCESS("Data loaded successfully"))
