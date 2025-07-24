# Dashboard App - Replit Guide

## Overview

This is a Flask-based web application that provides user authentication, registration, and a personalized dashboard experience. The application follows a traditional MVC pattern with Flask as the backend framework, SQLAlchemy for database operations, and Bootstrap for the frontend UI.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy extension
- **Authentication**: Flask-Login for session management
- **Form Handling**: WTForms with Flask-WTF for form validation
- **Password Security**: Werkzeug's security utilities for password hashing
- **Session Management**: Flask's built-in session handling with configurable secret key

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default)
- **CSS Framework**: Bootstrap 5 with Replit Dark Theme
- **Icons**: Font Awesome 6.4.0
- **Charts**: Chart.js for dashboard visualizations
- **Theme**: Dark theme optimized for Replit environment

### Database Architecture
- **Primary Database**: SQLite (default) with support for PostgreSQL via DATABASE_URL
- **ORM**: SQLAlchemy with declarative base
- **Connection Pooling**: Configured with pool recycling and pre-ping for reliability

## Key Components

### Models (models.py)
- **User Model**: Handles user data with fields for username, email, password hash, first/last name, timestamps
- **Authentication Methods**: Password hashing/verification, full name generation
- **Flask-Login Integration**: UserMixin for session management

### Forms (forms.py)
- **RegistrationForm**: Complete user registration with validation
- **LoginForm**: User authentication form
- **ProfileForm**: User profile editing (incomplete in current code)
- **Custom Validators**: Username and email uniqueness validation

### Routes (routes.py)
- **Public Routes**: Home page, registration, login
- **Protected Routes**: Dashboard, profile (requires authentication)
- **Authentication Flow**: Registration → Login → Dashboard access
- **Error Handling**: Database rollback and user feedback via flash messages

### Templates
- **Base Template**: Common layout with navigation, Bootstrap integration
- **Authentication Pages**: Login and registration forms with validation feedback
- **Dashboard**: Personalized user dashboard with statistics and charts
- **Profile Management**: User profile viewing and editing interface

## Data Flow

1. **User Registration**: Form validation → Password hashing → Database storage → Redirect to login
2. **User Authentication**: Credential verification → Session creation → Dashboard access
3. **Dashboard Access**: Session verification → User data retrieval → Template rendering with user context
4. **Profile Management**: Authentication check → Form pre-population → Validation → Database update

## External Dependencies

### Python Packages
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-Login (authentication)
- Flask-WTF (form handling)
- WTForms (form validation)
- Werkzeug (utilities including security)

### Frontend Libraries
- Bootstrap 5 (Replit Dark Theme variant)
- Font Awesome 6.4.0 (icons)
- Chart.js (dashboard visualizations)

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- `DATABASE_URL`: Database connection string (defaults to SQLite)

## Deployment Strategy

### Development Setup
- **Entry Point**: main.py runs Flask development server on port 5000
- **Debug Mode**: Enabled for development with detailed error logging
- **Hot Reload**: Flask development server provides automatic reloading
- **Database Initialization**: Automatic table creation on first run

### Production Considerations
- **WSGI Configuration**: ProxyFix middleware for proper header handling behind proxies
- **Database Connection**: Pool management with connection recycling
- **Security**: Environment-based secret key configuration
- **Logging**: Debug-level logging configured for troubleshooting

### Replit-Specific Features
- **Host Configuration**: Bound to 0.0.0.0 for Replit's network setup
- **Theme Integration**: Uses Replit's dark theme Bootstrap variant
- **Port Configuration**: Configured for port 5000 (Replit standard)

The application is designed to be easily deployable on Replit with minimal configuration, while maintaining the flexibility to scale to production environments with proper environment variable configuration.