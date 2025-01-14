from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

import os

import pandas as pd
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib

from rest_framework.renderers import JSONRenderer
from security.serializers import AttackPercentageSerializer

# # sql injectction
# # Load your dataset
# data_sql = pd.read_csv(os.path.join(settings.BASE_DIR, 'ml_models/sql_injection_dataset.csv'))

# # Define the feature extractor
# vectorizer_sql = CountVectorizer(token_pattern=r'\b\w+\b')

# # Extract features
# X = vectorizer_sql.fit_transform(data_sql['Query'])
# y = data_sql['Label']

# # # Split the dataset
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# model_filename = os.path.join(settings.BASE_DIR, 'ml_models/sql_svm_model.joblib')   # Replace with the actual filename
# sql_svm_model = joblib.load(model_filename)

# # phishing 
# data_phishing = pd.read_csv(os.path.join(settings.BASE_DIR, 'ml_models/phishing_site_urls.csv'))


# # Define the feature extractor
# vectorizer_phishing = CountVectorizer(token_pattern=r'\b\w+\b')

# # Extract features
# X = vectorizer_phishing.fit_transform(data_phishing['URL'])
# # y = data_phishing['Label']

# # Load the trained model
# model_filename =  os.path.join(settings.BASE_DIR, 'ml_models/phishing_DT_model.joblib')   # Replace with the actual filename
# phishing_dt_model = joblib.load(model_filename)


# # attack percentage 
# attack_percentage_data = pd.read_csv(os.path.join(settings.BASE_DIR, 'ml_models/label_occurrences_kdd.csv'))

# # Convert the DataFrame to a list of dictionaries
# data_list = attack_percentage_data.to_dict(orient='records')

# # Serialize the data using the serializer
# serializer = AttackPercentageSerializer(data_list, many=True)




# new work started
def home(request):
    return render(request, 'sample.html')

def index(request):
    return render(request, 'index.html')

def investigation(request):
    return render(request, 'investigation.html')

def prediction(request):
    return render(request, 'prediction.html')

def user_awareness(request):
    return render(request, 'user_awareness.html')

def solutions(request):
    return render(request, 'charts.html')

import json

def json_data(request):
    # json_data = os.path.join( settings.BASE_DIR, 'json_data/cyberattack.json')
    with open(os.path.join( settings.BASE_DIR, 'json_data/cyberattack.json')) as json_file:
                data = json.load(json_file)
    return JsonResponse(data, safe=False)


def login_page(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username = email)
        if len(user_obj) == 0 :
            messages.warning(request, "Email is not registered")
            return HttpResponseRedirect(request.path_info)
        
        user_obj = authenticate(username = email, password = password)

        if not user_obj :
            messages.warning(request, "Password is wrong")
            return HttpResponseRedirect(request.path_info)
        
        if user_obj : 
            login(request, user_obj)
            print("login")
            return redirect('/dashboard')

    return render(request, 'login.html')


def register_page(request):

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        # phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, "Email is already registered")
            return HttpResponseRedirect(request.path_info)

        user_obj = User.objects.create(first_name = fname, last_name = lname, email= email, username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, "You are registered with CyberDashboard")
        messages.success(request, "Login With you Credentials")
        return redirect('/login')
    return render(request, 'register.html')


# @login_required
def logout_page(request):
    logout(request)
    messages.success(request, "You are Logged Out from Dashboard")
    return redirect('/')







# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from security.models import *
# from security.serializers import *

# @api_view(['GET'])
# def home(request):
#     return Response(serializer.data)


# @api_view(['GET', 'PUT'])
# def sql(request):
#     if request.method == "GET":
#         sql_accuracies = Accuracy_SQL.objects.all()
#         sql_accuracies = AccuracySQLSerializer(sql_accuracies, many=True)
#         return Response(sql_accuracies.data)
#     if request.method == "PUT":
#         data = request.data
#         sql_query = data.get('sql_query')
#         print(sql_query)
#         # Preprocess the user input using the same CountVectorizer
#         sql_query = vectorizer_sql.transform([sql_query])
#         prediction = sql_svm_model.predict(sql_query)
#         msg = "hello"
#         if prediction[0] == 1:
#             msg = "SQL Injection Attack Detected!"
#         else:
#             msg = "No SQL Injection Attack Detected."
#         print(msg)
#         data = {"message" : msg}
#         # return redirect('/check-phishing-msg/' + phishing)
#         return Response(data)



# @api_view(['GET', 'PUT'])
# def phishing(request):
#     if request.method == "GET":
#         phishing_accuracies = Accuracy_Phishing.objects.all()
#         phishing_accuracies = AccuracyPhishingSerializer(phishing_accuracies, many=True)
#         return Response(phishing_accuracies.data)
#     if request.method == "PUT":
#         data = request.data
#         url = data.get('url')
#         print(url)
#         # Preprocess the user input using the same CountVectorizer
#         url = vectorizer_phishing.transform([url])
#         prediction = phishing_dt_model.predict(url)
#         phishing = "hello"
#         if prediction[0] == 1:
#             phishing = "Phishing Attack Detected!"
#         else:
#             phishing = "No Phishing Attack Detected."
#         print(phishing)
#         data = {"message" : phishing}
#         # return redirect('/check-phishing-msg/' + phishing)
#         return Response(data)

