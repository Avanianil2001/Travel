# Project Overview

## Travel Blog Application

This Django-based travel blog application enables users to create and manage blog posts, share their travel experiences, and provide feedback. Users can sign up, log in, and manage their profiles, including uploading a profile picture. The platform includes a gallery view for posts, allowing users to browse all published content. There is also a feedback section where users can submit their thoughts about the platform or their travel experiences.

The project also includes a REST API, providing functionality for blog post creation, updating, and deletion. Admins and users can interact with the system both through the web interface and API.

### Features:
- **User Management**: Users can register, log in, and manage their profiles.
- **Blog Management**: Users can create, view, update, and delete their blog posts. Each post includes a title, content, place, and image.
- **Post Gallery**: All posts are viewable in a gallery format, with individual post views available.
- **Feedback Submission**: Users can submit feedback, which is stored and can be viewed by admins.
- **REST API**: The API provides endpoints for creating, updating, and deleting blog posts, with full CRUD functionality.

### API Endpoints (REST):
- **POST** `/api/create_post`: Create a new blog post.
- **PUT** `/api/update_post/<post_id>`: Update an existing blog post.
- **DELETE** `/api/delete_post/<post_id>`: Delete a blog post.
