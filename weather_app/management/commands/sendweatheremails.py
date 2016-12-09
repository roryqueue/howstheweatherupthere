import traceback
from django.core.management.base import BaseCommand, CommandError
from django.template import loader, Context
from weather_app.models import User, Location, EmailMessage
from weather_app.wunderground_api import TodaysWeather
from weather_app import settings

class Command(BaseCommand):
    help = "Sends an email containing a user's local weather to their email"
    EMAIL_SUBJECTS = {
        'good': "It's nice out! Enjoy a discount on us.",
        'average': "Enjoy a discount on us.",
        'poor': "Not so nice out? That's okay, enjoy a discount on us."
    }
    EMAIL_TEMPLATE_PATH = 'weather_email.html'

    def add_arguments(self, parser):
        parser.add_argument('only_to', nargs='*', type=str)

    def handle(self, *args, **options):
        todays_weather = TodaysWeather()

        for user in User.objects.filter(active=True):
            email_message = EmailMessage(recipient=user)
            email_message.from_address = settings.EMAIL_HOST_USER
            users_weather = todays_weather.find_for_location(user.location)
            email_message.subject = self.EMAIL_SUBJECTS[users_weather['weather_qualitative']]
            email_message.text =\
"""Hello!
The current weather in {city}, {state} is {description} and {temperature} degrees.
Have a great day!""".format(
                city=user.location.city,
                state=user.location.state,
                temperature=str(users_weather['temperature']),
                description=users_weather['weather_phrase']
            )
            email_message.html = self.render_email_html(user.location, users_weather)
            email_message.send()

    def render_email_html(self, location, weather):
        template = loader.get_template(self.EMAIL_TEMPLATE_PATH)
        context = Context({
            'city': location.city,
            'state': location.state,
            'description': weather['weather_phrase'],
            'temperature': weather['temperature'],
            'image_url': weather['icon_url']
        })
        return template.render(context)
