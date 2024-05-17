$(document).ready(function() {
    // Sample data for demonstration
    var users = [
        {"rank": 1, "user": "user 1", "rating": 5},
        {"rank": 2, "user": "user 2", "rating": 4.5},
        {"rank": 3, "user": "user 3", "rating": 4},
        {"rank": 4, "user": "user 4", "rating": 3.5},
        // Add more users as needed
    ];

    // Generate leaderboard rows dynamically
    var leaderboardBody = $('#leaderboard-body');
    users.forEach(function(user) {
        var row = $('<div class="leaderboard-row"></div>');
        row.append('<span class="rank">' + user.rank + '</span>');
        row.append('<span class="user">' + user.user + '</span>');
        row.append('<span class="rating">' + generateStars(user.rating) + '</span>');
        leaderboardBody.append(row);
    });
});

// Function to generate star icons based on rating value
function generateStars(rating) {
    var fullStars = Math.floor(rating);
    var halfStar = rating % 1 >= 0.5 ? 1 : 0;
    var emptyStars = 5 - fullStars - halfStar;

    var stars = '';
    for (var i = 0; i < fullStars; i++) {
        stars += '<i class="fas fa-star"></i>';
    }
    if (halfStar) {
        stars += '<i class="fas fa-star-half-alt"></i>';
    }
    for (var j = 0; j < emptyStars; j++) {
        stars += '<i class="far fa-star"></i>';
    }

    return stars;
}
