from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView

from cities.models import City
from routes.forms import RouteForm, RouteModelForm
from trains.models import Train
from .controller import get_routes


__all__ = (
    'find_routes', 'add_route', 'find', 'save_route',
    'RoutesListView', 'RouteDetailView', 'RouteDeleteView',
)

from .models import Route


def find(request):
    form = RouteForm()
    return render(request, 'routes/find.html', {'form': form})


def find_routes(request):
    if request.method == 'POST':
        form = RouteForm(request.POST)
        if form.is_valid():
            try:
                context = get_routes(request, form)
            except ValueError as error:
                messages.error(request, error)
                return render(request, 'routes/find.html', {'form': form})
            return render(request, 'routes/find.html', context)
    form = RouteForm()
    return render(request, 'routes/find.html', {'form': form})

@login_required
def add_route(request):
    if request.method == 'POST':
        context = {}
        data = request.POST
        if data:
            total_time = int(data['total_time'])
            from_city_id = int(data['from_city'])
            to_city_id = int(data['to_city'])
            trains = data['trains'].split(',')
            trains_lst = [int(t) for t in trains if t.isdigit()]
            qs = Train.objects.filter(id__in=trains_lst).select_related(
                'from_city', 'to_city')
            cities = City.objects.filter(
                id__in=[from_city_id, to_city_id]).in_bulk()
            form = RouteModelForm(
                initial={
                    'from_city': cities[from_city_id],
                    'to_city': cities[to_city_id],
                    'travel_times': total_time,
                    'trains': qs
                }
            )
            context['form'] = form
        return render(request, 'routes/create.html', context)
    form = RouteForm()
    messages.error(request, 'Невозможно сохранить не существующий маршрут')
    # return render(request, 'routes/find.html', {'form': form})
    return redirect('routes/find.html')

@login_required
def save_route(request):
    if request.method == 'POST':
        form = RouteModelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Маршрут успешно сохранен!')
            return redirect('routes:find')
    form = RouteForm()
    return render(request, 'routes/find.html', {'form': form})


class RoutesListView(ListView):
    paginate_by = 10
    model = Route
    template_name = 'routes/list.html'

class RouteDetailView(DetailView):
    # детальное отображение
    queryset = Route.objects.all()
    template_name = 'routes/detail.html'


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('routes:list')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Маршрут успешно удален')
        return self.post(request, *args, **kwargs)