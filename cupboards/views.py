from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required

from .models import Cupboard, Material, Type, Image
from .forms import DesignForm, MaterialForm

# Create your views here.


def all_cupboards(request):
    """ A view to show all cupboards, including sorting and search queries """

    cupboards = Cupboard.objects.all()
    query = None
    type = None
    all_types = Type.objects.all()
    types = all_types
    sort = None
    direction = None

    if request.GET:

        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                cupboards = cupboards.annotate(lower_name=Lower('name'))

            if sortkey == 'price':
                sortkey = 'example_price'

            if sortkey == 'material':
                sortkey = 'material__name'

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
            type = Type.objects.filter(name__in=types)[0]
            
        print(type)

        if 'q' in request.GET:
            query = request.GET['q']

            if not query:
                messages.error(request, "Please enter some search criteria.")
                return redirect(reverse('cupboards'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            cupboards = cupboards.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'cupboards': cupboards,
        'search_term': query,
        'all_types': all_types,
        'type': type,
        'types': types,
        'current_sorting': current_sorting,
    }

    return render(request, 'cupboards/cupboards.html', context) 


def cupboard_details(request, cupboard_id):
    """ A view to show detailed cupdoard information and the user to select 
    their specifications and receive a quote"""

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)

    max_height = 2400
    max_width = 2400
    max_depth = 600
    min_depth = 150

    if cupboard.type.name == "cupboard":
        min_height = 400
        min_width = 400
    else:
        min_height = 200
        min_width = 200

    context = {
        'cupboard': cupboard,
        'max_height': max_height,
        'max_width': max_width,
        'max_depth': max_depth,
        'min_height': min_height,
        'min_width': min_width,
        'min_depth': min_depth
    }

    return render(request, 'cupboards/cupboard_details.html', context) 


def calculated_cupboard(request, cupboard_id):
    """ A view to calculate the cost of a cupboard after the user has entered their required dimensions and number of shelves in the form on the product_details template, then return an updated template showing the cost for those dimensions (dimensions also rendered back to them)"""

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)

    type = get_object_or_404(Type, pk=cupboard.type.id)

    material = get_object_or_404(Material, pk=cupboard.material.id)

    if request.method == "POST":
        height = int(request.POST.get("height"))
        width = int(request.POST.get("width"))
        depth = int(request.POST.get("depth"))
        shelves = int(request.POST.get("shelves"))

    price_per_mm2 = float(material.price_per_m2)/1000000
       
    """ Calculation.  Shelves are multiplied by 10 as there
    is a £10 cutting fee per shelf"""

    if type.name == "cupboard":
        area = (height*depth*2) + (height*width*2) + (width*depth*(2+shelves))
           
# or if shelving has not front
    else:
        area = (height*depth*2) + (height*width) + (width*depth*(2+shelves))
            
    cost = (area * price_per_mm2) + float(cupboard.design_surcharge) +(shelves*10)

    if float(area/10000) <= 732:
        postage = 10.00
    if 733 <= float(area/10000) <= 1488:
        postage = 20.00
    if 1489 <= float(area/10000) <= 2164:
        postage = 30.00
    if 2165 <= float(area/10000) <= 2880:
        postage = 40.00

    print(postage)

    H = height
    D = depth
    W = width
    S = shelves
    cost = round(cost, 2)
    code = f"{H}#{W}#{D}#{S}#{cost}#{postage}"

    max_height = 2400
    max_width = 2400
    max_depth = 600
    min_depth = 150

    if type.name == "cupboard":
        min_height = 400
        min_width = 400
    else:
        min_height = 200
        min_width = 200

    context = {
        'H': H,
        'D': D,
        'W': W,
        'S': S,
        'cost': cost,
        'cupboard': cupboard,
        'type': type,
        'code': code,
        'max_height': max_height,
        'max_width': max_width,
        'max_depth': max_depth,
        'min_height': min_height,
        'min_width': min_width,
        'min_depth': min_depth,
        'postage': postage
    }

    return render(request, 'cupboards/calculated_cupboard.html', context)


def cart_cupboard(request, cupboard_id, height, width, depth, shelves, price, postage):

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)

    type = get_object_or_404(Type, pk=cupboard.type.id)

    material = get_object_or_404(Material, pk=cupboard.material.id)


    H=height
    W = width
    D = depth
    S = shelves 
    cost = price
    postage = postage
    code = f"{H}#{W}#{D}#{S}#{cost}#{postage}"

    max_height = 2400
    max_width = 2400
    max_depth = 600
    min_depth = 150

    if type.name == "cupboard":
        min_height = 400
        min_width = 400
    else:
        min_height = 200
        min_width = 200

    context = {
        'H': H,
        'D': D,
        'W': W,
        'S': S,
        'cost': cost,
        'cupboard': cupboard,
        'type': type,
        'code': code,
        'max_height': max_height,
        'max_width': max_width,
        'max_depth': max_depth,
        'min_height': min_height,
        'min_width': min_width,
        'min_depth': min_depth,
        'postage': postage
    }

    return render(request, 'cupboards/calculated_cupboard.html', context)


@login_required
def add_design(request):
    """ Add a new design to the database"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you are not authorised to do this.')
        return redirect(reverse('home'))
   
    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES)
        if form.is_valid():
            cupboard = form.save()
            messages.success(request, 'Design successfully added.')
            return redirect(reverse('cupboard_details', args=[cupboard.id]))
        else:
            messages.error(request, 'Failed to add design. Please ensure the form is valid.')
    else:
        form = DesignForm()

    template = 'cupboards/add_design.html'

    context = {
        "form": form,
    }
    return render(request, template, context)


@login_required
def add_material(request):
    """ Add a new material to the database"""
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you are not authorised to do this.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material successfully added.')
            return redirect('materials')
        else:
            messages.error(request, 'Failed to add material. Please ensure the form is valid.')
    else:
        return redirect('materials')


def list_materials(request):
    """ A view to show more detailed information about te materials available and a link for admin to edit materials in the database"""

    materials = Material.objects.all()
    form = MaterialForm()

    context = {
        'materials': materials,
        'form': form
    }

    return render(request, 'cupboards/materials.html', context) 


@login_required
def edit_design(request, cupboard_id):
    """ Edit a cupboard or shelving unit design """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you are not authorised to do this.')
        return redirect(reverse('home'))

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES, instance=cupboard)
        if form.is_valid():
            form.save()
            messages.success(request, 'Design successfully updated.')
            return redirect(reverse('cupboard_details', args=[cupboard.id]))
        else:
            messages.error(request, 'Failed to update design. Please ensure the form is valid.')
    else:
        form = DesignForm(instance=cupboard)

    template = 'cupboards/edit_design.html'
    context = {
        'form': form,
        'cupboard': cupboard
    }
    return render(request, template, context)


@login_required
def edit_material(request, material_id):
    """ Edit a material """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you are not authorised to do this.')
        return redirect(reverse('home'))

    material = get_object_or_404(Material, pk=material_id)
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material info successfully updated.')
            return redirect(reverse('materials'))
        else:
            messages.error(request, 'Failed to update material. Please ensure the form is valid.')
    else:
        form = MaterialForm(instance=material)

    template = 'cupboards/edit_material.html'
    context = {
        'form': form,
        'material': material
    }
    return render(request, template, context)


@login_required
def delete_design(request, cupboard_id):
    """ Delete a design from the collection """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you are not authorised to do this.')
        return redirect(reverse('home'))

    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    cupboard.delete()
    messages.success(request, f'{cupboard.name} deleted.')
    return redirect(reverse('cupboards'))


@login_required
def delete_material(request, material_id):
    """ Delete a material from the database """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you are not authorised to do this.')
        return redirect(reverse('home'))
        
    material = get_object_or_404(Material, pk=material_id)
    material.delete()
    messages.success(request, f'{material.display_name} deleted.')

    return redirect(reverse('materials'))


# @login_required
# def add_image(request):


    
