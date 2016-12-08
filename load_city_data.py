from weather_app.models import User, City, EmailMessage

def load_city_state_names():
    population_rank_counter = 1
    city_state_dict = {}
    cities_starting_file = open('static_data/cities_starting_file.txt', 'r')

    while population_rank_counter <= 100:
        next_line = cities_starting_file.readline().strip()
        if next_line == '':
            break
        if str(population_rank_counter) == next_line:
            city_and_state = cities_starting_file.readline()
            split_city_state = city_and_state.split('; ')
            city_state_dict[split_city_state[0].strip()] = split_city_state[1].strip()
            population_rank_counter += 1

    print(city_state_dict)
    return city_state_dict

def add_state_abbreviations(cs_dict):
    pass

if __name__ == "__main__":
    add_state_abbreviations(load_city_state_names())