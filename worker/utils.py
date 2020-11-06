import json
from datetime import timedelta

import requests

from worker import settings as worker_settings
from worker.models import Destination, FlightsCache


def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def get_flights(date):
    """ Запрашиваем с API самую дешевую цену делая сортировку по цене им храним в таблице """
    destinations = Destination.objects.all()
    for destination in destinations:
        params = {
            'fly_from': destination.fly_from,
            'fly_to': destination.fly_to,
            'date_from': date,
            'date_to': date,
            'partner': 'picky',
            'limit': 1,
            'sort': 'price',
            'asc': 1
        }
        r = requests.get(worker_settings.FLIGHTS_URL, params=params)
        print(r.url)
        content = r.text
        feed = json.loads(content)
        data = feed['data'][0]
        FlightsCache.objects.create(
            destination=destination,
            date=date,
            flight_id=data['id'],
            fly_duration=data['fly_duration'],
            city_from=data['cityFrom'],
            city_to=data['cityTo'],
            distance=data['distance'],
            price=data['price'],
            deep_link=data['deep_link'],
            token=data['booking_token']
        )
        print('ID: {}'.format(data['id']))


def validate_flights():
    """ Проводим валидацию по кэшу каждые 2 часа - отмечаем невалидные, отмечем что цена изменена """
    flights = FlightsCache.objects.all()
    for flight in flights:
        params = {"v": 2, "booking_token": flight.token}
        r = requests.get(worker_settings.FLIGHTS_VALIDATE_URL, params=params)
        content = r.text
        feed = json.loads(content)
        flights_invalid = feed.get('flights_invalid', 'false')
        flights_checked = feed.get('flights_checked', 'true')
        price_change = feed.get('price_change', 'false')

        if flights_checked == 'true':
            flight.checked = True
        if flights_invalid == 'false':
            flight.validate = True
        if price_change == 'true':
            flight.price_changed = True
        flight.save()





