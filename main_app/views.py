from django.shortcuts import render

# Import HttpResponse to send text-based responses
# from django.http import HttpResponse  -- this is used temporarily to show a response before we start using html files

class Cat:
  def __init__(self, name, breed, description, age):
    self.name = name
    self.breed = breed
    self.description = description
    self.age = age

cats = [
  Cat('Lolo', 'tabby', 'Kinda rude.', 3),
  Cat('Sachi', 'tortoiseshell', 'Looks like a turtle.', 0),
  Cat('Fancy', 'bombay', 'Happy fluff ball.', 4),
  Cat('Bonk', 'selkirk rex', 'Meows loudly.', 6)
]

# Define the home view function
def home(request):
  # return HttpResponse('<h1>Hello ᓚᘏᗢ</h1>')
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

def cat_index(request):
  return render(request, 'cats/index.html', {'cats': cats})