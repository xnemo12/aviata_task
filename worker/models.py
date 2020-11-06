from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_time = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True


class Airport(BaseModel):
    code = models.CharField(_('Airport code'), max_length=3)
    name = models.CharField(_('Airport name'), max_length=50)

    class Meta:
        verbose_name = _('Airport')
        verbose_name_plural = _('Airports')

    def __str__(self):
        return self.code


class Destination(BaseModel):
    fly_from = models.ForeignKey(Airport, related_name='destinations_from', null=True, on_delete=models.SET_NULL)
    fly_to = models.ForeignKey(Airport, related_name='destinations_to', null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = _('Destination')
        verbose_name_plural = _('Destinations')

    def __str__(self):
        return self.fly_from.code + '-' + self.fly_to.code


class FlightsCache(BaseModel):
    destination = models.ForeignKey(Destination, related_name='caches', null=True, on_delete=models.SET_NULL)
    date = models.CharField(_('Date'), max_length=255)
    flight_id = models.CharField(_('Flight ID'), max_length=100)
    fly_duration = models.CharField(_('Fly duration'), max_length=100)
    city_from = models.CharField(_('City from'), max_length=100)
    city_to = models.CharField(_('City to'), max_length=100)
    distance = models.CharField(_('Distance'), max_length=100)
    price = models.CharField(_('Price'), max_length=100)
    deep_link = models.TextField(_('Link'))
    token = models.TextField(_('Token'))
    checked = models.BooleanField(_('Checked flight?'), default=False)
    validate = models.BooleanField(_('Valid flight?'), default=False)
    price_changed = models.BooleanField(_('Price changed'), default=False)
