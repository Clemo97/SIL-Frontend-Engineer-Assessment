import os
import requests
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.http import HttpResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from . import models
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def sign_in(request):
    return render(request, 'sign_in.html')


@csrf_exempt
def auth_receiver(request):
    print("Auth:", request)
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, google_requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )
    except ValueError:
        return HttpResponse(status=403)

    # In a real app, I'd also save any new user here to the database. 
    # See below for a real example I wrote for Photon Designer.
    request.session['user_data'] = user_data
    
    print("User Data:", user_data)

    return redirect('sign_in')

@method_decorator(csrf_exempt, name='dispatch')
class AuthGoogle(APIView):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    def post(self, request, *args, **kwargs):
        try:
            user_data = self.get_google_user_data(request)
        except ValueError:
            return HttpResponse("Invalid Google token", status=403)

        email = user_data["email"]
        user, created = models.User.objects.get_or_create(
            email=email, defaults={
                "username": email, "sign_up_method": "google",
                "first_name": user_data.get("given_name"),
            }
        )

        # Add any other logic, such as setting a http only auth cookie as needed here.
        return HttpResponse(status=200)

    @staticmethod
    def get_google_user_data(request: HttpRequest):
        token = request.POST['credential']
        return id_token.verify_oauth2_token(
            token, google_requests.Request(), os.environ['GOOGLE_OAUTH_CLIENT_ID']
        )


def sign_out(request):
    del request.session['user_data']
    return redirect('sign_in')



# @login_required
def get_albums(request):
    url = "https://jsonplaceholder.typicode.com/albums"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        albums = response.json()
        return render(request, 'user_albums.html', {'albums': albums})
    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'error': str(e)})
    

# def users_list(request):
#     return render(request, 'users.html')
