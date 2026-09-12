from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime

from database import Base, engine, SessionLocal
import models
from schemas import TicketCreate, TicketUpdate


app = FastAPI()

templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
@app.get("/create-ticket")
def create_ticket_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_ticket.html",
        context={}
    )  

@app.get("/ticket/{ticket_id}")
def ticket_page(request: Request, ticket_id: str):
    return templates.TemplateResponse(
        request=request,
        name="ticket_detail.html",
        context={"ticket_id": ticket_id}
    )      


@app.post("/api/tickets")
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db)
):
    last_ticket = db.query(models.Ticket).order_by(
        models.Ticket.id.desc()
    ).first()

    if last_ticket is None:
        next_number = 1
    else:
        next_number = last_ticket.id + 1

    new_ticket_id = f"TKT-{next_number:03d}"

    new_ticket = models.Ticket(
        ticket_id=new_ticket_id,
        customer_name=ticket.customer_name,
        customer_email=ticket.customer_email,
        subject=ticket.subject,
        description=ticket.description,
        status="Open"
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "ticket_id": new_ticket.ticket_id,
        "customer_name": new_ticket.customer_name,
        "status": new_ticket.status,
        "created_at": new_ticket.created_at
    }


@app.get("/api/tickets")
def list_tickets(
    status: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Ticket)

    if status:
        query = query.filter(
            models.Ticket.status == status
        )

    if search:
        search_text = f"%{search}%"

        query = query.filter(
            or_(
                models.Ticket.ticket_id.like(search_text),
                models.Ticket.customer_name.like(search_text),
                models.Ticket.customer_email.like(search_text),
                models.Ticket.subject.like(search_text),
                models.Ticket.description.like(search_text)
            )
        )

    tickets = query.order_by(
        models.Ticket.created_at.desc()
    ).all()

    return [
        {
            "ticket_id": ticket.ticket_id,
            "customer_name": ticket.customer_name,
            "customer_email": ticket.customer_email,
            "subject": ticket.subject,
            "description": ticket.description,
            "status": ticket.status,
            "created_at": ticket.created_at
        }
        for ticket in tickets
    ]


@app.get("/api/tickets/{ticket_id}")
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.ticket_id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    notes = db.query(models.Note).filter(
        models.Note.ticket_id == ticket.ticket_id
    ).order_by(models.Note.created_at.asc()).all()

    return {
        "ticket_id": ticket.ticket_id,
        "customer_name": ticket.customer_name,
        "customer_email": ticket.customer_email,
        "subject": ticket.subject,
        "description": ticket.description,
        "status": ticket.status,
        "created_at": ticket.created_at,
        "updated_at": ticket.updated_at,
        "notes": [
            {
                "id": note.id,
                "note_text": note.note_text,
                "created_at": note.created_at
            }
            for note in notes
        ]
    }


@app.put("/api/tickets/{ticket_id}")
def update_ticket(
    ticket_id: str,
    data: TicketUpdate,
    db: Session = Depends(get_db)
):
    ticket = db.query(models.Ticket).filter(
        models.Ticket.ticket_id == ticket_id
    ).first()

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    if data.status not in ["Open", "In Progress", "Closed"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status"
        )

    ticket.status = data.status
    ticket.updated_at = datetime.utcnow()

    if data.notes and data.notes.strip():
        new_note = models.Note(
            ticket_id=ticket.ticket_id,
            note_text=data.notes.strip()
        )

        db.add(new_note)

    db.commit()
    db.refresh(ticket)

    return {
        "ticket_id": ticket.ticket_id,
        "status": ticket.status,
        "updated_at": ticket.updated_at,
        "message": "Ticket updated successfully"
    }