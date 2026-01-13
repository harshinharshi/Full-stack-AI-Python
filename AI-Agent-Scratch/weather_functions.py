def get_weather(city):
    '''shows the weather of a city''' 
    if city.lower() == "goa":
        return "25 degree celsius in goa"
    elif city.lower() == "mumbai":
        return "1 degree celsius in mumbai"
    elif city.lower() == 'kochi':
        return '45 degree celsius in kochi'
    else:
        return "Unknown city"