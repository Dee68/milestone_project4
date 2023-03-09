from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from .models import Table, TableImage, Reservation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ReservationForm
import datetime


# Create your views here.


def restaurant(request):
    tables = Table.objects.all()
    context = {'tables': tables}
    return render(request, 'restaurant/index.html', context)


# @login_required(login_url='account/signin')
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
        reserve_start = datetime.datetime.strptime(reserve_start, '%m/%d/%Y %H:%M %p')
        reserve_end = datetime.datetime.strptime(reserve_end, '%m/%d/%Y %H:%M %p')
        case_1 = Reservation.objects.filter(table=table, reserve_start__lte=reserve_start, reserve_end__gte=reserve_start).exists()
        case_2 = Reservation.objects.filter(table=table, reserve_start__lte=reserve_end, reserve_end__gte=reserve_end).exists()
        case_3 = Reservation.objects.filter(table=table, reserve_start__gte=reserve_start, reserve_end__lte=reserve_end).exists()
        if case_1 or case_2 or case_3:
            messages.warning(request, 'This table is not available on your booking schedule.')
            return render(request, 'restaurant/table_detail.html')
        elif datetime.datetime.now() < reserve_start or datetime.datetime.now() < reserve_end:
            messages.error(request, 'You can not book from past,please check your inputs.')
            return render(request, 'restaurant/table_detail.html')
            
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


#@login_required(login_url='account/signin')
def reserve_table(request):

    # form = AvailabilityForm()
    # if request.method == 'POST':
    #     form = AvailabilityForm(request.POST)
    #     if form.is_valid():
    #         table_list = Table.objects.filter(table_type=form['table_type'])
    #         available_tables = []
    #         for t in table_list:
    #             if check_availability(t, form.cleaned_data['reserve_date'], form.cleaned_data['reserve_time']):
    #                 available_tables.append(t)
    #         if len(available_tables > 0):
    #             table = available_tables[0]
    #             reservation = Reservation.objects.create(
    #                 customer=request.user,
    #                 table=table,
    #                 reserve_date=form.cleaned_data['reserve_date'],
    #                 reserve_time=form.cleaned_data['reserve_time']
    #             )
    #             reservation.save()
    #             messages.success(request, 'You have successfully booked your table.')
    #             return HttpResponseRedirect('restaurant:home')
    #         else:
    #             messages.info(request, 'No available tables of this type.')
    #     else:
    #         messages.error(request, 'invalid input')
    # context = {'form': form}

    return render(request, 'restaurant/booking.html', context)
