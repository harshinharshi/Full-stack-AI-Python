def get_weather(city):
    '''shows the weather of a city''' 
    if city.lower() == "goa":
        return "20 degree celsius"
    elif city.lower() == "mumbai":
        return "30 degree celsius"
    else:
        return "Unknown city"