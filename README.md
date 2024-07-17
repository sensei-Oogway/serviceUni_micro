# University Services Web Application

This Django application serves as a comprehensive platform for university students to manage enrollment bookings, access pharmacy services, and schedule consultations. The project employs a quasi microservice architecture to enhance modularity and scalability, with Nginx acting as an API gateway for seamless communication between services. Data is managed using a PostgreSQL database.

## Features

- **Enrollment Booking:** Students can book their course enrollments through the application.
- **Pharmacy Services:** Access to pharmacy services such as ordering medications, checking availability, etc.
- **Consultation Scheduling:** Schedule appointments with university staff or counselors.

## Technologies and Architecture

- **Microservice Architecture:** Utilizes a microservice-based approach for modularity and scalability, its not a perfectly microservice-based architecture, but tries to mimic one, by running each Django app in a different server.
- **Nginx as API Gateway:** Nginx is configured as an API gateway to route requests to appropriate apps.
- **Django:** Backend framework for developing robust web applications.
- **PostgreSQL:** Relational database management system used for data storage.

## Installation

To run this application locally, follow these steps:

1. Clone the repository
2. Set up PostgreSQL database:
  - Create a PostgreSQL database for the application.
  - Update database settings in `settings.py` with your database credentials.
3. Apply database migrations
4. Start the Django development server


