from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required

from .models import Cupboard, Material, Type, SavedCupboard

# Create your views here.


def all_cupboards(request):
    """ A view to show all cupboards, including sorting and search queries """

    cupboards = Cupboard.objects.all()
    query = None
    types = None
    sort = None
    direction = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                cupboards = cupboards.annotate(lower_name=Lower('name'))
            if sortkey == 'type':
                sortkey = 'type__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            cupboards = cupboards.order_by(sortkey)
            
        if 'type' in request.GET:
            types = request.GET['type'].split(',')
            cupboards = cupboards.filter(type__name__in=types)
            types = Type.objects.filter(name__in=types)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('cupboards'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            cupboards = cupboards.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'cupboards': cupboards,
        'search_term': query,
        'current_types': types,
        'current_sorting': current_sorting,
    }

    # Insert some sort of form validation for entering dimensions,
    # with max and min values

    return render(request, 'cupboards/cupboards.html', context) 


def cupboard_details(request, cupboard_id):
    """ A view to show detailed cupdoard information and the user to select 
    their specifications and receive a quote"""

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)

    context = {
        'cupboard': cupboard,
    }

    return render(request, 'cupboards/cupboard_details.html', context) 


def calculated_cupboard(request, cupboard_id, material_id, type_id):
    """ A view to calculate the cost of a cupboard after the user has entered their required dimensions and number of shelves in the form on the product_details template, then return an updated template showing the cost for those dimensions (dimensions also rendered back to them)"""

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    material = get_object_or_404(Material, pk=material_id)
    type = get_object_or_404(Type, pk=type_id)

    if request.method == "POST":
        height_in_mm = float(request.POST.get("height")) * 10
        width_in_mm = float(request.POST.get("width")) * 10
        depth_in_mm = float(request.POST.get("depth")) * 10
        shelves = int(request.POST.get("shelves"))
        price_per_mm2 = float(material.price_per_m2)/1000000
       
    """ Calculation.  Shelves are multiplied by 10 as there
    is a £10 cutting fee per shelf"""

    if type.name == "cupboard":
        cost = ((
            (height_in_mm*depth_in_mm*2) + (height_in_mm*width_in_mm*2) +
            (width_in_mm*depth_in_mm*(2+shelves)
            )) * price_per_mm2) + float(cupboard.design_surcharge) + (
                shelves*10)
# or if shelving has not front
    else:
        cost = ((
            (height_in_mm*depth_in_mm*2) + (height_in_mm*width_in_mm) +
            (width_in_mm*depth_in_mm*(2+shelves)
              )) * price_per_mm2) + float(cupboard.design_surcharge) + (
                shelves*10)

    H = height_in_mm/10
    D = str(depth_in_mm/10)
    W = str(width_in_mm/10)
    S = str(shelves)
    cost = round(cost, 2)
    code = f"{H}#{W}#{D}#{S}#{cost}"

    context = {
        'H': H,
        'D': D,
        'W': W,
        'S': S,
        'cost': cost,
        'cupboard': cupboard,
        'type': type,
        'code': code
    }

    return render(request, 'cupboards/calculated_cupboard.html', context)


@login_required
def save_cupboard(request, cupboard_id, H, W, D, S, cost, code):

    redirect_url = request.POST.get('redirect_url')

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    saved_cupboard = {
        'user': request.user,
        'cupboard': cupboard,
        'height': H,
        'width': W,
        'depth': D,
        'shelves': S,
        'cost': cost,
        'code': code
    }

# check if user has already saved this cupboard:

    users_cupboards = list(SavedCupboard.objects.filter(user=request.user))
    if code in users_cupboards:
        # messages.info(request, message)(request, f"You have already saved this cupboard")
        return redirect('redirect_url')

    else:
        SavedCupboard.objects.create(**saved_cupboard)
  

    context = {
        "saved_cupboard": saved_cupboard
    }

    return redirect('cart/view_cart')
