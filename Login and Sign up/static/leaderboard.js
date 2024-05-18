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

        console.log(`Generated stars for rating ${rating}: ${stars}`);
        return stars;
    }

    // Fetch and generate leaderboard rows dynamically
    fetch('/api/users')
        .then(response => response.json())
        .then(data => {
            const leaderboardBody = $('#leaderboard-body');
            leaderboardBody.empty(); // Clear existing rows before appending new ones
            data.forEach((user, index) => {
                const rank = index + 1;
                const stars = generateStars(user.rating);
                const row = `<div class="leaderboard-row">
                                <span class="rank">${rank}</span>
                                <span class="user">${user.name}</span>
                                <span class="rating">${stars}</span>
                            </div>`;
                console.log(`Appending row: ${row}`);
                leaderboardBody.append(row);
            });
        })
        .catch(error => console.error('Error fetching leaderboard data:', error));
});
