from django.shortcuts import render

from worker.models import FlightsCache


def index(request):
    flights = FlightsCache.objects.all()
    context = {'data': flights}
    return render(request, 'index.html', context)
