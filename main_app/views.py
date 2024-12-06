from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Cat

# Import HttpResponse to send text-based responses
# from django.http import HttpResponse  -- this is used temporarily to show a response before we start using html files

# Temporarily make a Cat class here to start and make a mock data the labs
# Later we will replace this with data from postgres and moving the Cat class to the model.py file
#
# class Cat:
#   def __init__(self, name, breed, description, age):
#     self.name = name
#     self.breed = breed
#     self.description = description
#     self.age = age

# cats = [
#   Cat('Lolo', 'tabby', 'Kinda rude.', 3),
#   Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
#   Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
#   Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
# ]

# Define classes
class CatCreate(CreateView):
  model = Cat
  fields = '__all__'
  success_url = '/cats/'

class CatUpdate(UpdateView):
  model = Cat
  fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
  model = Cat
  success_url = '/cats/'

# Define the home view function
def home(request):
  # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def cat_index(request):
  cats = Cat.objects.all()
  return render(request, 'cats/index.html', {'cats': cats})

def cat_detail(request, cat_id):
  cat = Cat.objects.get(id=cat_id)
  return render(request, 'cats/detail.html', {'cat': cat})
