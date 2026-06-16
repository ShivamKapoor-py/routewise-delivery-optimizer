from fastapi import APIRouter

from app.models.request_models import (
    OptimizeRouteRequest
)

from app.models.response_models import (
    OptimizeRouteResponse
)

from app.services.osrm_service import (
    OSRMService
)

from app.services.routing_solver import (
    solve_tsp
)

router = APIRouter()


@router.get("/health")
def health():

    return {
        "status": "healthy"
    }


@router.get("/osrm-test")
async def osrm_test():

    return await OSRMService.test_connection()


@router.get("/solver-test")
def solver_test():

    matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0]
    ]

    route = solve_tsp(matrix)

    return {
        "route": route
    }


@router.post(
    "/optimize-route",
    response_model=OptimizeRouteResponse
)
async def optimize_route(
    payload: OptimizeRouteRequest
):

    all_locations = [
        payload.depot.model_dump()
    ] + [
        stop.model_dump()
        for stop in payload.stops
    ]

    matrix_data = (
        await OSRMService.get_matrix(
            all_locations
        )
    )

    duration_matrix = (
        matrix_data["durations"]
    )

    route_order = solve_tsp(
        duration_matrix
    )

    ordered_locations = [
        all_locations[i]
        for i in route_order[:-1]
    ]

    route_data = (
        await OSRMService.get_route_geometry(
            ordered_locations
        )
    )

    return OptimizeRouteResponse(
    optimized_order=route_order,

    total_distance_km=round(
        route_data["distance"] / 1000,
        2
    ),

    total_duration_minutes=round(
        route_data["duration"] / 60,
        2
    ),

    geometry=route_data["geometry"],

    ordered_stops=route_order
)