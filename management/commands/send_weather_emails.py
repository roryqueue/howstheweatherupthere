import traceback
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
import settings
from weather_app.models import User, City, EmailMessage
from lib.wunderground_api import TodaysWeather


class SendWeatherEmailsCommand(BaseCommand):
    help = 'Sends daily weather alert email messages to all users in database'

    def add_arguments(self, parser):
        parser.add_argument('only_to', nargs='*', type=str)

    def handle(self, *args, **options):

        for user in User.objects.all():
            todays_message = EmailMessage(recipient=user.email)

            try:
                successful_sends = send_mail(
                    todays_message.subject,
                    todays_message.body,
                    settings.from_addr,
                    [todays_message.recipient]
                )
                if successful_sends == 0:
                    todays_message.success = False
                    todays_message.error = """
                        send_mail returned 0, indication no successful recipients
                    """

            except Exception as e:
                todays_message.success = False
                todays_message.error = str(e)
                todays_message.traceback = traceback.print_exc()

