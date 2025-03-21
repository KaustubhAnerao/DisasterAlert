// Global variables
const API_BASE_URL = 'http://localhost:5000/api';  // Change this to your actual API endpoint
let currentPage = window.location.hash.substring(1) || 'home';

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Handle navigation
    window.addEventListener('hashchange', function() {
        currentPage = window.location.hash.substring(1) || 'home';
        loadPage(currentPage);
    });
    
    // Load initial page
    loadPage(currentPage);
    
    // Set up modal close functionality
    setupModal();
});

// Function to load the appropriate page content
function loadPage(page) {
    const mainContent = document.getElementById('main-content');
    mainContent.innerHTML = '<div class="loading">Loading...</div>';
    
    if (page === 'home' || page === '') {
        loadHomePage();
    } else if (page === 'events') {
        loadEventsPage();
    }
}

// Set up modal functionality
function setupModal() {
    const modal = document.getElementById('eventModal');
    const closeBtn = document.querySelector('.close');
    
    // Close modal when clicking X
    closeBtn.onclick = function() {
        modal.style.display = 'none';
    };
    
    // Close when clicking outside of modal content
    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    };
}