from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from django import template

register=template.Library()

# Create your models here.


class HotelInfo(models.Model):
    HotelId = models.TextField(db_column='hotelId', blank=True,primary_key=True)  # Field name made lowercase.
    Destination = models.TextField(db_column='destination', blank=True, null=True)  # Field name made lowercase.
    Area = models.TextField(db_column='area', blank=True, null=True)  # Field name made lowercase.
    HotelName = models.TextField(db_column='hotelName', blank=True, null=True)  # Field name made lowercase.
    HotelAddress = models.TextField(db_column='address', blank=True, null=True)  # Field name made lowercase. HotelAmenities(JSON)
    HotelAmens = models.TextField(db_column='hotelAmenities', blank=True, null=True)  # Field name made lowercase.
    HotelServices = models.TextField(db_column='hotelServices', blank=True, null=True)  # Field name made lowercase.
    HotelRoomTypes = models.TextField(db_column='hotelRoomTypes', blank=True, null=True)  # Field name made lowercase.(JSON)
    PriceByDate = models.TextField(db_column='priceByDate', blank=True, null=True)  # Field name made lowercase.(From)
    HotelPictures = models.ImageField(upload_to="hotelPics/",default="hotelPics/avatar.jpg")  # Field name made lowercase.(HTML)
    HotelDescription = models.TextField(db_column='hotelDescription',blank=True, null=True) # Field name made lowercase.
    ownerId = models.TextField(db_column='ownerId',default='Overnightasia')

    class Meta:
        managed = True
        db_table = 'HotelInfo'

    @register.filter(name='serviceparse')
    def serviceparse(val):
        return val.split(",")


class RoomInfo(models.Model):
    roomId = models.AutoField(primary_key=True)
    roomType = models.TextField(db_column="roomType",blank=True)
    hotelName = models.TextField(db_column='hotelName', blank=True, null=True)  # Field name made lowercase.
    destination = models.TextField(db_column='destination', blank=True, null=True)  # Field name made lowercase.
    date = models.DateField(null=True,blank=True)
    ratePerNight = models.FloatField(default=0)
    airportTransfer = models.FloatField(default=0)
    discountPercent = models.FloatField(default=0)
    hotelTax = models.FloatField(default=0)
    serviceCharge = models.FloatField(default=0)
    ownerId = models.TextField(db_column='ownerId',default='Overnightasia')


    class Meta:
        managed = True
        db_table = 'RoomInfo'

    @register.filter(name='roomparse')
    def roomparse(val):
        return val.split(",")


class Package(models.Model):
    packageId = models.AutoField(primary_key=True)
    packageName = models.TextField(db_column='packageName')
    packageDesc = models.TextField(db_column="description")
    price = models.FloatField(db_column="price",default=0)
    roomType = models.TextField(db_column="roomType", blank=True)
    serviceList = models.TextField(db_column="serviceList")
    discountPercent = models.FloatField(default=0)
    hotelTax = models.FloatField(default=0)
    serviceCharge = models.FloatField(default=0)

    class Meta:
        managed = True
        db_table = 'PackageInfo'

    @register.filter(name='packageparse')
    def packageparse(val):
        return val.split(",")


class Traveller(models.Model):
    location = models.TextField(default= " ")
    fname = models.TextField(default= " ")
    lname = models.TextField(default= " ")
    email = models.TextField(default= " ")
    phone = models.TextField(default=" ")
    homeAirport = models.TextField(default=" ")
    streetAddr = models.TextField(default=" ")
    unit = models.TextField(default=" ")
    city = models.TextField(default= " ")
    state = models.TextField(default= " ")
    zip = models.TextField(default=" ")
    country = models.TextField(default=" ")
    gender = models.TextField(default="male")
    travellerPictures = models.ImageField(upload_to="travellerPics/", default="img/300x300.png")  # Field name made lowercase.(HTML)

    class Meta:
        managed = True
        db_table = "Traveller"


class Merchant(models.Model):
    merchantID = models.AutoField(primary_key=True)
    merchantName = models.TextField(db_column='merchantname')
    email = models.TextField(default=" ")
    phone = models.TextField(default=" ")
    streetAddr = models.TextField(default=" ")
    unit = models.TextField(default=" ")
    city = models.TextField(default=" ")
    state = models.TextField(default=" ")
    zip = models.TextField(default=" ")
    country = models.TextField(default=" ")

    class Meta:
        managed=True
        db_table="Merchant"
