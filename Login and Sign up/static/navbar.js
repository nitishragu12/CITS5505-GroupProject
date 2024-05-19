// Wait for the DOM content to be fully loaded before executing JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Get necessary elements from the DOM
    const createPostBtn = document.getElementById('create-post-button');
    const postModal = document.getElementById('post-modal');
    const closeBtn = document.querySelector('.close');
    const postForm = document.getElementById('post-form');
    const postsList = document.getElementById('posts-list');

    // Event listener for opening the post modal
    createPostBtn.addEventListener('click', function() {
        postModal.style.display = 'block'; // Display the post modal
    });

    // Event listener for closing the post modal
    closeBtn.addEventListener('click', function() {
        postModal.style.display = 'none'; // Hide the post modal
    });

    // Function to create a comment element
    function createComment(content, user) {
        const comment = document.createElement('div');
        comment.className = 'comment'; // Set class for styling
        comment.innerHTML = `
            <p><strong>${user}:</strong> ${content}</p>
        `; // Set inner HTML for the comment
        return comment; // Return the created comment element
    }

    // Event listener for submitting the post form
    postForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission behavior
        const title = document.getElementById('post-title').value; // Get post title
        const content = document.getElementById('post-content').value; // Get post content
        const user = 'John'; // Static username, replace with dynamic data if available
        if (title.trim() !== '' && content.trim() !== '') { // Check if title and content are not empty
            // Create post element
            const post = document.createElement('div');
            post.className = 'post'; // Set class for styling
            post.innerHTML = `
                <h3>${title}</h3>
                <p>${content}</p>
                <p><strong>${user}</strong></p> <!-- Include username here -->
                <button class="toggleCommentsBtn"><i class="fas fa-comments"></i> Comments</button>
                <div class="comments" style="display: none;">
                    <textarea class="comment-content" placeholder="Write your comment..."></textarea><br>
                    <button class="submitCommentBtn">Comment</button>
                </div>
            `; // Set inner HTML for the post
            postsList.appendChild(post); // Append the post to the posts list
            postModal.style.display = 'none'; // Hide the post modal
        }
    });

    // Event listener for handling clicks on the posts list
    postsList.addEventListener('click', function(event) {
        if (event.target.classList.contains('toggleCommentsBtn')) {
            // Toggle display of comments section
            const commentsContainer = event.target.nextElementSibling;
            commentsContainer.style.display = commentsContainer.style.display === 'none' ? 'block' : 'none';
        } else if (event.target.classList.contains('submitCommentBtn')) {
            // Handle comment submission
            const commentContent = event.target.previousElementSibling;
            const content = commentContent.value; // Get comment content
            const user = 'John'; // Static username, replace with dynamic data if available
            if (content.trim() !== '') { // Check if comment content is not empty
                // Create comment element and append it
                const comment = createComment(content, user);
                const commentsContainer = event.target.parentElement;
                commentsContainer.insertBefore(comment, commentContent);
                commentContent.value = ''; // Clear the comment input field
            }
        }
    });
});
