// Load home page content
function loadHomePage() {
    const mainContent = document.getElementById('main-content');
    
    // Fetch top alerts from API
    fetch(`${API_BASE_URL}/top-alerts`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            let html = `
                <div class="top-alerts">
                    <h2>Top Alerts</h2>
                    <div id="alerts-container">
            `;
            
            if (data && data.length > 0) {
                data.forEach(alert => {
                    const credibilityClass = getCredibilityClass(alert.credibility_score);
                    
                    // Format the date
                    const alertDate = new Date(alert.created_utc * 1000);
                    const formattedDate = alertDate.toLocaleDateString();
                    
                    html += `
                        <div class="alert-card" data-event-name="${alert.event_name}">
                            <h3>${truncateText(alert.title, 120)}</h3>
                            <p>${truncateText(alert.selftext || 'No description available', 150)}</p>
                            <div class="alert-info">
                                <span>${alert.disaster_type || 'Unknown'} - ${alert.location || 'Unknown'}</span>
                                <span class="credibility ${credibilityClass}">Score: ${alert.credibility_score}/10</span>
                            </div>
                            <div class="alert-date">
                                <small>Posted: ${formattedDate}</small>
                            </div>
                        </div>
                    `;
                });
            } else {
                html += '<p>No alerts available at the moment.</p>';
            }
            
            html += `
                    </div>
                </div>
                <a href="#events" class="all-events-link">View All Events</a>
            `;
            
            mainContent.innerHTML = html;
            
            // Add event listeners to cards
            document.querySelectorAll('.alert-card').forEach(card => {
                card.addEventListener('click', function() {
                    const eventName = this.getAttribute('data-event-name');
                    fetchEventDetails(eventName);
                });
            });
        })
        .catch(error => {
            mainContent.innerHTML = `
                <div class="top-alerts">
                    <h2>Top Alerts</h2>
                    <p>Error loading alerts. Please try again later.</p>
                </div>
                <a href="#events" class="all-events-link">View All Events</a>
            `;
            console.error('Error fetching alerts:', error);
        });
}