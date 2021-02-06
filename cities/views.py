from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from cities.forms import CityForm
from cities.models import City

__all__ = (
    'CityDetailView', 'CityCreateView', 'CityUpdateView',
    'CityDeleteView', 'CityListView'
)


# def home(request):
#     if request.POST:
#         form = CityForm(request.POST)
#         if form.is_valid():
#             form.save()
#     form = CityForm()
#     qs = City.objects.all()
#     return render(request, 'cities/home.html', {'cities': qs, 'form': form})

class CityListView(ListView):
    paginate_by = 5
    model = City
    template_name = 'cities/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CityForm()
        context['form'] = form
        return context


class CityDetailView(DetailView):
    # детальное отображение
    queryset = City.objects.all()
    template_name = 'cities/detail.html'


class CityCreateView(SuccessMessageMixin, CreateView):
    # модель скоторой работает форма(куда добавит записи)
    model = City
    # передадать форму из класса форм на страничку
    form_class = CityForm
    # шаблон отображения
    template_name = 'cities/create.html'
    # адресс редиректа
    success_url = reverse_lazy('cities:home')
    # передача сообщений о успешном создании
    success_message = "Город успешно дабавлен!"


class CityUpdateView(SuccessMessageMixin, UpdateView):
    model = City
    form_class = CityForm
    template_name = 'cities/update.html'
    success_url = reverse_lazy('cities:home')
    success_message = "Город успешно изменен!"


class CityDeleteView(DeleteView):
    model = City
    form_class = CityForm
    template_name = 'cities/delete.html'
    success_url = reverse_lazy('cities:home')

    # после переопределения этого метода не показывает страничку с подтверждением
    def get(self, request, *args, **kwargs):
        messages.success(request, 'Город успешно удален!')
        return self.post(request, *args, **kwargs)
