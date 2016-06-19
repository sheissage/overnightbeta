import re

from django.db.models import Q, Min
from OverApp.models import RoomInfo, HotelAvailability

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):

    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def build_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.

    '''
    query = None # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})

            if or_query:
                or_query = or_query |q
            else:
                or_query = q


        if query:
            query = query & or_query
        else:
            query = or_query
    return query

def get_lowest_price(pk):
    # include dates in the future

    default_price = RoomInfo.objects.filter(hotel_id=pk).aggregate(lowest=Min('ratePerNight'))
    season_price = HotelAvailability.objects.filter(hotel_id=pk).aggregate(lowest=Min('ratePerNight'))
    print default_price
    print season_price
    if not season_price.get('lowest'):
        return default_price.get('lowest')
    if default_price.get('lowest') < season_price.get('lowest') and default_price.get('lowest') != 0:
        return default_price.get('lowest')
    else:
        return season_price.get('lowest')


def generic_search(request, model, fields, query):
    """
    """

    query_string = query

    if not query_string:
        entries = model.objects.all()
    else:
        entry_query = build_query(query_string, fields)
        entries = model.objects.filter(entry_query)

    for entry in entries:
        entry.lowest = get_lowest_price(entry.pk)
        amenities = entry.hotelAmens.split(',')
        entry.hotelAmens = amenities
        rooms = entry.hotelRoomTypes.split(',')
        entry.hotelRoomTypes = rooms
        services = entry.hotelServices.split(',')
        entry.hotelServices = services


    return entries