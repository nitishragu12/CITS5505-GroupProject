$(document).ready(function() {
    // Function to generate star icons based on rating value
    function generateStars(rating) {
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5 ? 1 : 0;
        const emptyStars = 5 - fullStars - halfStar;

        let stars = '';
        for (let i = 0; i < fullStars; i++) {
            stars += '<i class="fas fa-star"></i>';
        }
        if (halfStar) {
            stars += '<i class="fas fa-star-half-alt"></i>';
        }
        for (let j = 0; j < emptyStars; j++) {
            stars += '<i class="far fa-star"></i>';
        }

        return stars;
    }

    // Function to generate badge based on rank
    function generateBadge(rank) {
        // Assuming badgeUrls is defined elsewhere in your code
        if (rank === 1) {
            return '<img src="' + badgeUrls.gold + '" class="badge" alt="Gold Badge">';
        } else if (rank === 2) {
            return '<img src="' + badgeUrls.silver + '" class="badge" alt="Silver Badge">';
        } else if (rank === 3) {
            return '<img src="' + badgeUrls.bronze + '" class="badge" alt="Bronze Badge">';
        } else {
            return '';
        }
    }

    // Fetch and generate leaderboard rows dynamically
    function loadLeaderboard() {
        fetch('/api/leaderboard')
            .then(response => response.json())
            .then(data => {
                const leaderboardBody = $('#leaderboard-body');
                leaderboardBody.empty(); // Clear existing rows before appending new ones
                data.forEach((user, index) => {
                    const rank = index + 1;
                    const stars = generateStars(user.average_rating);
                    const badge = generateBadge(rank);
                    const row = `<div class="leaderboard-row">
                                    <span class="badge">${badge}</span>
                                    <span class="rank">${rank}</span>
                                    <span class="user">${user.name}</span>
                                    <span class="rating">${stars}</span>
                                </div>`;
                    leaderboardBody.append(row);
                });
            })
            .catch(error => console.error('Error fetching leaderboard data:', error));
    }

    // Call the function to load the leaderboard on document ready
    loadLeaderboard();
});
