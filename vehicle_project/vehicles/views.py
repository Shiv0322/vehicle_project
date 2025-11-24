from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Vehicle
from .forms import VehicleForm

def vehicle_list(request):
    search_query = request.GET.get('search', '')
    type_filter = request.GET.get('type', '')

    vehicles = Vehicle.objects.all().order_by('-created_at')

    if search_query:
        vehicles = vehicles.filter(
            Q(name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(registration_number__icontains=search_query)
        )

    if type_filter:
        vehicles = vehicles.filter(vehicle_type=type_filter)

    paginator = Paginator(vehicles, 5)  # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'type_filter': type_filter,
    }
    return render(request, 'vehicles/vehicle_list.html', context)


def vehicle_add(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicles/vehicle_form.html', {'form': form})


def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/vehicle_form.html', {'form': form})


def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    return redirect('vehicle_list')
