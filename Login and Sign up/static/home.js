document.addEventListener('DOMContentLoaded', function() {
    const createPostBtn = document.getElementById('create-post-button');
    const postModal = document.getElementById('post-modal');
    const closeBtn = document.querySelector('.close');
    const postForm = document.getElementById('post-form');
    const postsList = document.getElementById('posts-list');

    createPostBtn.addEventListener('click', function() {
        postModal.style.display = 'block';
    });

    closeBtn.addEventListener('click', function() {
        postModal.style.display = 'none';
    });

    function createComment(content, depth) {
        const comment = document.createElement('div');
        comment.className = 'comment';
        comment.style.marginLeft = `${depth * 15}px`; // Indent based on depth
        comment.innerHTML = `
            <p>${content}</p>
        `;
        return comment;
    }

    postForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const title = document.getElementById('post-title').value;
        const content = document.getElementById('post-content').value;
        if (title.trim() !== '' && content.trim() !== '') {
            const post = document.createElement('div');
            post.className = 'post';
            post.innerHTML = `
                <h3>${title}</h3>
                <p>${content}</p>
                <div class="comments"></div>
                <textarea class="comment-content" placeholder="Write your comment..."></textarea><br>
                <button class="submitCommentBtn">Comment</button>
            `;
            postsList.appendChild(post);
            postModal.style.display = 'none';
        }
    });

    postsList.addEventListener('click', function(event) {
        if (event.target.classList.contains('submitCommentBtn')) {
            const commentContent = event.target.parentElement.querySelector('.comment-content');
            const content = commentContent.value;
            if (content.trim() !== '') {
                const comment = createComment(content, 1); // Depth 1 for comments
                const post = event.target.parentElement;
                const commentsContainer = post.querySelector('.comments');
                commentsContainer.appendChild(comment);
                commentContent.value = '';
            }
        }
    });
});
