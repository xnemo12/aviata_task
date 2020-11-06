from datetime import date, timedelta

from celery import shared_task

from worker.models import FlightsCache
from worker.utils import get_flights, validate_flights, daterange


@shared_task
def update_cache():
    """ очищаем кэш и берем новые данные на месяц вперед"""
    FlightsCache.objects.all().delete()

    current_date = date.today()
    days_after = (date.today() + timedelta(days=30))

    for dt in daterange(current_date, days_after):
        try:
            get_flights(dt.strftime("%d/%m/%Y"))
        except:
            print("Data is not valid")


@shared_task
def validate_cache():
    validate_flights()
