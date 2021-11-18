from django.shortcuts import render

# Create your views here.


def index(request):

    return render(request, 'home/index.html')


def about(request):

    return render(request, 'home/about.html')


def assembly(request):

    return render(request, 'home/assembly.html')


def contact(request):

    return render(request, 'home/contact.html')


def delivery(request):

    return render(request, 'home/delivery.html')


def pricing(request):

    return render(request, 'home/pricing.html')


def returns(request):

    return render(request, 'home/returns.html')