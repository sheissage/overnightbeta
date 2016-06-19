from __future__ import unicode_literals

import django
import json
import time

from searchModule import queryBuilder as qb
from .models import HotelInfo, RoomInfo, Merchant, Package, HotelAvailability, Traveller
import models
from .utils import generic_search

###################
""" Dajngo libs"""
###################
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Q


# Create your views here.

def landing_page(request):
    return render(request, 'landingpage.html')


def loginTraveller(request):
    return render(request, 'login.html')


def travellerSignup(request):
    return render(request, 'signup.html')


def merchantSignup(request):
    return render(request, 'merchantSignup.html')


def loadMerchantLogin(request):
    return render(request, 'merchantLogin.html')


def loadDash(request):
    roomData = models.RoomInfo.objects.all().values()
    print("before max")
    getMax()
    print("After max")
    print(roomData)
    return render(request, 'hotelDashboard.html', {'roomdata': roomData})


def getContent(request):
    print("here")
    res = ''
    if request.method == 'POST':
        params = request.POST
        val = params.get('search_keyword')
        print(val)

        print("outside")
    # return HttpResponse(json.dumps({'data': res}),
    # content_type="application/json")
    return render(request, 'landingpage.html', {'data': res})


def showSearchResult(request):
    return render(request, 'searchresults_common.html')


def uploadPage(request):
    return render(request, 'uploadPics.html')


def manageContent(request):
    return render(request, 'manageContent.html')


def showBookingConfirmation(request):
    return render(request, 'bookingconfirmation.html')


def showUserProfile(request):
    return render(request, 'user-profile.html')


def showUserProfileBookingHistory(request):
    return render(request, 'user-profile-booking-history.html')


def showUserProfileCards(request):
    return render(request, 'user-profile-cards.html')


def showUserProfileSettings(request):
    return render(request, "user-profile-settings.html")


def addAvailability(request):
    if request.method == 'POST':
        params = request.POST

        room_pk = int(params.get("roomType"))
        hotel_pk = params.get('hotel')

        start = params.get("start")
        end = params.get("end")

        airportTransport = params.get('airporttransport')
        serviceCharge = params.get('servicecharge')
        
        price = params.get("price")
        discount = params.get('discount')
        hotelTax = params.get('hoteltax')

        price_type = params.get('roomPriceType')

        pattern = '%Y-%m-%d'
        start_epoch = int(time.mktime(time.strptime(start, pattern)))
        end_epoch = int(time.mktime(time.strptime(end, pattern)))

        merchant = Merchant.objects.get(user=request.user)
        hotel = HotelInfo.objects.get(merchant=merchant, pk=hotel_pk)
        room = RoomInfo.objects.get(hotel=hotel, pk=room_pk)
        print price_type
        if price_type == 'default':
            room.ratePerNight = float(price)
            room.airportTransfer = float(airportTransport)
            room.discountPercent = float(discount)
            room.hotelTax = float(hotelTax)
            room.serviceCharge = float(serviceCharge)
            room.save()

            return redirect('hotel-dashboard')

        #####################################################
        """ check if date availability is already present """
        #####################################################
        availabilities = HotelAvailability.objects.filter(
            merchant=merchant,
            hotel=hotel,
            room=room
        )

        for availability in availabilities:
            date_range = range(availability.start, availability.end)
            if start_epoch in date_range or end_epoch in date_range:
                return HttpResponse('Invalid - Overlapping Seasonal Rates')


        availability = HotelAvailability(
            start=start_epoch, 
            end=end_epoch,
            discountPercent=float(discount),
            hotelTax=float(hotelTax),
            serviceCharge=float(serviceCharge),
            airportTransfer=float(airportTransport),
            ratePerNight=float(price),
            merchant=merchant,
            hotel=hotel,
            room=room
        )
        availability.save()

    return redirect('hotel-dashboard')


def managePackage(request):
    merchant = Merchant.objects.get(user=request.user)
    hotels = HotelInfo.objects.filter(merchant=merchant).values('hotelId', 'hotelName')
    context = {
        'hotels': hotels
    }
    return render(request, "managePackage.html", context)


def createPackage(request):
    if request.method == 'POST':
        name = request.POST['name']
        packagedesc = request.POST['packagedesc']
        price = request.POST['price']
        services = request.POST['services']
        room_pk = int(request.POST['roomType'])
        hotel = request.POST['hotel']

        merchant = Merchant.objects.get(user=request.user)
        hotel = HotelInfo.objects.get(merchant=merchant, pk=hotel)

        room = RoomInfo.objects.get(merchant=merchant, hotel=hotel, pk=room_pk)

        package = models.Package(
            packageName=name, 
            packageDesc=packagedesc,
            price=float(price),
            roomType=room.roomType, 
            serviceList=services,
            merchant=merchant,
            hotel=hotel,
            room=room
            )
        package.save()
        
        return redirect('hotel-dashboard')


def createRoom(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        destination = request.POST['destination']
        name = request.POST['name']
        address = request.POST['address']
        amenities = request.POST['amenities']
        services = request.POST['services']
        roomtypes = request.POST['roomtype']
        currency = request.POST['currency']

        maxindex = int(getMax()) + 1
        
        hotelId = destination + '-' + str(maxindex)
        room_types = roomtypes.split(',')

        merchant = Merchant.objects.get(user=request.user)
        
        ##################
        """ save hotel """
        ##################

        hotel = HotelInfo(
            hotelName=name,
            hotelId=hotelId, 
            destination=destination,
            hotelAddress=address, 
            hotelAmens=amenities,
            hotelServices=services,
            hotelRoomTypes=roomtypes,
            merchant=merchant,
            currency=currency
        )

        hotel.save()

        ##################
        """ save rooms """
        ##################
        
        for room_type in room_types:
            room = RoomInfo(
                hotel=hotel, 
                merchant=merchant, 
                roomType=room_type.upper().strip(), 
                destination=destination,
                ratePerNight=0,
                discountPercent=0, airportTransfer=0,
                serviceCharge=0, hotelTax=0
            )

            room.save()

        request.session['sess_hotelId'] = hotelId

    return render(request, 'uploadPics.html', {"data": hotelId})

def uploadPics(request):
    hotelId = request.session['sess_hotelId']
    hotel = HotelInfo.objects.get(hotelId=hotelId)
    hotel.hotelPictures = request.FILES['hotelImage']
    hotel.save()

    return redirect('hotel-dashboard')


def createMerchant(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        repass = request.POST['repass']

        if repass == password:
            user = User.objects.create_user(
                username=email, email=email, password=password)
            user.first_name = fname
            user.last_name = lname
            user.save()

            merchant = Merchant(
                user=user,
                merchantName=user.first_name + ' ' + user.last_name,
                email=user.email
            )
            merchant.save()

            if user is None:
                return HttpResponse("Merchant Cannot be created")

            # subject, from_email, to = "Welcome to " + \
            #     "Overnight.asia (beta)", 'enquiry@overnight.asia', email
            # text_content = 'Thank you for signing up as a partner. ' + \
            #     fname+"\n You're one of the #Overnight20 partners."
            # html_content = '<p>Thank you for signing up as a partner.</p>'
            # msg = EmailMultiAlternatives(
            #     subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            return render(request, 'merchantLogin.html')
        return render(request, "merchantSignup.html",
                      {"data": "Passwords do not match"})

def getRoomTypes(request):
    if request.method == 'GET' and request.is_ajax:
        hotelId = request.GET.get('hotelId', '')
        hotel = HotelInfo.objects.get(hotelId=hotelId)
        roomTypes = RoomInfo.objects.filter(hotel=hotel)
        result = []

        for roomType in roomTypes:
            cache = {}
            cache['pk'] = roomType.pk
            cache['roomType'] = roomType.roomType
            
            result.append(cache)
        return JsonResponse(result, safe=False)

def getBookingOffers(request):
    if request.method == 'GET':
        hotelId = request.GET.get('hotelId', '')
        start = request.GET.get('start', '')
        end = request.GET.get('end', '')

        merchant = Merchant.objects.get(user=request.user)
        hotel = HotelInfo.objects.get(hotelId=hotelId)

        response = {}

        packages = Package.objects.filter(hotel=hotel, merchant=merchant, is_deleted=False, is_active=True)
        dates = HotelAvailability.objects.filter(hotel=hotel)\
            .filter(Q(start__range=(start, end)) | Q(end__range=(start, end)))
        rooms = RoomInfo.objects.filter(hotel=hotel)

        #######################
        """ get packages """
        #######################

        result = []
        for package in packages:
            cache = {}
            cache['name'] = package.packageName
            cache['description'] = package.packageDesc
            cache['room'] = package.roomType
            cache['service'] = package.serviceList
            cache['discount'] = package.discountPercent
            cache['tax'] = package.hotelTax
            cache['servicecharge'] = package.serviceCharge
            cache['airporttransfer'] = package.airportTransfer
            cache['pk'] = package.pk
            result.append(cache)

        response['packages'] = result

        #######################
        """    get promos   """
        #######################

        result = []
        for date in dates:
            start = int(time.strftime('%b %d %Y', time.localtime(date.start)))
            end = int(time.strftime('%b %d %Y', time.localtime(date.end)))
            cache['service'] = date.serviceList
            cache['discount'] = date.discountPercent
            cache['tax'] = date.hotelTax
            cache['servicecharge'] = date.serviceCharge
            cache['airporttransfer'] = date.airportTransfer
            cache['room'] = date.room.roomType
            cache['pk'] = date.pk
            result.append(cache)

        response['promos'] = result

        #######################
        """    get defaults   """
        #######################

        result = []
        for room in rooms:
            cache = {}
            cache['room'] = room.roomType
            cache['price'] = room.ratePerNight
            cache['service'] = room.serviceList
            cache['discount'] = room.discountPercent
            cache['tax'] = room.hotelTax
            cache['servicecharge'] = room.serviceCharge
            cache['airporttransfer'] = room.airportTransfer
            cache['room'] = date.pk
            
            result.append(cache)

        response['defaults'] = result

        return JsonResponse(result, safe=False)

def getBookingDetails(request):
    if request.method == 'POST':
        merchant = Merchant.objects.get(user=request.user)
        booking_type = request.POST['type']
        pk = request.POST['pk']

        cache = {}

        if booking_type == 'package':
            package = Package.objects.get(merchant=merchant, pk=pk)

            cache['name'] = package.packageName
            cache['description'] = package.packageDesc
            cache['room'] = package.roomType
            cache['service'] = package.serviceList
            cache['discount'] = package.discountPercent
            cache['tax'] = package.hotelTax
            cache['servicecharge'] = package.serviceCharge
            cache['airporttransfer'] = package.airportTransfer
        elif booking_type == 'promo':
            date = HotelAvailability.objects.get(merchant=merchant, pk=pk)

            cache['service'] = date.serviceList
            cache['discount'] = date.discountPercent
            cache['tax'] = date.hotelTax
            cache['servicecharge'] = date.serviceCharge
            cache['airporttransfer'] = date.airportTransfer
            cache['room'] = date.room.roomType
            cache['pk'] = date.pk
        else:
            room = RoomInfo.objects.filter(hotel=hotel, pk=pk)
            cache['room'] = room.roomType
            cache['price'] = room.ratePerNight
            cache['service'] = room.serviceList
            cache['discount'] = room.discountPercent
            cache['tax'] = room.hotelTax
            cache['servicecharge'] = room.serviceCharge
            cache['airporttransfer'] = room.airportTransfer
            cache['room'] = date.pk

def getRoomInfo(request):
    if request.method == 'GET' and request.is_ajax:
        merchant = Merchant.objects.get(user=request.user)
        roomId = request.GET.get('roomId', '')

        room = RoomInfo.objects.get(merchant=merchant, pk=roomId)

        # result = []
        cache = {}
        cache['ratePerNight'] = room.ratePerNight
        cache['airportTransfer'] = room.airportTransfer
        cache['discountPercent'] = room.discountPercent
        cache['hotelTax'] = room.hotelTax
        cache['serviceCharge'] = room.serviceCharge
        # result.append(cache)
        return JsonResponse(cache, safe=False)

def getRoomAvailability(request):
    if request.method == 'GET' and request.is_ajax:
        merchant = Merchant.objects.get(user=request.user)
        roomId = request.GET.get('roomId', '')
        start =  request.GET.get('start', '')
        end =  request.GET.get('end', '')

        room = RoomInfo.objects.get(merchant=merchant, pk=roomId)

        dates = HotelAvailability.objects.filter(room=room)\
            .filter(Q(start__range=(start, end)) | Q(end__range=(start, end)))

        result = []
        for date in dates:
            cache = {}
            start = int(time.strftime('%d', time.localtime(date.start)))
            end = int(time.strftime('%d', time.localtime(date.end)))
            if start > end:
                end = 31

            cache['start'] = start
            cache['end'] = end
            cache['rate'] = date.ratePerNight
            result.append(cache)
        return JsonResponse(result, safe=False)

def logonMerchant(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)
                try:
                    merchant = Merchant.objects.get(user=user)
                except:
                    return HttpResponse("Invalid User")
                return redirect('hotel-dashboard')
            return HttpResponse("User is not active")
        return HttpResponse("Invalid User")


def hotelDashboardRedirect(request):
    merchant = Merchant.objects.get(user=request.user)
    hotels = HotelInfo.objects.filter(merchant=merchant).values('hotelId', 'hotelName')
    context = {
        'hotels': hotels
    }
    return render(request, "hotelDashboard.html", context, content_type="text/html")


def getMax():
    hotel = HotelInfo.objects.all().order_by('-created').first()
    if not hotel:
        return 0
    max_id = (hotel.hotelId).split('-')[1]

    return max_id

def authenticateUser(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["passwd"]
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                resp = landing_page(request)
                return resp

def signupFirsttoSecond(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        
        context = {
            'firstname': firstname,
            'lastname': lastname
        }
        return render(request, 'signup2.html',  context)

def createTaveller(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        
        if password == repassword:
            try:
                user = User.objects.create_user(
                    username=email, email=email, password=password)
                user.first_name = firstname
                user.last_name = lastname
                user.save()
            except:
                return HttpResponse('User email already exists')

            traveller = Traveller(
                fname=firstname, 
                lname=lastname,
                email=email,
                gender=gender,
                user=user
            )
            traveller.save()

            # subject, from_email, to = 'Welcome to Overnight.asia (beta)',
            # 'enquiry@overnight.asia', email
            # text_content = 'Hello! ' + fname + \
            #     "\n Thank you for signing up as "\
            #     "a beta member of Overnight.asia."
            # html_content = '<p>Hello! ' + fname + \
            #     '<br> Thank you for signing on '\
            #     '<strong>Overnight.asia</strong> .</p>'
            # msg = EmailMultiAlternatives(
            #     subject, text_content, from_email, [to])
            # msg.attach_alternative(html_content, "text/html")
            # msg.send()

            context = {
                'user': traveller.pk
            }

            return render(request, 'signup3.html',  context)
        else:
            return HttpResponse('Passwords Do not match')

def createTravellerAddress(request):
    if request.method == 'POST':
        country = request.POST['country']
        city = request.POST['city']
        street = request.POST['street']
        unit = request.POST['unit']
        zipcode = request.POST['zip']

        pk = int(request.POST['user'])

        try:
            traveller = Traveller.objects.get(pk=pk)
            traveller.country = country
            traveller.city = city
            traveller.streetAddr = street
            traveller.unit = unit
            traveller.zip = zipcode

            traveller.save()

            return render(request, 'landingpage.html')
        except Exception as e:
            print e
            return HttpResponse('Something wrong')



def search(request):
    webquery = request.GET.get('searchbar')
    
    MODEL_MAP = {
        HotelInfo: ['destination', 'area', 'hotelName', 'hotelAddress', 'hotelAmens', 'hotelServices', 'hotelDescription', 'hotelRoomTypes',]
    }
    objects = []

    for model,fields in MODEL_MAP.iteritems():
        objects+=generic_search(request, model, fields, webquery)
        
    context = {
        'hotels': objects,
        'count': len(objects),
        'query': webquery
    }
    return render(request, 'searchresults_common.html', context)

def showeResults(request):
    pass

def showBookingdetails(request):
    hotelName = request.GET.get("hotelName")
    request.session["sess_hotelName"] = request.GET.get("hotelName")
    hoteldata = models.HotelInfo.objects.all().filter(
        HotelName=hotelName).values()
    print(hotelName)
    print(hoteldata)
    roomdata = models.RoomInfo.objects.all().filter(
        HotelName=hotelName).values()
    print(roomdata)
    return render(request, 'bookingdetails.html',
                  {'hoteldata': hoteldata, 'roomdata': roomdata})


def callPriceRefresh(request):
    hotelName = request.session['sess_hotelName']
    roomType = request.GET.get('roomType')
    hoteldata = models.HotelInfo.objects.all().filter(
        HotelName=hotelName).values()
    pricebydate = models.RoomInfo.objects.all().filter(
        HotelName=hotelName, roomType=roomType).values('ratePerNight')
    roomdata = models.RoomInfo.objects.all().filter(
        HotelName=hotelName).values()
    print(roomdata)
    return render(request, 'bookingdetails.html',
                  {'hoteldata': hoteldata, 'roomdata': roomdata})


def logout_user(request):
    logout(request)
    request.user = None
    return render(request, "landingpage.html")