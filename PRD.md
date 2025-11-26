# Guestbook Web Application - Product Requirements Document

## Project Overview
A simple guestbook web application that allows users to submit their name and a message, with all submissions displayed on the main page.

## Features

### Core Features
- **Message Submission**: Users can submit their name and a message through a web form
- **Message Display**: All submitted messages are displayed on the main page in chronological order (newest first)
- **Data Persistence**: Messages are stored in a SQLite database
- **Input Validation**: Basic validation to prevent empty submissions and enforce length limits

### Technical Requirements
- **Backend**: Flask (Python web framework)
- **Database**: SQLite for data storage
- **Frontend**: HTML/CSS (no JavaScript required)
- **Deployment**: Single command execution (python app.py)

### User Interface
- Clean, responsive design
- Form with two fields: Name and Message
- Success/error message display
- List of all submitted messages with timestamps
- Mobile-friendly layout

### Validation Rules
- Name field: Required, maximum 100 characters
- Message field: Required, maximum 500 characters
- Both fields are trimmed of whitespace

### Database Schema
`sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
`

## File Structure
`
guestbook/
â”œâ”€â”€ app.py                 # Main Flask application
â”œâ”€â”€ requirements.txt       # Python dependencies
â”œâ”€â”€ templates/
â”‚   â””â”€â”€ index.html        # Main page template
â”œâ”€â”€ static/
â”‚   â””â”€â”€ css/
â”‚       â””â”€â”€ style.css     # Styling
â”œâ”€â”€ .gitignore            # Git ignore file
â”œâ”€â”€ prd.md               # This document
â””â”€â”€ diary.txt            # Development notes
`

## Getting Started
1. Install dependencies: pip install -r requirements.txt
2. Run the application: python app.py
3. Open browser to: http://localhost:5000

## Future Enhancements (Optional)
- User authentication
- Message moderation
- Rich text formatting
- File uploads
- Admin panel
- API endpoints
