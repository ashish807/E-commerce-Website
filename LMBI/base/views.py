from django.shortcuts import render


def landing(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'base/landing.html', context)


def about(request):
    context = {
        'title': 'About'
    }
    return render(request, 'base/about.html', context)
 

def test(request):
    context = {
        'title': 'TEST'
    }
    return render(request, 'test.html', context)


def btInfo(request):
    context = {
        'title': 'Blood Test Information'
    }

    return render(request, 'base/blood/bloodTestMain.html', context)

def cvoid19(request):
    context = {
        'title': 'Blood Test Information'
    }

    return render(request, 'base/blood/covid.html', context)

def cbc(request):
    context = {
        'title': 'Blood Test Information'
    }

    return render(request, 'base/blood/cbc.html', context)

def cholestrol(request):
    context = {
        'title': 'Blood Test Information'
    }

    return render(request, 'base/blood/cholestrol.html', context)