# adBridge: a django mini-project

## Overview

The Classifieds - `adBridge` is a web application that allows users to post, browse, and interact with classified ads across various categories like jobs, rentals, sales, services, and more. The platform facilitates direct communication between buyers and sellers.

## Features

- **Ad Posting:** Users can create ads with details like type, title, description, contact info, price, and visibility settings.
- **User Interaction:** Buyers can send messages to sellers regarding the ads, and receive replies.
- **CRUD Operations:** Users can create, edit, and delete ads and messages of their own.
- **Category Management:** Categories are created and managed via Django Admin.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/rupesh-ps/mini-project.git
    cd mini-project
    ```

2. Set up the environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Migrate the database:
    ```bash
    python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

5. Run the server:
    ```bash
    python manage.py runserver
    ```

6. Visit `http://127.0.0.1:8000/` in your browser.

## Project Structure

- `ads/` - Models, views, and templates for ads.
- `ad_chat/` - Handles buyer-seller messaging.
- `static/` - CSS, JS, and other static files.
- `templates/` - HTML templates.
