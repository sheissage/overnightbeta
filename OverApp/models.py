from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django import template
from django.contrib.auth.models import User

register=template.Library()

# Create your models here.

class Merchant(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    merchantId = models.AutoField(primary_key=True)
    merchantName = models.CharField(max_length=5120, blank=False, null=False)
    email = models.CharField(max_length=5120, blank=False, null=False)
    phone = models.CharField(max_length=5120, blank=True, null=True)
    streetAddr = models.CharField(max_length=5120, blank=True, null=True)
    unit = models.CharField(max_length=5120, blank=True, null=True)
    city = models.CharField(max_length=5120, blank=True, null=True)
    state = models.CharField(max_length=5120, blank=True, null=True)
    zip = models.CharField(max_length=5120, blank=True, null=True)
    country = models.CharField(max_length=5120, blank=True, null=True)
    user = models.ForeignKey(User, unique=True)

    class Meta:
        managed=True
        verbose_name_plural = 'Merchant'

class HotelInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    hotelId = models.TextField(blank=False, primary_key=True)  # Field name made lowercase.
    destination = models.CharField(max_length=5120, blank=True, null=True) # Field name made lowercase.
    area = models.CharField(max_length=5120, blank=True, null=True) # Field name made lowercase.
    hotelName = models.CharField(max_length=5120, blank=True, null=True)  # Field name made lowercase.
    hotelAddress = models.CharField(max_length=5120, blank=True, null=True)  # Field name made lowercase. HotelAmenities(JSON)
    hotelAmens = models.CharField(max_length=5120, blank=True, null=True)  # Field name made lowercase.
    hotelServices = models.CharField(max_length=5120, blank=True, null=True)  # Field name made lowercase.
    hotelRoomTypes = models.CharField(max_length=5120, blank=True, null=True)  # Field name made lowercase.(JSON)
    priceByDate = models.CharField(max_length=5120, blank=True, null=True)  # Field name made lowercase.(From)
    hotelPictures = models.ImageField(upload_to="hotelPics/",default="hotelPics/avatar.jpg")  # Field name made lowercase.(HTML)
    hotelDescription = models.CharField(max_length=5120, blank=True, null=True)# Field name made lowercase.
    # ownerId = models.TextField(db_column='ownerId',default='Overnightasia')
    currency = models.CharField(max_length=3, default='USD')
    merchant = models.ForeignKey('OverApp.Merchant')

    class Meta:
        managed = True
        verbose_name_plural = 'HotelInfo'

    @register.filter(name='serviceparse')
    def serviceparse(val):
        return val.split(",")


class RoomInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    roomId = models.AutoField(primary_key=True)
    roomType = models.CharField(max_length=5120, blank=True, null=True)# Field name made lowercase.
    destination = models.CharField(max_length=5120, blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(null=True,blank=True)
    ratePerNight = models.FloatField(default=0)
    airportTransfer = models.FloatField(default=0)
    discountPercent = models.FloatField(default=0)
    hotelTax = models.FloatField(default=0)
    serviceCharge = models.FloatField(default=0)
    # ownerId = models.TextField(db_column='ownerId',default='Overnightasia')
    merchant = models.ForeignKey('OverApp.Merchant')
    hotel = models.ForeignKey('OverApp.HotelInfo')


    class Meta:
        managed = True
        verbose_name_plural = 'RoomInfo'

    @register.filter(name='roomparse')
    def roomparse(val):
        return val.split(",")


class Package(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    packageId = models.AutoField(primary_key=True)
    packageName = models.CharField(max_length=5120, blank=True, null=True)
    packageDesc = models.CharField(max_length=5120, blank=True, null=True)
    price = models.FloatField(db_column="price",default=0)
    currency = models.CharField(max_length=5, blank=True, null=True)
    roomType = models.CharField(max_length=5120, blank=True, null=True)
    serviceList = models.CharField(max_length=5120, blank=True, null=True)
    discountPercent = models.FloatField(default=0)
    hotelTax = models.FloatField(default=0)
    serviceCharge = models.FloatField(default=0)
    hotel = models.ForeignKey('OverApp.HotelInfo')
    merchant = models.ForeignKey('OverApp.Merchant')
    room = models.ForeignKey('OverApp.RoomInfo')

    class Meta:
        managed = True
        verbose_name_plural = 'Package'

    @register.filter(name='packageparse')
    def packageparse(val):
        return val.split(",")

class HotelAvailability(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    start = models.IntegerField()
    end = models.IntegerField()
    discountPercent = models.FloatField(default=0)
    hotelTax = models.FloatField(default=0)
    serviceCharge = models.FloatField(default=0)
    airportTransfer = models.FloatField(default=0)
    ratePerNight = models.FloatField(default=0)
    hotel = models.ForeignKey('OverApp.HotelInfo')
    merchant = models.ForeignKey('OverApp.Merchant')
    room = models.ForeignKey('OverApp.RoomInfo')

    class Meta:
        managed = True
        verbose_name_plural = 'HotelAvailability'


class Traveller(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=5120, blank=True, null=True)
    fname = models.CharField(max_length=5120, blank=True, null=True)
    lname = models.CharField(max_length=5120, blank=True, null=True)
    email = models.CharField(max_length=5120, blank=True, null=True)
    phone = models.CharField(max_length=5120, blank=True, null=True)
    homeAirport = models.CharField(max_length=5120, blank=True, null=True)
    streetAddr = models.CharField(max_length=5120, blank=True, null=True)
    unit = models.CharField(max_length=5120, blank=True, null=True)
    city = models.CharField(max_length=5120, blank=True, null=True)
    state = models.CharField(max_length=5120, blank=True, null=True)
    zip = models.CharField(max_length=5120, blank=True, null=True)
    country = models.CharField(max_length=5120, blank=True, null=True)
    gender = models.CharField(max_length=64, default='male')
    travellerPictures = models.ImageField(upload_to="travellerPics/", default="img/300x300.png")  # Field name made lowercase.(HTML)
    user = models.ForeignKey(User, unique=True)

    class Meta:
        managed = True
        verbose_name_plural = 'Traveller'

class BookingInfo(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    start = models.IntegerField()
    end = models.IntegerField()
    days = models.IntegerField()
    checkin = models.IntegerField()
    checkout = models.IntegerField()
    totalRate = models.IntegerField()
    is_promo = models.BooleanField(default=False)
    is_package = models.BooleanField(default=False)
    discountPercent = models.FloatField(default=0)
    hotelTax = models.FloatField(default=0)
    serviceCharge = models.FloatField(default=0)
    airportTransfer = models.FloatField(default=0)
    hotel = models.ForeignKey('OverApp.HotelInfo')
    merchant = models.ForeignKey('OverApp.Traveller')
    room = models.ForeignKey('OverApp.RoomInfo')
    promo = models.ForeignKey('OverApp.HotelAvailability', blank=True, null=True)
    package = models.ForeignKey('OverApp.Package', blank=True, null=True)

    class Meta:
        managed = True
        verbose_name_plural = 'BookingInfo'

