from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cupboards.models import Cupboard, SavedCupboard

# Create your views here.


@login_required
def my_cupboards(request):

    return render(request, 'profiles/my_cupboards.html', context)
