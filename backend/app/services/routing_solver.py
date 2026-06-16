from ortools.constraint_solver import (
    pywrapcp,
    routing_enums_pb2
)


def solve_tsp(duration_matrix):

    size = len(duration_matrix)

    manager = pywrapcp.RoutingIndexManager(
        size,
        1,
        0
    )

    routing = pywrapcp.RoutingModel(
        manager
    )

    def callback(from_index, to_index):

        from_node = (
            manager.IndexToNode(from_index)
        )

        to_node = (
            manager.IndexToNode(to_index)
        )

        return int(
            duration_matrix[from_node][to_node]
        )

    transit_index = (
        routing.RegisterTransitCallback(
            callback
        )
    )

    routing.SetArcCostEvaluatorOfAllVehicles(
        transit_index
    )

    params = (
        pywrapcp
        .DefaultRoutingSearchParameters()
    )

    params.first_solution_strategy = (
        routing_enums_pb2
        .FirstSolutionStrategy
        .PATH_CHEAPEST_ARC
    )

    solution = (
        routing.SolveWithParameters(
            params
        )
    )

    route = []

    index = routing.Start(0)

    while not routing.IsEnd(index):

        route.append(
            manager.IndexToNode(index)
        )

        index = solution.Value(
            routing.NextVar(index)
        )

    route.append(
        manager.IndexToNode(index)
    )

    return route