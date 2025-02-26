from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login , logout
from .models import FarmerInput,Contact
from django.contrib import messages
from .middleware import auth,guest
import requests
import os
import json
import re
#from .middlewares import auth,guest


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username' : '' , 'password1' :'' , 'password2':''}
        form = UserCreationForm(initial= initial_data)
    return render(request, 'auth/register.html' , {'form' : form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data = {'username' : '' , 'password' :''}
        form = AuthenticationForm(initial= initial_data)
    return render(request, 'auth/login.html' , {'form' : form})  

def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    context = {"success" : False}
    if request.method== "POST":
        #print("this is post")

        name = request.POST['name']
        email = request.POST['email']
        desc = request.POST['desc']
        print(name,email,desc)

        ins = Contact( name = name, email= email,desc= desc)
        ins.save()
        context = {"success" : True}
        print(name,email,desc)

        messages.success(request, "Form successfully submitted!")  # Success message
        print('message added')
        return redirect('index')


    
    return render(request, 'index.html',context)


def dashboard(request):
    return render(request,'dashboard.html')


def step(request):
    return render(request,'steps.html')


def recommend_crop(request):
    if request.method == 'POST':
        land_dimensions = request.POST.get('land_dimensions')
        climate = request.POST.get('climate')
        soil_type = request.POST.get('soil_type')

        print(f"Received Data - Land Dimensions: {land_dimensions}, Climate: {climate}, Soil Type: {soil_type}")

        FarmerInput.objects.create(
            land_dimensions=land_dimensions,
            climate=climate,
            soil_type=soil_type
        )

        # Get the API key from environment variables
        gemini_api_key = os.environ.get('GEMINI_API_KEY')
        if not gemini_api_key:
            return render(request, 'error.html', {'error_message': "GEMINI_API_KEY not set in environment variables."})


        # Construct the API endpoint with the key
        # Construct the API endpoint with the key
        gemini_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_api_key}"


        # Construct the prompt for the Gemini API
        prompt = f"""
        Recommend a crop to grow given the following information in medium 10 steps:
        Land Dimensions: {land_dimensions}
        Climate: {climate}
        Soil Type: {soil_type}
        Please provide your answer in JSON format, including the following keys:
        - recommended_crop
        - steps
        - success_percent in %
        - estimated_cost in $
        """

        # Make the request to the Gemini API
        try:
            ai_response = requests.post(
                gemini_endpoint,
                json={
                    "contents": [
                        {
                            "parts": [{"text": prompt}]
                        }
                    ]
                }
            )
            ai_response.raise_for_status()  # Raise an exception for bad status codes

            # Extract the response content
            response_data = ai_response.json()
            response_text = response_data['candidates'][0]['content']['parts'][0]['text']
            print(f"Raw Gemini Response: {response_text}")
            # Try to parse response_text as json, if failed return error to the user.
            cleaned_response = re.sub(r'^```json\n|```$', '', response_text).strip()  # Updated regex

            print(f"Cleaned Response: {cleaned_response}")
            try:
                json_response = json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                print(f"An error occurred trying to parse api json response: {e}")
                return render(request, 'error.html', {'error_message': str(e)})

            # Process the response (assuming a JSON response as requested in the prompt)
            recommended_crop = json_response.get('recommended_crop')
            steps = json_response.get('steps')
            success_percent = json_response.get('success_percent')
            estimated_cost = json_response.get('estimated_cost')

            return render(request, 'recommendation.html', {
                'recommended_crop': recommended_crop,
                'steps': steps,
                'success_percent': success_percent,
                'estimated_cost': estimated_cost
            })
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the API request: {e}")
            return render(request, 'error.html', {'error_message': str(e)})
        except KeyError as e:
            print(f"An error occurred trying to find a key in the api json response: {e}")
            return render(request, 'error.html', {'error_message': str(e)})

    return render(request, 'input_form.html')

#cmd to activate gimini is : export GEMINI_API_KEY=AIzaSyD-r0oyE7b1EfkcGWC_t2SYsM0J2fjsYDk


def about_us(request):
    return render(request,'about_us.html')

def faq(request):
    return render(request,'faq.html')










