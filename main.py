# -*- coding: utf-8 -*-
import forecastio
import datetime
icons_dir = './icons/'

coord = (55.6, 37.7)

icons = {
    'clear-day':'Sun.png',
    'clear-night':'Moon.png',
    'rain':'Cloud-Rain.png',
    'snow':'Cloud-Snow-Alt.png',
    'sleet':'Cloud-Hail.png',
    'wind':'Wind.png',
    'fog':'Cloud-Fog.png',
    'cloudy':'Cloud.png',
    'partly-cloudy-day':'Cloud-Sun.png',
    'partly-cloudy-night':'Cloud-Moon.png',
}

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def weather(query):
    results = []
    forecast = forecastio.load_forecast('fa4410dea9d5faaf6b54c606b9f2030c', *coord, units='si')
    daily = forecast.daily()
    if daily.data[0].time < datetime.datetime.now():
        del daily.data[0]
    # summary for this week
    results.append({
        "Title": 'This Week: {}'.format(daily.summary),
        "SubTitle": '',
        "IcoPath": icons_dir + icons.get(daily.icon, '')
    })
    # daily summary for the next 5 days
    for day in daily.data[:5]:
        results.append({
            "Title": '{}: {}'.format(weekdays[day.time.weekday()], day.d['summary']),
            "SubTitle": 'High: {}°C    \tLow: {}°C    \tPressure: {:.2f}mm    \tWind: {}m/s    \tRain: {}%'.format(
                day.d['temperatureMax'], day.d['temperatureMin'], day.d['pressure']*0.7501, day.d['windSpeed'], day.d['precipProbability']*100),
            "IcoPath": icons_dir + icons.get(day.d['icon'], '')
        })
    if not results:
        results.append({
                "Title": 'Not found',
                "SubTitle": '',
                "IcoPath":"Images/app.png"
            })
    return results

from wox import Wox

class Weather(Wox):
    def query(self, query):
        return weather(query)

if __name__ == "__main__":
    Weather()