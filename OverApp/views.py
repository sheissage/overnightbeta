from __future__ import unicode_literals
from django.shortcuts import render
import json
from searchModule import queryBuilder as qb
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
import django
from .models import HotelInfo, RoomInfo, Merchant, Package
import models
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse


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


def updateRoomInfo(request):
    if request.method == 'POST':
        params = request.POST
        roomType = params.get("roomType")
        date = params.get("start")
        price = params.get("price")
        discount = params.get('discount')
        destination = params.get("destination")

        merchant = Merchant.objects.get(user=request.user)
        hotel = HotelInfo.objects.get(merchant=merchant)

        roomobj = RoomInfo(
            Destination=destination, 
            roomType=roomType,
            date=date, 
            airportTransfer=price,
            ratePerNight=price, 
            discountPercent=discount,
            hotelTax=price, 
            serviceCharge=price,
            merchant=merchant,
            hotel=hotel
            )
        roomobj.save()

    roomdata = models.RoomInfo.objects.all().values()
    return render(request, 'hotelDashboard.html', {'roomdata': roomdata})


def managePackage(request):
    merchant = Merchant.objects.get(user=request.user)
    hotels = HotelInfo.objects.filter(merchant=merchant).values('hotelId', 'hotelName')
    context = {
        'hotels': hotels
    }
    return render(request, "managePackage.html", context)


def createPackage(request):
    if request.method == 'POST':
        print request.POST
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
        
        roomdata = RoomInfo.objects.filter(merchant=merchant)
        context = {
            'roomtypes': roomdata.values_list('roomType', flat=True).distinct('roomType'),
            'destinations': roomdata.values_list('destination', flat=True).distinct('destination')
        }
        return render(request, "hotelDashboard.html", context)


def createRoom(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        destination = request.POST['destination']
        name = request.POST['name']
        address = request.POST['address']
        amenities = request.POST['amenities']
        services = request.POST['services']
        roomtypes = request.POST['roomtype']

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
            merchant=merchant
        )

        hotel.save()

        ##################
        """ save rooms """
        ##################
        
        for room_type in room_types:
            room = RoomInfo(
                hotel=hotel, 
                merchant=merchant, 
                roomType=room_type.upper(), 
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

    roomdata = RoomInfo.objects.filter(merchant=hotel.merchant)
    context = {
        'roomtypes': roomdata.values_list('roomType', flat=True).distinct('roomType'),
        'destinations': roomdata.values_list('destination', flat=True).distinct('destination')
    }
    return render(request, "hotelDashboard.html", context)


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
        roomTypes = RoomInfo.objects.filter(hotel=hotel).values('pk', 'roomType')
        result = []

        for roomType in roomTypes:
            cache = {}
            cache['pk'] = roomType.get('pk')
            cache['roomType'] = roomType.get('roomType')
            result.append(cache)

        print result
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
                merchant = Merchant.objects.get(user=user)
                roomdata = RoomInfo.objects.filter(merchant=merchant)
                context = {
                    'roomtypes': roomdata.values_list('roomType', flat=True).distinct('roomType'),
                    'destinations': roomdata.values_list('destination', flat=True).distinct('destination')
                }
                return render(request, "hotelDashboard.html", context)
            return HttpResponse("User is not active")
        return HttpResponse("Invalid User")


def getMax():
    hotel = HotelInfo.objects.all().order_by('-created').first()
    if not hotel:
        return 0
    max_id = (hotel.hotelId).split('-')[1]

    return max_id


def signupUser(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        passwd = request.POST['passwd']
        repass = request.POST['repass']
        gender = request.POST['gender']
        country = request.POST['country']
        city = request.POST['city']
        street = request.POST['street']
        unit = request.POST['unit']
        zipcode = request.POST['zip']

        if repass == passwd:
            user = User.objects.create_user(
                username=email, email=email, password=passwd)
            user.first_name = fname
            user.last_name = lname
            user.save()
            # modUser=django.contrib.auth.models.AuthUser.objects.get(email=email)
            # modUser.first_name=fname
            # modUser.last_name=lname
            # modUser.save()
            if user is None:
                return HttpResponse("User Cannot Be Created")

            newTraveller = models.Traveller(fname=fname, lname=lname,
                                            email=email, gender=gender,
                                            unit=unit, streetAddr=street,
                                            city=city, zip=zipcode,
                                            country=country, homeAirport=city)
            newTraveller.save()
            subject, from_email, to = 'Welcome to Overnight.asia (beta)',
            'enquiry@overnight.asia', email
            text_content = 'Hello! ' + fname + \
                "\n Thank you for signing up as "\
                "a beta member of Overnight.asia."
            html_content = '<p>Hello! ' + fname + \
                '<br> Thank you for signing on '\
                '<strong>Overnight.asia</strong> .</p>'
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render(request, "login.html")


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


def showSearchresult(request):
    webquery = request.GET['searchbar']
    posarr, facilities = qb.associateSentiment(webquery=webquery)
    print(posarr)
    print(facilities)
    area = posarr[3]
    # fix out of index error
    data = models.HotelInfo.objects.all()
    hoteldata = [item for item in data if item[3] != none]
    return render(request, 'searchresults_common.html', {'data': hoteldata})


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
