from django.shortcuts import render
from .models import Design

# Create your views here.


def all_designs(request):
    """ A view to show all designs, including sorting and search queries """

    designs = Design.objects.all()

    context = {
        'designs': designs,
    }

    return render(request, 'designs/designs.html', context) 
# Create your views here.
