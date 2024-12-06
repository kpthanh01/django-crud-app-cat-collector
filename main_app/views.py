from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
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
class CatCreate(LoginRequiredMixin, CreateView):
  model = Cat
  fields = ['name', 'breed', 'description', 'age']

  # This is made because we have a User now and Cat is now related to a User
  # This inherited method is called when a
  # valid cat form is being submitted
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)
  
  success_url = '/cats/'

class CatUpdate(LoginRequiredMixin, UpdateView):
  model = Cat
  fields = ['breed', 'description', 'age']

class CatDelete(LoginRequiredMixin, DeleteView):
  model = Cat
  success_url = '/cats/'

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'
  success_url = '/toys/'

class ToyList(LoginRequiredMixin, ListView):
  model = Toy

class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys/'

class Home(LoginView):
  template_name = 'home.html'

# Define the home view function

# This home function is being replace by Home class-base-view
# def home(request):
#   # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
#   return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def cat_index(request):
  # Replacing this so that only the cat associated to a user will display
  #cats = Cat.objects.all()

  cats = Cat.objects.filter(user=request.user)
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

def signup(request):
  error_message = ''
  if request.method == 'POST':
      # This is how to create a 'user' form object
      # that includes the data from the browser
      form = UserCreationForm(request.POST)
      if form.is_valid():
          # This will add the user to the database
          user = form.save()
          # This is how we log a user in
          login(request, user)
          return redirect('cat-index')
      else:
          error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)
  # Same as: 
  # return render(
  #     request, 
  #     'signup.html',
  #     {'form': form, 'error_message': error_message}
  # )
