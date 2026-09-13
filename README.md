# Support CRM System

A full-stack customer support ticket management system built using FastAPI, SQLite, SQLAlchemy, Jinja2, HTML, CSS, and JavaScript.

## Live Demo

https://support-crm-production-ba42.up.railway.app

## GitHub Repository

https://github.com/AISANSHAIKH321/support-crm

## Features

- Create customer support tickets
- Auto-generated ticket IDs
- Automatic ticket creation timestamp
- View all support tickets
- Search tickets by ticket ID, customer name, customer email, issue title, and description
- Filter tickets by status
- Ticket statuses: Open, In Progress, Closed
- View complete ticket details
- Update ticket status
- Add notes and comments
- Responsive web interface
- REST API backend

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy

### Database

- SQLite

### Frontend

- HTML
- CSS
- JavaScript
- Jinja2 Templates

### Deployment

- Railway

## Project Structure

support-crm/
    main.py
    database.py
    models.py
    schemas.py
    requirements.txt
    .gitignore
    templates/
        index.html
        create_ticket.html
        ticket_detail.html

## API Endpoints

- POST /api/tickets - Create a new ticket
- GET /api/tickets - List tickets with search and status filters
- GET /api/tickets/{ticket_id} - Get ticket details and notes
- PUT /api/tickets/{ticket_id} - Update ticket status and add notes

## Local Setup

1. Clone the repository:

git clone https://github.com/AISANSHAIKH321/support-crm.git

2. Open the project:

cd support-crm

3. Create virtual environment:

python -m venv venv

4. Activate virtual environment on Windows:

venv\Scripts\activate

5. Install dependencies:

pip install -r requirements.txt

6. Run the application:

uvicorn main:app --reload

7. Open in browser:

http://127.0.0.1:8000

## Database

The application uses SQLite with SQLAlchemy ORM.

Tables:

- tickets
- notes

## Deployment

The application is deployed on Railway and connected to GitHub for automatic deployments.

## Author

Aisan Shaikh

GitHub:
https://github.com/AISANSHAIKH321

LinkedIn:
https://linkedin.com/in/aisan-shaikh5b47a3250