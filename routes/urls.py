from django.urls import path
from routes.views import *


urlpatterns = [
    path('find/', find, name='find'),
    path('find_routes/', find_routes, name='find_routes'),
    path('add_route/', add_route, name='add_route'),
    path('create/', save_route, name='save_route'),
    path('list/', RoutesListView.as_view(), name='list'),
    path('detail/<int:pk>', RouteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', RouteDeleteView.as_view(), name='delete'),

]
