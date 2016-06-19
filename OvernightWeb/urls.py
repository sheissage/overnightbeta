"""OvernightWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from OverApp import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.landing_page),
	url(r'^get_news/', views.getContent),
    url(r'^search/', views.search),
    url(r'^login/', views.loginTraveller),
    url(r'^authenticateUser/', views.authenticateUser),
    url(r'^logoutUser/', views.logout_user),
    url(r'^signup/', views.travellerSignup),
    url(r'^showBooking/', views.showUserProfileBookingHistory),
    url(r'^callPriceRefresh/', views.callPriceRefresh),
    url(r'^showBookingConfirmation/', views.showBookingConfirmation),
    url(r'^showUserProfile/', views.showUserProfile),
    url(r'^showUserProfileBookingHistory/', views.showUserProfileBookingHistory),
    url(r'^showUserProfileCards/', views.showUserProfileCards),
    url(r'^showUserProfileSettings/', views.showUserProfileSettings),
    # url(r'^showSearchresultJakarta/', views.showSearchresult),
    url(r'^loadDashboard/', views.loadDash),
    url(r'^addAvailability/', views.addAvailability),
    url(r'^manageContent/', views.manageContent),
    url(r'^createRoom/', views.createRoom),
    url(r'^createMerchant/', views.createMerchant),
    url(r'^logonMerchant/', views.logonMerchant),
    url(r'^loadMerchantLogin/', views.loadMerchantLogin),
    url(r'^managePackage/', views.managePackage),
    url(r'^createPackage/', views.createPackage),
    url(r'^merchantSignup/', views.merchantSignup),
    url(r'^uploadPics/', views.uploadPics),
    url(r'^getRooms/', views.getRoomTypes),
    url(r'^getRoomInfo/', views.getRoomInfo),
    url(r'^getRoomAvailability/', views.getRoomAvailability),
    url(r'^getBookingOffers/', views.getBookingOffers),
    url(r'^signupPage2/', views.signupFirsttoSecond),
    url(r'^signupPage3/', views.createTaveller),
    url(r'^signupFinish/', views.createTravellerAddress),
    url(r'^signup/', views.signupFirsttoSecond),
    url(r'^dashboard/', views.hotelDashboardRedirect, name='hotel-dashboard'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

