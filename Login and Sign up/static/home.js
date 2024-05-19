document.addEventListener('DOMContentLoaded', function() {
    // Get elements from the DOM
    const createPostBtn = document.getElementById('create-post-button');
    const postModal = document.getElementById('post-modal');
    const closeBtn = document.querySelector('.close');
    const postForm = document.getElementById('post-form');
    const postsList = document.getElementById('posts-list');

    // Event listener for opening post modal
    createPostBtn.addEventListener('click', function() {
        postModal.style.display = 'block';
    });

    // Event listener for closing post modal
    closeBtn.addEventListener('click', function() {
        postModal.style.display = 'none';
    });

    // Function to create a comment element
    function createComment(content, user) {
        const comment = document.createElement('div');
        comment.className = 'comment';
        comment.innerHTML = `
            <p><strong>${user}:</strong> ${content}</p>
        `;
        return comment;
    }

    // Event listener for submitting post form
    postForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const title = document.getElementById('post-title').value;
        const content = document.getElementById('post-content').value;
        const user = 'John'; // Replace this with dynamic user data if available
        if (title.trim() !== '' && content.trim() !== '') {
            // Create post element
            const post = document.createElement('div');
            post.className = 'post';
            post.innerHTML = `
                <h3>${title}</h3>
                <p>${content}</p>
                <p><strong>${user}</strong></p> <!-- Include username here -->
                <button class="toggleCommentsBtn"><i class="fas fa-comments"></i> Comments</button>
                <div class="comments" style="display: none;">
                    <textarea class="comment-content" placeholder="Write your comment..."></textarea><br>
                    <button class="submitCommentBtn">Comment</button>
                </div>
            `;
            postsList.appendChild(post);
            postModal.style.display = 'none';
        }
    });

    // Event listener for toggling comments section
    postsList.addEventListener('click', function(event) {
        if (event.target.classList.contains('toggleCommentsBtn')) {
            // Toggle comments visibility
            const commentsContainer = event.target.nextElementSibling;
            commentsContainer.style.display = commentsContainer.style.display === 'none' ? 'block' : 'none';
        } else if (event.target.classList.contains('submitCommentBtn')) {
            // Submit comment
            const commentContent = event.target.previousElementSibling;
            const content = commentContent.value;
            const user = 'John'; // Replace this with dynamic user data if available
            if (content.trim() !== '') {
                // Create comment element and append it
                const comment = createComment(content, user);
                const commentsContainer = event.target.parentElement;
                commentsContainer.insertBefore(comment, commentContent);
                commentContent.value = '';
            }
        }
    });
});
