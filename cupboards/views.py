from django.shortcuts import render, get_object_or_404
from .models import Cupboard, Material

# Create your views here.


def all_cupboards(request):
    """ A view to show all cupboards, including sorting and search queries """

    cupboards = Cupboard.objects.all()

    context = {
        'cupboards': cupboards,
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


def calculated_cupboard(request, cupboard_id, material_id):
    """ A view to calculate the cost of a cupboard after the user has entered their required dimensions and number of shelves in the form on the product_details template, then return an updated template showing the cost for those dimensions (dimensions also rendered back to them)"""

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    material = get_object_or_404(Material, pk=material_id)

    # methods = ["GET", "POST"]
    if request.method == "POST":
        height_in_mm = float(request.POST.get("height")) * 10
        width_in_mm = float(request.POST.get("width")) * 10
        depth_in_mm = float(request.POST.get("depth")) * 10
        shelves = int(request.POST.get("shelves"))
        price_per_mm2 = float(material.price_per_m2)/1000000

    print(height_in_mm)
    print(width_in_mm)
    print(depth_in_mm)
    print(shelves)
    print(price_per_mm2)
    print(cupboard.name)
    print(material)

       
    """ Calculation.  Shelves are multiplied by 10 as there
    is a £10 cutting fee per shelf"""

    if cupboard.type == cupboard:
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

    context = {
        'H': height_in_mm/10,
        'D': str(depth_in_mm/10),
        'W': str(width_in_mm/10),
        'S': str(shelves),
        'cost': round(cost, 2),
        'cupboard': cupboard
    }

    return render(request, 'cupboards/calculated_cupboard.html', context) 
