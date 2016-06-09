from __future__ import unicode_literals
from django.shortcuts import render
import json
from searchModule import queryBuilder as qb
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
import django
import models
from django.core.mail import EmailMultiAlternatives


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

# api call to alchemy to get content


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
        print(params)
        roomType = params.get("roomType")
        date = params.get("start")
        price = params.get("price")
        discount = params.get('discount')
        destination = params.get("destination")
        roomobj = models.RoomInfo(Destination=destination, roomType=roomType,
                                  date=date, airportTransfer=price,
                                  ratePerNight=price, discountPercent=discount,
                                  hoteltax=price, servicecharge=price)
        roomobj.save()

    roomdata = models.RoomInfo.objects.all().values()
    return render(request, 'hotelDashboard.html', {'roomdata': roomdata})


def managePackage(request):
    roomdata = models.RoomInfo.objects.all().values('roomType')
    return render(request, "managePackage.html", {'data': roomdata})


def createPackage(request):
    if request.method == 'POST':
        name = request.POST['name']
        packagedesc = request.POST['packagedesc']
        price = request.POST['price']
        services = request.POST['services']
        roomType = request.POST['roomType']

        package = models.Package(
            packagename=name, packagedesc=packagedesc,
            price=price, roomType=roomType, serviceList=services)
        package.save()
        packageResponse = managePackage(request)

        return packageResponse


def createRoom(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        destination = request.POST['destination']
        name = request.POST['name']
        address = request.POST['address']
        amenities = request.POST['amenities']
        services = request.POST['services']
        roomtypes = request.POST['roomtype']
        maxindex = getMax()+1
        print('maxindex')
        hotelId = destination+"-"+str('maxindex')
        roomarr = roomtypes.split(",")
        username = request.user
        print('username')
        for each in roomarr:
            room = models.RoomInfo(HotelName=name, date='2016-06-01',
                                   ownerId=request.user, roomType=each.upper(
                                   ), Destination=destination,
                                   ratePerNight=0, packagePrice=0,
                                   discountPercent=0, airTransfer=0,
                                   serviceCharges=0, tax=0)
            room.save()

        hotel = models.HotelInfo(HotelID=hotelId, Destination=destination,
                                 HotelAddress=address, HotelAmens=amenities,
                                 HotelServices=services)
        hotel.save()
        request.session['sess_hotelId'] = hotelId
    return render(request, 'uploadPics.html', {"data": hotelId})
    # return HttpResponse(destination+name+address+amenities+services+maxindex)


def uploadPics(request):
    hotelId = request.session['sess_hotelId']
    hotel = models.HotelInfo.objects.get(HotelID=hotelId)
    hotel.HotelPictures = request.FILES['hotelImage']
    hotel.save()
    roomdata = models.Roominfo.objects.filter(ownerId=request.user).values()
    return render(request, "hotelDashboard.html", {'roomdata': roomdata})


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
            # modUser=django.contrib.auth.models.AuthUser.objects.get(email=email)
            # modUser.first_name=fname
            # modUser.last_name=lname
            # modUser.save()
            if user is None:
                return HttpResponse("Merchant Cannot be created")
            subject, from_email, to = "Welcome to " + \
                "Overnight.asia (beta)", 'enquiry@overnight.asia', email
            text_content = 'Thank you for signing up as a partner. ' + \
                fname+"\n You're one of the #Overnight20 partners."
            html_content = '<p>Thank you for signing up as a partner.</p>'
            msg = EmailMultiAlternatives(
                subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return render(request, 'merchantLogin.html')
        return render(request, "merchantSignup.html",
                      {"data": "Passwords do not match"})


def logonMerchant(request):
    request.context = RequestContext(request)
    if request.method == 'POST':
        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                print(request.user)
                roomdata = models.RoomInfo.objects.filter(
                    ownerId=user).values()
                return render(request, "hotelDashboard.html",
                              {'roomdata': roomdata})
            return HttpResponse("User is not active")
        return HttpResponse("Invalid User")


def getMax():
    idarr = []
    allIds = models.HotelInfo.objects.all().order_by(
        "HotelID").values("HotelID")
    for each in allIds:
        idarr.append(int(each['HotelID'].split("-")[1]))
    return max(idarr)

# def jsonify(val,type):
#     initstr='['
#     valarr=val.split(",")
#     for each in valarr:


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
