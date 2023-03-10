from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from .models import Table, TableImage, Reservation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
from account.models import Profile
from django.utils.timezone import now
import datetime
import pytz 


def restaurant(request):
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, 'restaurant/index.html', context)


def table_detail(request, id, slug):
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
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    reservations = Reservation.objects.filter(customer=user)
    context = {'profile': profile, 'reservations': reservations }
    return render(request, 'restaurant/reservation_list.html', context)


@login_required(login_url='account/signin')
def reservation_edit(request, id):
    r = get_object_or_404(Reservation, id=id)
    table_images = TableImage.objects.filter(table=r.table)
    form = ReservationForm(instance=r)
    context = {'r': r, 'table_images': table_images, 'form': form}
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
    r = get_object_or_404(Reservation, id=id)
    r.delete()
    messages.success(request, f'You have successfully deleted your reservation of {r.table.title }.')
    return redirect('account:profile')
