from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from .models import Table, TableImage, Reservation, Review, Food, Drink
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm, ReviewForm
from account.models import Profile
from django.utils.timezone import now
import datetime
import pytz


def restaurant(request):
    '''
        a view to display the home page
        gets all the tables in the restaurant
    '''
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, 'restaurant/index.html', context)


def table_detail(request, id, slug):
    '''
        A view to display an individual table
        with a form to reserve it if user is logged in
    '''
    table = get_object_or_404(Table, id=id, slug=slug)
    table_images = TableImage.objects.filter(table=table)
    form = ReservationForm()
    context = {'table': table, 'table_images': table_images, 'form': form}
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        customer = request.user
        reserve_start = request.POST['reserve_start']
        reserve_end = request.POST['reserve_end']
        if reserve_start == '' or reserve_end == '':
            messages.error(request, 'Enter your desires times for reservation.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        reserve_start = datetime.datetime.strptime(reserve_start, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        reserve_end = datetime.datetime.strptime(reserve_end, '%m/%d/%Y %I:%M %p').replace(tzinfo=pytz.utc)
        case_1 = Reservation.objects.filter(table=table, reserve_start__lte=reserve_start, reserve_end__gte=reserve_start).exists()
        case_2 = Reservation.objects.filter(table=table, reserve_start__lte=reserve_end, reserve_end__gte=reserve_end).exists()
        case_3 = Reservation.objects.filter(table=table, reserve_start__gte=reserve_start, reserve_end__lte=reserve_end).exists()
        if case_1 or case_2 or case_3:
            messages.warning(request, 'This table is not available on your booking schedule.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        elif now() > reserve_start or now() > reserve_end or reserve_start > reserve_end:
            messages.error(request, 'You can not book from past,please check your inputs.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))         
        else:
            reservation = Reservation.objects.create(
               customer=customer,
               table=table,
               reserve_start=reserve_start,
               reserve_end=reserve_end
            )
            reservation.save()
            messages.success(request, 'You have successfully booked the table.')
            return redirect('restaurant:home')
    return render(request, 'restaurant/table_detail.html', context)


@login_required(login_url='account/signin')
def reservation_list(request):
    '''
        This view displays a list of reservation
        done by a logged in user if any.
    '''
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    reservations = Reservation.objects.filter(customer=user)
    context = {'profile': profile, 'reservations': reservations }
    return render(request, 'restaurant/reservation_list.html', context)


@login_required(login_url='account/signin')
def reservation_edit(request, id):
    '''
        This view edits/update an individual reservation
        of a logged in user.
    '''
    r = get_object_or_404(Reservation, id=id)
    table_images = TableImage.objects.filter(table=r.table)
    form = ReservationForm(instance=r)
    context = {'r': r, 'table_images': table_images, 'form': form}
    if now() > r.reserve_end:
        messages.error(request, 'Your reservation has expired.')
        return redirect('restaurant:reservations')
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=r)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated your reservation.')
            return redirect('restaurant:reservations')
        else:
            messages.error(request, 'Please enter valid values to input fields.')
            return redirect('restaurant:reservations')
    return render(request, 'restaurant/reservation_edit.html', context)


@login_required(login_url='account/signin')
def reservation_delete(request, id):
    '''
        This view enables a logged in user to delete 
        his/her reservation.
    '''
    r = get_object_or_404(Reservation, id=id)
    r.delete()
    messages.success(request, f'You have successfully deleted your reservation of {r.table.title }.')
    return redirect('account:profile')


def review_list(request):
    '''
        This view displays all the reviews made by users
    '''
    reviews = Review.objects.all()
    context = {'reviews': reviews}
    return render(request, 'restaurant/review_list.html', context)


def review_table(request, id, slug):
    '''
        This view enables a logged in user to
        give a review of a table
    '''
    form = ReviewForm()
    table = get_object_or_404(Table, id=id, slug=slug)
    reviews = table.table_review.all()
    context = {'table': table, 'reviews': reviews, 'form': form}
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            content = request.POST.get('content')
            author = request.user
            review = Review.objects.create(table=table, author=author, content=content)
            review.save()
            messages.success(request, 'Your review is added successfully.')
            return redirect('restaurant:home')
        else:
            messages.error(request, 'Something went wrong')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'restaurant/table_review.html', context)


def login_user(request):
    '''
        This view enables users to sign in 
        to view pages allowed only for logged in users.
    '''
    return render(request, 'restaurant/login_user.html')


def food_list(request):
    '''
        This view displays the food menu items.
    '''
    desserts = Food.objects.filter(food_type='dessert')
    foods = Food.objects.filter(food_type='main')
    context = {'desserts': desserts, 'foods': foods}
    return render(request, 'restaurant/food_list.html', context)


def drink_list(request):
    '''
        This view displays the drink menu items.
    '''
    wines = Drink.objects.filter(drink_type='wines')
    beers = Drink.objects.filter(drink_type='beers')
    cocktails = Drink.objects.filter(drink_type='cocktails')
    context = {'wines': wines, 'beers': beers, 'cocktails': cocktails}
    return render(request, 'restaurant/drink_list.html', context)
