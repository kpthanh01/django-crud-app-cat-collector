from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Cat, Toy
from .forms import FeedingForm

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

class ToyCreate(CreateView):
  model = Toy
  fields = '__all__'
  success_url = '/toys/'

class ToyList(ListView):
  model = Toy

class ToyDetail(DetailView):
  model = Toy

class ToyUpdate(UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(DeleteView):
  model = Toy
  success_url = '/toys/'

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
  feeding_form = FeedingForm()
  return render(request, 'cats/detail.html', {
    'cat': cat,
    'feeding_form': feeding_form
  })

def add_feeding(request, cat_id):
  # create a ModelForm instance using the data in request.POST
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # don't save the form to the db until it has the cat_id assigned
    new_feeding = form.save(commit=False)
    new_feeding.cat_id = cat_id
    new_feeding.save()
  return redirect('cat-detail', cat_id=cat_id)