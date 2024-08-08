# Django Chat Application

## Overview

This Django chat application provides a platform for users to engage in real-time chat conversations. Users can register, log in, create chat rooms, send messages, and interact with other participants. The project also includes features like direct messaging, friend management, and profile viewing.

## Features

- **User Authentication**
  - **Register**: Users can create an account.
  - **Login**: Registered users can log in to their account.
  - **Logout**: Users can log out of their session.
  - **Password Change**: Logged-in users can change their password.

- **Chat Functionality**
  - **Create Chat Rooms**: Users can create new chat rooms.
  - **View Chat Rooms**: All chat rooms are displayed on the main chat page.
  - **Chat Room Details**: Users can view and participate in conversations within a specific chat room.
  - **Send Messages**: Users can send messages in chat rooms they are participants in.
  - **Edit and Delete Messages**: Users can edit or delete their messages.

- **Direct Messaging**
  - **Create Direct Chats**: Users can start direct chat sessions with others.
  - **Send Direct Messages**: Users can send and receive direct messages.

- **Profile Management**
  - **View Profile**: Users can view their own profile or other users' profiles.
  - **Add Friends**: Users can add other users as friends.
  - **View Friends**: Users can view a list of their friends.

- **Search Functionality**
  - **Search Chats and Users**: Users can search for specific chat rooms or users.

- **Commenting and Notifications**
  - **Send Comments**: Users can submit comments via a form.
  - **Email Notifications**: Notifications are sent to the admin email when a comment is submitted.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
3. **Run database migrations:**
   ```bash
   python manage.py migrate
4. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
5. **Start the development server:**
   ```bash
   python manage.py runserver
## Folder Structure

- **base/:** Contains the Django app's templates, forms, models, and views.
- **templates/:** Contains HTML files for the front-end pages.
- **urls.py:** Defines URL patterns for the application.
- **models.py:** Defines the database models (Chat, Message, CustomUser).
- **forms.py:** Contains form classes for user registration, login, message sending, etc.

## Contributing
If you'd like to contribute to the project, please fork the repository and use a feature branch. Pull requests are welcome.
