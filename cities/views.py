from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from cities.forms import CityForm
from cities.models import City

__all__ = (
    'home', 'CityDetailView',
)


def home(request):
    if request.POST:
        form = CityForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
    form = CityForm()
    qs = City.objects.all()
    return render(request, 'cities/home.html', {'cities': qs, 'form': form })


class CityDetailView(DetailView):
    queryset = City.objects.all()
    template_name = 'cities/detail.html'
