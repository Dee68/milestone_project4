from django.shortcuts import render, get_object_or_404
from account.models import Profile

# Create your views here.


def restaurant(request):
    return render(request, 'restaurant/index.html')
