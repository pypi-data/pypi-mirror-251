import requests


class Weather:
    """Creates a Weather object getting an apikey as input and either
    a city name or lat and lon coordinates.

    Package use examples:

    # Create a weather object using a city name.
    # The api key is not guaranteed to work.
    # Get your own api key from https://openweathermap.org
    # And wait a couple of hours for the apikey to get activated.

    -> weather1 = Weather(api_key='525edac8c50454f21c9557e48d9a893e', city='Berlin')

    Using latitude and longitude coordinates:
    -> weather2 = Weather(api_key='525edac8c50454f21c9557e48d9a893e', lat=42.8, lon=12.4)

    # Get complete weather forecast for the next 12 hours:
    -> weather1.next_12h()

    # Simplified forecast for the next 12 hours:
    -> weather2.next_12h_simplified()

    Sample url to get sky condition icons:
    https://openweathermap.org/img/wn/10d@2x.png
    """

    def __init__(self, api_key, city=None, lat=None, lon=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise AttributeError("Provide a city, or lat and lon values")

    def next_12h(self):
        """Returns 3-hour for the next 12 hours as a dict.
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """Returns date, temperature and sky condition every 3 hours for
        the next 12 hours as a list of tuples.
        """
        try:
            simple_data = []
            for data in self.data['list'][:4]:
                simple_data.append((data['dt_txt'], data['main']['temp'], data['weather'][0]['description'],
                                    data['weather'][0]['icon']))
            return simple_data
        except KeyError:
            return "City not found, try different city name."

weather = Weather(api_key='525edac8c50454f21c9557e48d9a893e', city='Milan')
print(weather.next_12h_simplified())


