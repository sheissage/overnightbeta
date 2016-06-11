from OverApp import models
from django.template import RequestContext

def associateSentiment(webquery):
    splitArr=webquery.split(" ")
    processedArr=splitArr[splitArr.index("in"):]
    destination=models.HotelInfo.objects.all().values('Destination')
    area=models.HotelInfo.objects.all().values('Area')
    amenities=models.HotelInfo.objects.all().values('HotelAmens')
    # services=models.HotelInfo.objects.all().values('HotelServices')
    # rooms=models.HotelInfo.objects.all().values('HotelRoomTypes')
    servArr=splitArr[splitArr.index("with"):]

    return processedArr,servArr
