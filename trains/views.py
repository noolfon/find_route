from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from trains.forms import TrainForm
from trains.models import Train

__all__ = (
    'TrainDetailView', 'TrainCreateView', 'TrainUpdateView',
    'TrainDeleteView', 'TrainListView'
)


# def home(request):
#     if request.POST:
#         form = TrainForm(request.POST)
#         if form.is_valid():
#             form.save()
#     form = TrainForm()
#     qs = Train.objects.all()
#     return render(request, 'trains/home.html', {'trains': qs, 'form': form})

class TrainListView(ListView):
    paginate_by = 10
    model = Train
    template_name = 'trains/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = TrainForm()
        context['form'] = form
        return context


class TrainDetailView(DetailView):
    # детальное отображение
    queryset = Train.objects.all()
    template_name = 'trains/detail.html'


class TrainCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    # модель скоторой работает форма(куда добавит записи)
    model = Train
    # передадать форму из класса форм на страничку
    form_class = TrainForm
    # шаблон отображения
    template_name = 'trains/create.html'
    # адресс редиректа
    success_url = reverse_lazy('trains:home')
    # передача сообщений о успешном создании
    success_message = "Поезд успешно дабавлен!"


class TrainUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/update.html'
    success_url = reverse_lazy('trains:home')
    success_message = "Поезд успешно изменен!"


class TrainDeleteView(LoginRequiredMixin, DeleteView):
    model = Train
    form_class = TrainForm
    template_name = 'trains/delete.html'
    success_url = reverse_lazy('trains:home')

    def get(self, request, *args, **kwargs):
        messages.success(request, 'Поезд успешно удален!')
        return self.post(request, *args, **kwargs)
