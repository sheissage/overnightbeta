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
from OvernightWeb import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.landing_page),
	url(r'^get_news/', views.get_content),
    url(r'^showResult/', views.showSearchresult),
    url(r'^login/', views.loginUser),
    url(r'^authenticateUser/', views.authenticateUser),
    url(r'^logoutUser/', views.logout_user),
    url(r'^signup/', views.signup),
    url(r'^signupUser/', views.signupUser),
    url(r'^showBooking/', views.showBookingPage),
    url(r'^callPriceRefresh/', views.callPriceRefresh),
    url(r'^showBookingConfirmation/', views.showBookingConfirmation),
    url(r'^showUserProfile/', views.showUserProfile),
    url(r'^showUserProfileBookingHistory/', views.showUserProfileBookingHistory),
    url(r'^showUserProfileCards/', views.showUserProfileCards),
    url(r'^showUserProfileSettings/', views.showUserProfileSettings),
    url(r'^showSearchresultJakarta/', views.showSearchresultJakarta),
    url(r'^loadDashboard/', views.loadDash),
    url(r'^updateRoominfo/', views.updateRoomInfo),
    url(r'^manageContent/', views.manageContent),
    url(r'^createRoom/', views.createRoom),
    url(r'^createMerchant/', views.createMerchant),
    url(r'^logonMerchant/', views.logonMerchant),
    url(r'^loadMerchantLogin/', views.loadMerchantLogin),
    url(r'^managePackage/', views.managePackage),
    url(r'^createPackage/', views.createPackage),
    url(r'^merchantSignup/', views.merchantSignup),
    url(r'^uploadPics/', views.uploadPics),
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT,}),
]

