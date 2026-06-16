import httpx

from app.core.config import settings


class OSRMService:

    @staticmethod
    async def test_connection():

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT
        ) as client:

            response = await client.get(
                f"{settings.OSRM_BASE_URL}/nearest/v1/driving/77.2090,28.6139"
            )

        return response.json()

    @staticmethod
    async def get_matrix(locations):

        coordinates = ";".join(
            f"{loc['lng']},{loc['lat']}"
            for loc in locations
        )

        url = (
            f"{settings.OSRM_BASE_URL}"
            f"/table/v1/driving/{coordinates}"
            "?annotations=distance,duration"
        )

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT
        ) as client:

            response = await client.get(url)

        return response.json()

    @staticmethod
    async def get_route_geometry(locations):

        coordinates = ";".join(
            f"{loc['lng']},{loc['lat']}"
            for loc in locations
        )

        url = (
            f"{settings.OSRM_BASE_URL}"
            f"/route/v1/driving/{coordinates}"
            "?overview=full"
            "&geometries=polyline"
        )

        async with httpx.AsyncClient(
            timeout=settings.REQUEST_TIMEOUT
        ) as client:

            response = await client.get(url)

        data = response.json()

        route = data["routes"][0]

        return {
            "geometry": route["geometry"],
            "distance": route["distance"],
            "duration": route["duration"]
        }