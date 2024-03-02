from django.http import HttpResponse

from django.shortcuts import render
from django.http import HttpResponse
import requests
import pandas as pd

def fetch_menu(restaurant_id):
    try:
        url = f"https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=18.56&lng=73.95&restaurantId={restaurant_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        menu_data = response.json()
        return menu_data
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch menu data: {e}")
        return None

def extract_menu(menu_data):
    try:
        data = menu_data.get('data')
        menu_items = [
            x['card']['card'] for x in data['cards'][2]['groupedCard']['cardGroupMap']['REGULAR']['cards']
            if x['card']['card']['@type'] == 'type.googleapis.com/swiggy.presentation.food.v2.ItemCategory'
        ]

        menu_details = []
        for i in range(len(menu_items)):
            for item_card in menu_items[i]['itemCards']:
                dish_info = item_card['card']['info']
                dish_name = dish_info.get('name', None)
                price = dish_info.get('price', None) / 100 if 'price' in dish_info else None
                category = dish_info.get('category', None)
                description = dish_info.get('description', None)
                menu_details.append({'Name': dish_name, 'Price': price, 'Category': category, 'Description': description})
        
        return pd.DataFrame(menu_details)
    except KeyError as e:
        print(f"Failed to extract menu data: {e}")
        return None

def fetch_and_extract_menu(request):
    if request.method == 'GET':
        restaurant_id = request.GET.get('restaurant_id')
        if restaurant_id:
            menu_data = fetch_menu(restaurant_id)
            if menu_data:
                menu_df = extract_menu(menu_data)
                if menu_df is not None:
                    # Return CSV file as attachment
                    response = HttpResponse(menu_df.to_csv(index=False), content_type='csv')
                    response['Content-Disposition'] = 'attachment; filename="menu.csv"'
                    return response
                else:
                    return HttpResponse("Failed to extract menu data. Check the structure of the response.")
            else:
                return HttpResponse("Failed to fetch menu data.")
        else:
            return HttpResponse("Please provide a restaurant ID.")
    else:
        return HttpResponse("Invalid request method.")
