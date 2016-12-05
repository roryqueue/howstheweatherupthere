from django.core.management.base import BaseCommand, CommandError
from weather_app.models import User
from email_sender.models import EmailMessage

class SendWeatherEmails(BaseCommand):
    help = 'Sends daily weather alert email messages to all users in database'

    def add_arguments(self, parser):
        parser.add_argument('only_to', nargs='*', type=str)

    def handle(self, *args, **options):
        for user in User.objects.all():
            poll.opened = False
            poll.save()

            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))