import requests
from requests.exceptions import RequestException
from datetime import datetime
from config_data import config

def search_destination(city):
    url = 'https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination'
    headers = {
        "x-rapidapi-host": "booking-com15.p.rapidapi.com",
        "x-rapidapi-key": config.RAPID_API_KEY
    }
    params = {
    "query": city
    }
    try:
        my_req = requests.get(url, headers=headers, params=params, timeout=10)
        my_req.raise_for_status()
        data = my_req.json()
        return data
    except RequestException as error:
        with open('log.txt','a',encoding='utf-8') as file:
            file.write(f'{datetime.now()}: При выполнении запроса к SearchDestination возникла ошибка. {error}\n')
        return None


def search_hotels(adults, children_age, min_price, max_price, dest_id, destination_type, check_in, check_out, search_mode):
    url = 'https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels'
    headers = {
        "x-rapidapi-host": "booking-com15.p.rapidapi.com",
        "x-rapidapi-key": config.RAPID_API_KEY
    }

    sort_options = {
        'lowprice': 'price',
        'guest_rating': 'bayesian_review_score',
        'bestdeal': 'distance'
}
    sort_by = sort_options[search_mode]

    params = {
        "adults": adults,
        "price_min": min_price,
        "price_max": max_price,
        "arrival_date" : check_in.strftime('%Y-%m-%d'),
        "departure_date": check_out.strftime('%Y-%m-%d'),
        "dest_id": dest_id,
        "search_type": destination_type.upper(),
        'sort_by': sort_by
    }
    if children_age:
        params['children_age'] = children_age
    try:
        my_req = requests.get(url, headers=headers, params=params, timeout=10)
        my_req.raise_for_status()
        data = my_req.json()
        return data
    except RequestException as error:
        with open('log.txt','a',encoding='utf-8') as file:
            file.write(f'{datetime.now()}: При выполнении запроса к SearchHotels возникла ошибка. {error}\n')
        return None

def get_hotel_description(hotel_id):

    url = 'https://booking-com15.p.rapidapi.com/api/v1/hotels/getDescriptionAndInfo'
    headers = {
        'x-rapidapi-host': 'booking-com15.p.rapidapi.com',
        'x-rapidapi-key': config.RAPID_API_KEY
    }
    params = {
        'hotel_id': hotel_id,
        'languagecode': 'ru'
    }
    try:
        my_req = requests.get(url, headers=headers, params=params, timeout=10)
        my_req.raise_for_status()
        data = my_req.json()
        return data
    except RequestException as error:
        with open('log.txt','a',encoding='utf-8') as file:
            file.write(f'{datetime.now()}: При выполнении запроса к getDescriptionAndInfo возникла ошибка. {error}\n')
        return None

def get_hotel_details(hotel_id, check_in, check_out):

    url = 'https://booking-com15.p.rapidapi.com/api/v1/hotels/getHotelDetails'

    headers = {
        'x-rapidapi-host': 'booking-com15.p.rapidapi.com',
        'x-rapidapi-key': config.RAPID_API_KEY
    }
    params = {
        "hotel_id": hotel_id,
        "arrival_date" : check_in.strftime('%Y-%m-%d'),
        "departure_date": check_out.strftime('%Y-%m-%d')
    }
    response = requests.get(url,headers=headers, params=params)
    data = response.json()
    return data

def get_sort_by(adults, children_age, dest_id, search_type, check_in, check_out):

    url = 'https://booking-com15.p.rapidapi.com/api/v1/hotels/getSortBy'
    headers = {
        'x-rapidapi-host': 'booking-com15.p.rapidapi.com',
        'x-rapidapi-key': config.RAPID_API_KEY
    }
    params = {
        'adults': adults,
        'dest_id': dest_id,
        'search_type': search_type.upper(),
        'arrival_date': check_in.strftime('%Y-%m-%d'),
        'departure_date': check_out.strftime('%Y-%m-%d')
    }

    if children_age:
        params['children_age'] = children_age

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    return response.json()