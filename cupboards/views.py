from django.shortcuts import render, get_object_or_404
from .models import Cupboard

# Create your views here.


def all_cupboards(request):
    """ A view to show all cupboards, including sorting and search queries """

    cupboards = Cupboard.objects.all()

    context = {
        'cupboards': cupboards,
    }

    return render(request, 'cupboards/cupboards.html', context) 


def cupboard_details(request, cupboard_id):
    """ A view to show detailed cupdoard information and the user to select 
    their specifications and receive a quote"""

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)

    context = {
        'cupboard': cupboard,
    }

    return render(request, 'cupboards/cupboard_details.html', context) 
