from django.contrib import messages
from django.shortcuts import render
from routes.forms import RouteForm
from .controller import get_routes

# Create your views here.

__all__ = (
    'find',
)


def find(request):
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
