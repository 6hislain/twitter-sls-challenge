import os
import json
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Split a JSON file into multiple files, with each file containing up to 10 lines of data"

    def add_arguments(self, parser):
        parser.add_argument("input_file", type=str, help="Path to the input JSON file")
        parser.add_argument("output_folder", type=str, help="Path to the output folder")

    def handle(self, *args, **options):
        input_file = options["input_file"]
        output_folder = options["output_folder"]

        with open(input_file, "r") as f:
            lines = f.readlines()

        num_files = len(lines) // 10
        if len(lines) % 10 > 0:
            num_files += 1

        for i in range(num_files):
            output_file = os.path.join(output_folder, f"{i+1}.json")
            with open(output_file, "w") as f:
                start = i * 10
                end = start + 10
                data = [json.loads(line) for line in lines[start:end]]
                json.dump(data, f)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully split {input_file} into {num_files} files in folder {output_folder}."
            )
        )
