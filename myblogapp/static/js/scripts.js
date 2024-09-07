document.addEventListener('DOMContentLoaded', function () {
    const blogEntriesDiv = document.getElementById('blog-entries');
    const blogForm = document.getElementById('blog-form');
    const updateForm = document.getElementById('update-form');
    const cancelUpdateButton = document.getElementById('cancel-update');
    const fetchBlogForm = document.getElementById('fetch-blog-form');
    const specificBlogEntryDiv = document.getElementById('specific-blog-entry');

    // Fetch and display all blog entries
    function fetchBlogEntries() {
        fetch('/api/blogentries/all')
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
                        <button onclick="editBlogEntry(${entry.post_id})">Edit</button>
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

    // Edit an existing blog entry
    window.editBlogEntry = function (postId) {
        fetch(`/api/blogentries/${postId}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('update-post-id').value = data.post_id;
                document.getElementById('update-title').value = data.title;
                document.getElementById('update-subtitle').value = data.subtitle;
                document.getElementById('update-blurb').value = data.blurb;
                document.getElementById('update-content').value = data.content;
                updateForm.style.display = 'block';
                blogForm.style.display = 'none';
            })
            .catch(error => console.error('Error:', error));
    };

    // Update the blog entry
    updateForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const updatedEntry = {
            title: document.getElementById('update-title').value,
            subtitle: document.getElementById('update-subtitle').value,
            blurb: document.getElementById('update-blurb').value,
            content: document.getElementById('update-content').value,
            is_published: true
        };

        const postId = document.getElementById('update-post-id').value;

        fetch(`/api/blogentries/${postId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedEntry)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Updated:', data);
            fetchBlogEntries(); // Refresh the list after updating
            updateForm.style.display = 'none';
            blogForm.style.display = 'block';
        })
        .catch(error => console.error('Error:', error));
    });

    // Cancel update
    cancelUpdateButton.addEventListener('click', function () {
        updateForm.style.display = 'none';
        blogForm.style.display = 'block';
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

    // Fetch a specific blog entry by its ID
    fetchBlogForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const blogId = document.getElementById('fetch-blog-id').value;

        // Fetch the blog entry by its ID
        fetch(`/api/blogentries/${blogId}`)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error("Blog entry not found.");
                }
            })
            .then(data => {
                // Display the specific blog entry
                document.getElementById('specific-title').innerText = data.title;
                document.getElementById('specific-subtitle').innerText = data.subtitle;
                document.getElementById('specific-blurb').innerText = data.blurb;
                document.getElementById('specific-content').innerText = data.content;
                specificBlogEntryDiv.style.display = 'block';
            })
            .catch(error => {
                alert(error.message);
                specificBlogEntryDiv.style.display = 'none';
            });
    });

    // Fetch blog entries on load
    fetchBlogEntries();
});
