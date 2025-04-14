// Load events page content
function loadEventsPage() {
  const mainContent = document.getElementById("main-content");

  // Fetch events from API
  fetch(`${API_BASE_URL}/events`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      let html = `
                <a href="#home" class="back-to-home">← Back to Home</a>
                <div class="search-container">
                    <input type="text" id="event-search" placeholder="Search events by type, location or keyword...">
                </div>
                <div class="events-grid" id="events-container">
            `;

      if (data && data.length > 0) {
        data.forEach((event) => {
          // Calculate credibility class
          const credibilityClass = getCredibilityClass(
            event.average_credibility_score
          );

          // Format the date if available
          let dateDisplay = "";
          if (event.latest_update) {
            const eventDate = new Date(event.latest_update * 1000);
            dateDisplay = eventDate.toLocaleDateString();
          }

          html += `
                        <div class="event-card" data-event-name="${
                          event.event_name
                        }">
                            <div class="event-header">
                                <div class="event-title">${
                                  event.event_name
                                }</div>
                                <div class="event-location">${
                                  event.location || "Unknown"
                                }</div>
                            </div>
                            <p>${
                              event.title
                                ? truncateText(event.title, 100)
                                :""
                            }</p>
                            <div class="event-stats">
                                <span>Posts: ${event.no_of_posts}</span>
                                <span class="credibility ${credibilityClass}">Score: ${
            event.average_credibility_score
          }/10</span>
                                ${
                                  dateDisplay
                                    ? `<span>Updated: ${dateDisplay}</span>`
                                    : ""
                                }
                            </div>
                        </div>
                    `;
        });
      } else {
        html += "<p>No events available at the moment.</p>";
      }

      html += `
                </div>
            `;

      mainContent.innerHTML = html;

      // Add search functionality
      const searchInput = document.getElementById("event-search");
      if (searchInput) {
        searchInput.addEventListener("input", function () {
          filterEvents(this.value.toLowerCase());
        });
      }

      // Add event listeners to cards
      document.querySelectorAll(".event-card").forEach((card) => {
        card.addEventListener("click", function () {
          const eventName = this.getAttribute("data-event-name");
          fetchEventDetails(eventName);
        });
      });
    })
    .catch((error) => {
      mainContent.innerHTML = `
                <a href="#home" class="back-to-home">← Back to Home</a>
                <div class="search-container">
                    <input type="text" placeholder="Search events...">
                </div>
                <p>Error loading events. Please try again later.</p>
            `;
      console.error("Error fetching events:", error);
    });
}

// Filter events based on search input
function filterEvents(query) {
  const eventCards = document.querySelectorAll(".event-card");

  eventCards.forEach((card) => {
    const eventTitle = card
      .querySelector(".event-title")
      .textContent.toLowerCase();
    const eventLocation = card
      .querySelector(".event-location")
      .textContent.toLowerCase();
   

    if (
      eventTitle.includes(query) ||
      eventLocation.includes(query) 
    ) {
      card.style.display = "block";
    } else {
      card.style.display = "none";
    }
  });
}

// Fetch event details from API
function fetchEventDetails(eventName) {
  fetch(`${API_BASE_URL}/events/${encodeURIComponent(eventName)}`)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      showEventDetails(data);
    })
    .catch((error) => {
      console.error("Error fetching event details:", error);

      const modal = document.getElementById("eventModal");
      const modalContent = document.getElementById("modal-content-container");
      modalContent.innerHTML =
        "<p>Error loading event details. Please try again later.</p>";
      modal.style.display = "block";
    });
}

// Show event details in modal
function showEventDetails(data) {
  const modal = document.getElementById("eventModal");
  const modalContent = document.getElementById("modal-content-container");

  const event = data.event;
  const posts = data.posts || [];

  const credibilityClass = getCredibilityClass(event.average_credibility_score);

  // Format dates
  const firstReportedDate = event.created_utc
    ? new Date(event.created_utc* 1000).toLocaleString()
    : "Unknown";
  const latestUpdateDate = event.updated_utc
    ? new Date(event.updated_utc * 1000).toLocaleString()
    : "Unknown";

  let detailsHTML = `
        <h2 class="event-detail-title">${event.event_name}</h2>
        <p><strong>Type:</strong> ${event.disaster_type}</p>
        <p><strong>Location:</strong> ${event.location}</p>
        <p><strong>First Reported:</strong> ${firstReportedDate}</p>
        <p><strong>Last Reported:</strong> ${latestUpdateDate}</p>
        <p><strong>Number of Reports:</strong> ${event.no_of_posts}</p>
        <div style="margin: 15px 0;">
            <span class="credibility ${credibilityClass}">Average Credibility Score: ${event.average_credibility_score}/10</span>
        </div>
        
        <h3>Related Posts</h3>
    `;

  if (posts.length > 0) {
    posts.forEach((post) => {
      const postDate = new Date(post.created_utc * 1000).toLocaleString();
      const postCredibilityClass = getCredibilityClass(post.credibility_score);

      detailsHTML += `
                <div class="post-card" style="margin-bottom: 20px; padding: 15px; background-color: #f9f9f9; border-radius: 8px;">
                    <h4>${post.title}</h4>
                    <p>${post.selftext}</p>
                    <div style="display: flex; justify-content: space-between; margin-top: 10px; font-size: 0.9rem;">
                        <span>Posted: ${postDate}</span>
                        <span class="credibility ${postCredibilityClass}">Score: ${post.credibility_score}/10</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 0.85rem;">
                        <p>Source: <a href="${post.url}" target="_blank">${post.subreddit_name_prefixed}</a></p>
                        <p>Author: ${post.author}</p>
                        <p>Comments: ${post.num_comments} | Upvote Ratio: ${post.upvote_ratio}</p>
                    </div>
                </div>
            `;
    });
  } else {
    detailsHTML += "<p>No posts available for this event.</p>";
  }

  modalContent.innerHTML = detailsHTML;
  modal.style.display = "block";
}
