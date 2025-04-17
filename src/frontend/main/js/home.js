// Load home page content
async function loadHomePage() {
  const mainContent = document.getElementById("main-content");

  async function getCoordinatesForLocation(locationName) {
    try {
      const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(locationName)}`);
      if (!response.ok) {
        throw new Error('Geocoding API request failed');
      }
      const data = await response.json();
      if (data.length > 0) {
        return [parseFloat(data[0].lon), parseFloat(data[0].lat)]; // Returns [longitude, latitude]
      }
      return null;
    } catch (error) {
      console.error('Error geocoding location:', error);
      return null;
    }
  }

  // Fetch top alerts from API
  fetch(`${API_BASE_URL}/top-alerts`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then(async (data) => {
      let html = `
                <div class="top-alerts">
                    <h2>Top Alerts</h2>
                    <div id="alerts-container">
            `;

      if (data && data.length > 0) {
        console.log(data);
        data.forEach((alert) => {
          if (alert.top_alert === true) {
            const credibilityClass = getCredibilityClass(
              alert.average_credibility_score
            );

            // Format the date
            const firstReportedDate = alert.created_utc
              ? new Date(alert.created_utc * 1000).toLocaleString()
              : "Unknown";
            const latestUpdateDate = alert.updated_utc
              ? new Date(alert.updated_utc * 1000).toLocaleString()
              : "Unknown";

            html += `
                        <div class="alert-card" data-event-name="${
                          alert.event_name
                        }">
                            <h3>${alert.event_name}</h3>
                            <div class="alert-info">
                                <span>${alert.disaster_type || "Unknown"} - ${
              alert.location || "Unknown"
            }</span>
                                <span class="credibility ${credibilityClass}">Credibility Score: ${
              alert.average_credibility_score
            }/10</span>
                            </div>
                            <div class="alert-date">
                                <div>
                                  <small>Posted: ${firstReportedDate}</small>
                                </div>
                                <div>
                                  <small>Updated: ${latestUpdateDate}</small>
                                </div>
                            </div>
                            
                        </div>
                    `;
          }
        });
      } else {
        html += "<p>No alerts available at the moment.</p>";
      }

      html += `
                    </div>
                </div>
                <a href="#events" class="all-events-link">View All Events</a>
                <div id="map" style="width:100%; height:400px; margin-top:20px;"></div>
            `;

      mainContent.innerHTML = html;

      // Initialize MapLibre only if map div exists

      let map = null;
      const mapContainer = document.getElementById("map");
      if (mapContainer) {
        map = new maplibregl.Map({
          container: "map",
          style: "https://tiles.openfreemap.org/styles/liberty",
          center: [34.0209, -6.8417],
          zoom: 1,
        });
      }

      // Calculate timestamp for 3 months ago
      const threeMonthsAgo = new Date();
      threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
      const threeMonthsTimestamp = Math.floor(threeMonthsAgo.getTime() / 1000);

      // Loop through data and add markers
      if (data && data.length > 0) {
        for(const alert of data) {
          try {
              const coords = await getCoordinatesForLocation(alert.location);
              if (coords) {
                const markerElement = document.createElement('div');
                markerElement.style.backgroundImage = `url(../../assets/${encodeURIComponent(alert.disaster_type)}.png)`;
                markerElement.style.width = '30px';
                markerElement.style.height = '30px';
                markerElement.style.backgroundSize = '100%';
                markerElement.style.backgroundRepeat = 'no-repeat';
                markerElement.style.cursor = 'pointer';

                const marker = new maplibregl.Marker({ element: markerElement })
                    .setLngLat(coords)
                    .setPopup(
                        new maplibregl.Popup({ offset: 25 }).setHTML(`
                            <h3>${alert.event_name}</h3>
                        `)
                    );

                if (map) {
                  marker.addTo(map);
                }
              }
            } catch (error) {
              console.error(`Error processing alert for ${alert.location}:`, error);
            }
        }
      }

      // Add event listeners to cards
      document.querySelectorAll(".alert-card").forEach((card) => {
        card.addEventListener("click", function () {
          const eventName = this.getAttribute("data-event-name");
          fetchEventDetails(eventName);
        });
      });
    })
    .catch((error) => {
      mainContent.innerHTML = `
                <div class="top-alerts">
                    <h2>Top Alerts</h2>
                    <p>Error loading alerts. Please try again later.</p>
                </div>
                <a href="#events" class="all-events-link">View All Events</a>
                <div id="map" style="width:100%; height:400px; margin-top:20px;"></div>
            `;
      const map = new maplibregl.Map({
        container: "map",
        style: "https://tiles.openfreemap.org/styles/liberty",
        center: [34.0209, -6.8417],
        zoom: 1,
      });
      console.error("Error fetching alerts:", error);
    });
}