import random
import requests

data = []


# Displaying the console menu
def display_menu():
    print("Select an option:")
    print("1. All countries")
    print("2. Country info")
    print("3. Capital Quiz")
    print("0. Exit")


# Calling the methods of menu
def select_option(option):
    if option == "1":
        display_countries()
    elif option == "2":
        display_country_info()
    elif option == "3":
        display_quiz_game(data)
    else:

        print("Invalid input, please try again.")

# Fetching all countries data when the project started running
def fetch_countries():
    global data
    data = requests.get('https://restcountries.com/v3.1/all').json()


# Menu 1: Displaying the all countries names received by API
def display_countries():
    for i in range(len(data)):
        print(f"{i + 1}) {data[i]['name']['common']}")
    print('')


# Menu 2: Displaying the full info of the country user entered
def display_country_info():
    country_input = input("Enter the country name: ")
    data = requests.get(f'https://restcountries.com/v3.1/name/{country_input}').json()
    common_name = data[0]['name']['common']
    official_name = data[0]['name']['official']
    capitals = ", ".join(data[0].get('capital', []))
    population = data[0].get('population', 'N/A')
    area = data[0].get('area', 'N/A')
    region = data[0].get('region', 'N/A')
    subregion = data[0].get('subregion', 'N/A')
    currencies = ", ".join([f"{info['name']} ({code})" for code, info in data[0]['currencies'].items()])
    car_signs = ", ".join(data[0]['car'].get('signs', []))
    car_side = data[0]['car'].get('side', 'N/A')
    internet_tld = ", ".join(data[0]['tld'])
    google_maps = data[0]['maps'].get('googleMaps', 'N/A')
    print(f"""Name: {common_name}
Official name: {official_name}
Capital: {capitals}
Area: {area} km^2
Population: {population} people
Region: {region}
Subregion: {subregion}
Car sign and driving side: {car_signs} - {car_side}
Currency: {currencies}
Internet TLD: {internet_tld}
Google maps link: {google_maps}\n""")


# Method used in menu 3 in order to generate the options of quiz
def generate_options(correct_country, all_countries):
    options = [correct_country['capital'][0]] if correct_country.get('capital') else []
    while len(options) < 4:
        random_country = random.choice(all_countries)
        if random_country.get('capital') and random_country['capital'][0] not in options:
            options.append(random_country['capital'][0])

    random.shuffle(options)
    return options


# Menu 3: Displaying the quiz with the country name and options for capital
def display_quiz_game(countries):
    correct_answers = 0
    wrong_answers = 0

    countries_with_capitals = [c for c in countries if c.get('capital') and len(c['capital']) > 0]

    quiz_countries = random.sample(countries_with_capitals, 10)

    for index, country in enumerate(quiz_countries, start=1):
        correct_capital = country['capital'][0]
        options = generate_options(country, countries_with_capitals)

        print(f"№ {index}: The capital of {country['name']['common']} ?")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")

        user_input = input("Enter your choice (1-4) or exit (0): ")

        if user_input == "0":
            break

        if user_input.isdigit() and 1 <= int(user_input) <= 4:
            selected_option = options[int(user_input) - 1]
            if selected_option == correct_capital:
                print("Correct!\n")
                correct_answers += 1
            else:
                print(f"Wrong! Correct answer: {correct_capital}.\n")
                wrong_answers += 1
        else:
            print("Invalid input, please try again!")
    if correct_answers >= 7:
        print("You won :)")
    else:
        print("You lost. Please, try again!")

    print(f"Statistics: Correct answers - {correct_answers}, wrong answers - {wrong_answers}\n")


# The main function when program is executed
print("Welcome to the Country Quiz :)")
while True:
    fetch_countries()
    display_menu()
    user_input = input("Enter your choice: ")
    if user_input == "0":
        break
    select_option(user_input)
