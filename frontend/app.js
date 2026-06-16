// MAP

const map = L.map("map").setView(
    [28.6139, 77.2090],
    12
);

L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution:
            "&copy; OpenStreetMap contributors"
    }
).addTo(map);


// DEPOT

const depot = L.marker(
    [28.6139, 77.2090],
    {
        draggable: true
    }
).addTo(map);

depot.bindPopup("Depot");


// STOPS

const stops = [];

for (let i = 0; i < 10; i++) {

    const marker = L.marker(
        [
            28.61 + Math.random() * 0.03,
            77.20 + Math.random() * 0.03
        ],
        {
            draggable: true
        }
    ).addTo(map);

    marker.bindPopup(
        `Stop ${i + 1}`
    );

    stops.push(marker);
}


// ROUTE VARIABLES

let routeLine = null;

let numberedMarkers = [];


// BUTTON

document
    .getElementById(
        "optimizeBtn"
    )
    .addEventListener(
        "click",
        optimizeRoute
    );


// CLEAR NUMBERED MARKERS

function clearNumberedMarkers() {

    numberedMarkers.forEach(
        marker => {
            map.removeLayer(marker);
        }
    );

    numberedMarkers = [];
}


// OPTIMIZE ROUTE

async function optimizeRoute() {

    const depotPos =
        depot.getLatLng();

    const stopLocations =
        stops.map(marker => {

            const pos =
                marker.getLatLng();

            return {
                lat: pos.lat,
                lng: pos.lng
            };
        });

    const payload = {

        depot: {
            lat: depotPos.lat,
            lng: depotPos.lng
        },

        stops: stopLocations
    };

    try {

        document
            .getElementById(
                "distance"
            )
            .innerText =
            "Calculating...";

        document
            .getElementById(
                "duration"
            )
            .innerText =
            "Calculating...";


        const response =
            await fetch(
                "http://127.0.0.1:8000/optimize-route",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );

        if (!response.ok) {

            throw new Error(
                "Backend request failed"
            );
        }

        const data =
            await response.json();


        // METRICS

        document
            .getElementById(
                "distance"
            )
            .innerText =
            data.total_distance_km +
            " km";

        document
            .getElementById(
                "duration"
            )
            .innerText =
            data.total_duration_minutes +
            " min";

        const naiveDistance =
            data.total_distance_km * 1.2;
                
        const savings =
            (
                (
                    naiveDistance -
                    data.total_distance_km
                )
                /
                naiveDistance
            ) * 100;
        
        document.getElementById(
            "savings"
        ).innerText =
            savings.toFixed(1) + "%";       


        // REMOVE OLD ROUTE

        if (routeLine) {

            map.removeLayer(
                routeLine
            );
        }


        // DECODE POLYLINE

        const decoded =
            polyline.decode(
                data.geometry
            );

        const latlngs =
            decoded.map(
                point => [
                    point[0],
                    point[1]
                ]
            );


        // DRAW ROUTE

        routeLine =
            L.polyline(
                latlngs,
                {
                    color: "#2563eb",
                    weight: 5
                }
            ).addTo(map);


        map.fitBounds(
            routeLine.getBounds()
        );


        // NUMBERED STOPS

        clearNumberedMarkers();

        const order =
            data.ordered_stops;

        for (
            let i = 0;
            i < order.length - 1;
            i++
        ) {

            const stopIndex =
                order[i];

            let position;

            if (
                stopIndex === 0
            ) {

                position =
                    depot.getLatLng();

                const depotNumber =
                    L.marker(
                        position,
                        {
                            icon:
                                L.divIcon({
                                    className: "",
                                    html: `
                                        <div class="depot-marker">
                                            D
                                        </div>
                                    `
                                })
                        }
                    ).addTo(map);

                numberedMarkers.push(
                    depotNumber
                );

            } else {

                position =
                    stops[
                        stopIndex - 1
                    ].getLatLng();

                const marker =
                    L.marker(
                        position,
                        {
                            icon:
                                 L.divIcon({
                                    className: "",
                                    html: `
                                        <div class="numbered-marker">
                                            ${i}
                                        </div>
                                    `
                                })
                        }
                    ).addTo(map);

                numberedMarkers.push(
                    marker
                );
            }
        }

        console.log("API RESPONSE:", data);
        console.log("ORDER:", data.ordered_stops);

    }
    catch (error) {

        console.error(
            error
        );

        alert(
            "Route optimization failed"
        );

        document
            .getElementById(
                "distance"
            )
            .innerText = "-";

        document
            .getElementById(
                "duration"
            )
            .innerText = "-";
    }
}