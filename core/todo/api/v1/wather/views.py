import requests
from django.http import JsonResponse
from django.views.decorators.cache import cache_page

@cache_page(60 * 20)
def get_weather_mashhad(request):
    api_key = '58bfd78f63cb69a80b9c1d782738b822'
    city = 'Mashhad'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
        }
        return JsonResponse(weather_info, safe=False)
    else:
        return JsonResponse({'error': 'Failed to fetch data'}, status=response.status_code)
