// Helper function to truncate text
function truncateText(text, maxLength) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// Helper function to determine credibility class
function getCredibilityClass(score) {
    if (score >= 7) {
        return 'credibility-high';
    } else if (score >= 4) {
        return 'credibility-medium';
    } else {
        return 'credibility-low';
    }
}