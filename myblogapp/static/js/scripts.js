document.addEventListener('DOMContentLoaded', function () {
    const blogEntriesDiv = document.getElementById('blog-entries');
    const blogForm = document.getElementById('blog-form');

    // Fetch all blog entries
    function fetchBlogEntries() {
        fetch('/api/blogentries')
            .then(response => response.json())
            .then(data => {
                blogEntriesDiv.innerHTML = '';
                data.forEach(entry => {
                    const entryDiv = document.createElement('div');
                    entryDiv.classList.add('blog-entry');
                    entryDiv.innerHTML = `
                        <h3>${entry.title}</h3>
                        <p>${entry.subtitle}</p>
                        <p>${entry.blurb}</p>
                        <p>${entry.content}</p>
                        <p><strong>Published:</strong> ${entry.is_published}</p>
                        <button onclick="deleteBlogEntry(${entry.post_id})">Delete</button>
                    `;
                    blogEntriesDiv.appendChild(entryDiv);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    // Create a new blog entry
    blogForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const newEntry = {
            user_id: 1, // Assuming user_id is 1 for now; modify as needed
            title: document.getElementById('title').value,
            subtitle: document.getElementById('subtitle').value,
            blurb: document.getElementById('blurb').value,
            content: document.getElementById('content').value,
            is_published: true
        };

        fetch('/api/blogentries', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newEntry)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            fetchBlogEntries(); // Refresh the list after adding
        })
        .catch(error => console.error('Error:', error));
    });

    // Delete a blog entry
    window.deleteBlogEntry = function (postId) {
        fetch(`/api/blogentries/${postId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Deleted:', data);
            fetchBlogEntries(); // Refresh the list after deleting
        })
        .catch(error => console.error('Error:', error));
    };

    // Fetch blog entries on load
    fetchBlogEntries();
});
