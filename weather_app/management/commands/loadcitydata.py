import traceback
from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from weather_app.models import Location


class Command(BaseCommand):
    help = 'Sends daily weather alert email messages to all users in database'
    RAW_CITIES_FILEPATH = 'static_data/cities_starting_file.txt'
    RAW_ABBREVIATIONS_FILEPATH = 'static_data/state_abbreviations.txt'

    def handle(self, *args, **options):
        locations = self.load_initial_locations()
        abbreviations = self.load_state_abbreviations()
        self.match_state_abbreviations(locations, abbreviations)
        pprint([row.__dict__ for row in Location.objects.all()])

    def load_initial_locations(self):
        population_rank_counter = 1
        cities_starting_file = open(self.RAW_CITIES_FILEPATH, 'r')

        next_line = None
        # loop until we have our tow 100 cities or the file ends
        while population_rank_counter <= 100 and next_line != '':
            try:
                next_line = cities_starting_file.readline().strip()

                if next_line == str(population_rank_counter):
                    city_and_state = cities_starting_file.readline()
                    split_city_state = city_and_state.split('; ')
                    city = split_city_state[0].strip()
                    state = split_city_state[1].strip()
                    new_location = Location(city=city, state=state)
                    new_location.save()
                    population_rank_counter += 1
            except IntegrityError:
                pass

        return Location.objects.all()

    def load_state_abbreviations(self):
        state_abbreviations = {}
        for line in open(self.RAW_ABBREVIATIONS_FILEPATH, 'r'):
            split_line = line.strip().split('  ')
            name = split_line[0].strip()
            abbreviation = split_line[-1].strip()
            state_abbreviations[name] = abbreviation

        return state_abbreviations

    def match_state_abbreviations(self, locations, abbreviations):
        for location in locations:
            location.state_abbreviation = abbreviations[location.state]
            location.save()
