from trains.models import Train


def dfs_paths(graph, start, goal):
    """ Функция поиска всех возможных маршрутов
     из одного города в другой. Вариант посещения одного
     и готоже города не рассматривается."""
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs):
    """qs - получаем список поездов
    формируем словарь, где ключ - это город из которого можно выехать
    значние - это города куда можно попасть. запись ввиде id
    благодаря setdefault  получаем  вот такие записи
    {8: {11, 20}, 24: {4}, 11: {12}} """
    graph = {}
    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    qs = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(qs)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    travelling_time = data['route_travel_time']
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
    if not len(all_ways):
        # нет ни одного маршрута для данного поиска
        raise ValueError('Маршрута, удовлетворяющего условиям не существует')
    if cities:
        # если есть города, через которые нужно проехать
        _cities = [city.id for city in cities]
        right_ways = []
        for route in all_ways:
            if all(city in route for city in _cities):
                right_ways.append(route)
        if not right_ways:
            # когда список маршрутов пуст
            raise ValueError('Маршрут, через эти города невозможен')
    else:
        right_ways = all_ways
    routes = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    for route in right_ways:
        tmp = {}
        tmp['trains'] = []
        total_time = 0
        for i in range(len(route) - 1):
            qs = all_trains[(route[i], route[i + 1])]
            q = qs[0]
            total_time += q.travel_time
            tmp['trains'].append(q)
        tmp['total_time'] = total_time
        if total_time <= travelling_time:
            # если общее время в пути, меньше заданного,
            # то добавляем маршрут в общий список
            routes.append(tmp)
    if not routes:
        # если список пуст, то нет таких маршрутов,
        # которые удовлетворяли бы заданным условиям
        raise ValueError('Время в пути больше заданного')
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = list(set(r['total_time'] for r in routes))
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city, 'to_city': to_city}
    return context

# def get_routes(request, form) -> dict:
#     context = {'form': form}
#     qs = Train.objects.all()
#     graph = get_graph(qs)
#     data = form.cleaned_data
#     from_city, to_city = data['from_city'], data['to_city']
#     route_travel_time = data['route_travel_time']
#     cities = data['cities']
#     all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
#     if not len(all_ways):
#         raise ValueError('Такого маршрута нет')
#     if cities:
#         _cities = [city.id for city in cities]
#         rigth_ways = []
#         for route in all_ways:
#             if all(city in route for city in _cities):
#                 rigth_ways.append(route)
#         if not rigth_ways:
#             raise ValueError('Маршрут через эти города не возможен')
#     else:
#         rigth_ways = all_ways
#     routes = []
#     all_trains = {}
#     for q in qs:
#         all_trains.setdefault((q.from_city_id, q.to_city_id), [])
#         all_trains[(q.from_city_id, q.to_city_id)].append(q)
#     for route in rigth_ways:
#         tmp = {}
#         tmp['trains'] = []
#         total_time = 0
#         for i in range(len(route) - 1):
#             qs = all_trains[(route[i], route[i + 1])]
#             q = qs[0]
#             total_time += q.travel_time
#             tmp['trains'].append(q)
#         tmp['total_time'] = total_time
#         if total_time <= route_travel_time:
#             routes.append(tmp)
#     if not routes:
#         raise ValueError('Время в пути больше задоного')
#     sorted_routes = []
#     if len(routes):
#         sorted_routes = routes
#     else:
#         times = list(set(r['total_time'] for r in routes))
#         times = sorted(times)
#         for time in times:
#             for route in routes:
#                 if time == route['total_time']:
#                     sorted_routes.append(route)
#     context['routes'] = sorted_routes
#     context['cities'] = {'from_city': from_city.name, 'to_city': to_city.name}
#
#     return context