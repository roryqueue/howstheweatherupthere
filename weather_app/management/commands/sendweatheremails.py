import traceback
from django.core.management.base import BaseCommand, CommandError
from weather_app.models import User, City, EmailMessage
from lib.wunderground_api import TodaysWeather


class Command(BaseCommand):
    help = 'Loads city, state, and state abbreviation data from uncleaned text files to db'

    def add_arguments(self, parser):
        parser.add_argument('only_to', nargs='*', type=str)

    def handle(self, *args, **options):

        for user in User.objects.all():
            todays_message = EmailMessage(recipient=user.email)
            todays_message.from_address = settings.EMAIL_HOST_USER
            todays_message.send()