from django.shortcuts import render, redirect
import requests
from . models import City
from . forms import CityForm
from django.contrib import messages


# Home Page Function
def index(request):

    # Get the API url and key
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=315cc50b44b677d4f4c746d652aea81e'

    message_class = ''

    # Check if method is a POST request
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        # Check if form is valid
        if form.is_valid(): 
            # Get the value of the data
            new_city = form.cleaned_data['name']

            # Check if city already existed in the database or in your location
            city_count = City.objects.filter(name=new_city).count()

            # Not existing
            if city_count == 0:
                # Convert the result to json object
                r = requests.get(api_url.format(new_city)).json()

                if r['cod'] == 200:
                    # Authenticate and submit the data in the form to the database
                    form.save()
                    messages.success(request, f'{new_city} added successfully')
                    message_class = 'alert__message-success'
                else:
                    messages.error(request, f'{new_city} does not exist in the world')
                    message_class = 'alert__message-danger'
                    
            else:
                messages.error(request, f'{new_city} already existed in the database')
                message_class = 'alert__message-danger'

        else:
            messages.error(request, f'Something went wrong. Your city is not added')
            message_class = 'alert__message-danger'
   
    form = CityForm()

    # Query or Get all the cities in the database
    cities = City.objects.all()

    # Store the list of city weathers to be displayed on the page
    city_weather = []

    try:

        for city in cities:

            # Convert the result to json object
            r = requests.get(api_url.format(city)).json()
            
            # Store the json object into a python dictionary
            city_data = {
                'icon': r['weather'][0]['icon'],
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
            }

            # Add the values of city_data(Object) to the city_weater(list)
            city_weather.append(city_data)

    except Exception as e:
        pass

    # Pass the list value [] to the template or page
    context = {
        'city_weather': city_weather,
        'form': form,
        'message_class': message_class
    }
    return render(request, 'weather/index.html', context)


# Delete City Function
def delete_city(request, city_name):
    # Delete the city where the city name equals city_name
    City.objects.get(name=city_name).delete()
    return redirect('index')