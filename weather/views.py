from typing import Any
from datetime import datetime
from random import randrange
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views import View
from django.shortcuts import render, redirect
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.permissions import IsAuthenticated

from .models import WeatherEntity
from .repositories import WeatherRepository
from .serializers import WeatherSerializer
from .forms import WeatherForm
from .exceptions import WeatherException

class WeatherView(View):

    # authentication_classes = [JWTAuthentication]
    # permissions_classes = [IsAuthenticated]
    authenticate = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        # try:
        #     user, _ = self.authentication_classes[0].authenticate(request=request)
        #     request.user = user
        #     self.authenticate = True
        # except Exception as e:
        #     pass

        # continua a execução da classe, indo para o método correspondente
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.getAll())
            serializer = WeatherSerializer(data=weathers, many=True)
            if (serializer.is_valid()):
                modelWeather = serializer.save()
                objectReturn = {"weathers":modelWeather}
            else:
                objectReturn = {"error":serializer.errors}
        except WeatherException as e:
            objectReturn = {"error":e.message}

        if not self.authenticate:
            objectReturn["errorAuth"] = "Usuário não autenticado"

        print(objectReturn)
  
        return render(request, "home.html", objectReturn)
    
class WeatherGenerate(View):
    
    # authentication_classes = [JWTAuthentication]
    authenticate = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        # try:
        #     user, _ = self.authentication_classes[0].authenticate(request=request)
        #     request.user = user
        #     self.authenticate = True
        # except Exception as e:
        #     return redirect('Weather View')
        
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        repository = WeatherRepository(collectionName='weathers')
        weather = WeatherEntity(
            temperature=randrange(start=17, stop=40),
            date=datetime.now(),
            city='Sorocaba'
        )
        serializer = WeatherSerializer(data=weather.__dict__)
        if (serializer.is_valid()):
            repository.insert(serializer.data)
        else:
            print(serializer.errors)

        return redirect('Weather View')
    
class WeatherReset(View):

    # authentication_classes = [JWTAuthentication]
    authenticate = False

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        # try:
        #     user, _ = self.authentication_classes[0].authenticate(request=request)
        #     request.user = user
        #     self.authenticate = True
        # except Exception as e:
        #     return redirect('Weather View')
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request): 
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteAll()

        return redirect('Weather View')
    
class WeatherInsert(View):

    # authentication_classes = [JWTAuthentication]
    authenticate = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        # try:
        #     user, _ = self.authentication_classes[0].authenticate(request=request)
        #     request.user = user
        #     self.authenticate = True
        # except Exception as e:
        #     return redirect('Weather View')
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        weatherForm = WeatherForm()

        return render(request, "form.html", {"form":weatherForm})
    
    def post(self, request):
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            serializer = WeatherSerializer(data=weatherForm.data)
            if (serializer.is_valid()):
                repository = WeatherRepository(collectionName='weathers')
                repository.insert(serializer.data)
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect('Weather View')
    

class WeatherEdit(View):
    def get(self, request, id):
        repository = WeatherRepository(collectionName='weathers')
        weather = repository.getByID(id)
        weatherForm = WeatherForm(initial=weather)

        return render(request, "form_edit.html", {"form":weatherForm, "id":id})
    
    def post(self, request, id):
        weatherForm = WeatherForm(request.POST)
        if weatherForm.is_valid():
            serializer = WeatherSerializer(data=weatherForm.data)
            serializer.id = id
            if (serializer.is_valid()):
                repository = WeatherRepository(collectionName='weathers')
                repository.update(serializer.data, id)
            else:
                print(serializer.errors)
        else:
            print(weatherForm.errors)

        return redirect('Weather View')




class WeatherDelete(View):

    # authentication_classes = [JWTAuthentication]
    authenticate = True

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        # try:
        #     user, _ = self.authentication_classes[0].authenticate(request=request)
        #     request.user = user
        #     # self.authenticate = True
        # except Exception as e:
        #     return redirect('Weather View')
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        repository = WeatherRepository(collectionName='weathers')
        repository.deleteByID(id)

        return redirect('Weather View')
    

class WeatherFilter(View):
    def post(self, request):
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')

        repository = WeatherRepository(collectionName='weathers')
        try:
            weathers = list(repository.get(data))
            serializer = WeatherSerializer(data=weathers, many=True)
            if (serializer.is_valid()):
                modelWeather = serializer.save()
                objectReturn = {"weathers":modelWeather}
            else:
                objectReturn = {"error":serializer.errors}
        except WeatherException as e:
            objectReturn = {"error":e.message}