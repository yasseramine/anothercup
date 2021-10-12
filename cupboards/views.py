from django.shortcuts import render
from .models import Cupboard

# Create your views here.


def all_cupboards(request):
    """ A view to show all cupboards, including sorting and search queries """

    cupboards = Cupboard.objects.all()

    context = {
        'cupboards': cupboards,
    }

    return render(request, 'cupboards/cupboards.html', context) 

