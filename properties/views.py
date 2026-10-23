from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PropertyForm
from .models import Category, Property, PropertyImage

SORT_OPTIONS = {
    'new': '-created_at',
    'cheap': 'price',
    'expensive': '-price',
}


def home(request):
    properties = Property.objects.filter(is_active=True).select_related('category').order_by('-created_at')[:6]
    return render(request, 'properties/home.html', {
        'properties': properties,
        'categories': Category.objects.all(),
    })


def property_list(request):
    qs = Property.objects.filter(is_active=True).select_related('category')

    q = request.GET.get('q', '').strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(address__icontains=q))

    deal_type = request.GET.get('deal_type')
    if deal_type in ('sale', 'rent'):
        qs = qs.filter(deal_type=deal_type)

    category = request.GET.get('category')
    if category and category.isdigit():
        qs = qs.filter(category_id=category)

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min and price_min.isdigit():
        qs = qs.filter(price__gte=price_min)
    if price_max and price_max.isdigit():
        qs = qs.filter(price__lte=price_max)

    rooms = request.GET.get('rooms')
    if rooms in ('1', '2', '3'):
        qs = qs.filter(rooms=rooms)
    elif rooms == '4':
        qs = qs.filter(rooms__gte=4)

    sort = request.GET.get('sort', 'new')
    qs = qs.order_by(SORT_OPTIONS.get(sort, '-created_at'))

    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'properties/property_list.html', {
        'properties': page_obj,
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'q': q,
        'current_rooms': rooms or '',
        'current_sort': sort,
        'current_category': category or '',
        'price_min': price_min or '',
        'price_max': price_max or '',
        'current_deal_type': deal_type or '',
    })


def property_detail(request, pk):
    obj = get_object_or_404(Property.objects.select_related('category', 'agent', 'owner'), pk=pk)
    similar = (
        Property.objects.filter(is_active=True, category=obj.category)
        .exclude(pk=obj.pk)
        .select_related('category')
        .order_by('-created_at')[:3]
    )
    return render(request, 'properties/property_detail.html', {
        'property': obj,
        'similar': similar,
    })


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            for image_file in request.FILES.getlist('extra_images'):
                PropertyImage.objects.create(property=obj, image=image_file)

            return redirect('property_detail', pk=obj.pk)
    else:
        form = PropertyForm()

    return render(request, 'properties/property_form.html', {'form': form})


@login_required
def property_update(request, pk):
    obj = get_object_or_404(Property, pk=pk)
    if obj.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()

            delete_ids = [i for i in request.POST.getlist('delete_images') if i.isdigit()]
            for img in obj.images.filter(pk__in=delete_ids):
                img.image.delete(save=False)
                img.delete()

            for image_file in request.FILES.getlist('extra_images'):
                PropertyImage.objects.create(property=obj, image=image_file)

            return redirect('property_detail', pk=obj.pk)
    else:
        form = PropertyForm(instance=obj)

    return render(request, 'properties/property_form.html', {
        'form': form,
        'object': obj,
    })


@login_required
def property_delete(request, pk):
    obj = get_object_or_404(Property, pk=pk)
    if obj.owner != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        obj.delete()
        return redirect('property_list')

    return render(request, 'properties/property_confirm_delete.html', {'object': obj})


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
