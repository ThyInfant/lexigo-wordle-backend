from django.core.management.base import BaseCommand
from games.models import Word


class Command(BaseCommand):
    help = "Load 5-letter words into database"

    def handle(self, *args, **kwargs):
        with open("data/words.txt", "r") as file:
            words = file.readlines()

        count = 0

        for word in words:
            word = word.strip().lower()

            if (
                len(word) == 5
                and word.isalpha()
            ):
                Word.objects.get_or_create(text=word)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Loaded {count} words successfully"))
