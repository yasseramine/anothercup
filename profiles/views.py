from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from cupboards.models import Cupboard, SavedCupboard

# Create your views here.


@login_required()
def my_cupboards(request, saved_cupboards):

# Actually will filter cupboards according to session user but for now
    saved_cupboards = SavedCupboard.objects.all()

    context = {
        "saved_cupboards": saved_cupboards
    }

    return render(request, 'profiles/my_cupboards.html', context)

