from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required

from .models import Cupboard, Material, Type
from .forms import DesignForm, MaterialForm

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
                messages.error(request, "Please enter some search criteria.")
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



def add_design_material(request):
    """A view just to render the page with forms to add a new design or new material"""

    form1 = DesignForm()
    form2 = MaterialForm()
    template = 'cupboards/add_design_material.html'

    context = {
        "form1": form1,
        "form2": form2
    }

    return render(request, template, context)


def add_design(request):
    """ Add a new design to the collection"""
    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Design successfully added.')
            return redirect('add_design_material')
        else:
            messages.error(request, 'Failed to add design. Please ensure the form is valid.')
    else:
        return redirect('add_design_material')


def add_material(request):
    """ Add a new material to the database"""
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material successfully added.')
            return redirect('add_design_material')
        else:
            messages.error(request, 'Failed to add material. Please ensure the form is valid.')
    else:
        return redirect('add_design_material')


def list_materials(request):
    """ A view to show more detailed information about te materials available and a link for admin to edit materials in the database"""

    materials = Material.objects.all()

    context = {
        'materials': materials
    }

    return render(request, 'cupboards/materials.html', context) 


def edit_design(request, cupboard_id):
    """ Edit a cupboard or shelving unit design """
    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    if request.method == 'POST':
        form = DesignForm(request.POST, request.FILES, instance=cupboard)
        if form.is_valid():
            form.save()
            messages.success(request, 'Design successfully updated.')
            return redirect(reverse('cupboards'))
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


def edit_material(request, material_id):
    """ Edit a material """
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


def delete_design(request, cupboard_id):
    """ Delete a design from the collection """
    cupboard = get_object_or_404(Cupboard, pk=cupboard_id)
    cupboard.delete()
    messages.success(request, 'Design deleted.')
    return redirect(reverse('cupboards'))


def delete_material(request, material_id):
    """ Delete a material from the database """
    material = get_object_or_404(Material, pk=material_id)
    material.delete()
    messages.success(request, 'Material deleted.')

    # Delete designs made of this material
    # Cupboard.objects.filter(material=material_id).delete()

    return redirect(reverse('materials'))
