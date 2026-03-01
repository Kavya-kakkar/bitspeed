from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database import get_db
from models import Contact

app = FastAPI()


class IdentifyRequest(BaseModel):
    email: Optional[str] = None
    phoneNumber: Optional[str] = None


@app.post("/identify")
def identify(data: IdentifyRequest, db: Session = Depends(get_db)):

    
    if not data.email and not data.phoneNumber:
        raise HTTPException(
            status_code=400,
            detail="At least one field (email or phoneNumber) is required"
        )

    email = data.email
    phone = data.phoneNumber


    matched_contacts = db.query(Contact).filter(
        or_(
            Contact.email == email,
            Contact.phoneNumber == phone
        )
    ).all()

  
    if not matched_contacts:
        new_contact = Contact(
            email=email,
            phoneNumber=phone,
            linkPrecedence="primary",
            linkedId=None
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)

        return {
            "contact": {
                "primaryContactId": new_contact.id,
                "emails": [email] if email else [],
                "phoneNumbers": [phone] if phone else [],
                "secondaryContactIds": []
            }
        }


    primary_candidates = []

    for contact in matched_contacts:
        if contact.linkPrecedence == "primary":
            primary_candidates.append(contact)
        else:
            primary = db.query(Contact).filter(
                Contact.id == contact.linkedId
            ).first()
            if primary:
                primary_candidates.append(primary)

  
    primary_candidates = list({c.id: c for c in primary_candidates}.values())

  
    primary_contact = sorted(
        primary_candidates,
        key=lambda x: x.createdAt
    )[0]

   
    for contact in primary_candidates:
        if contact.id != primary_contact.id:
            contact.linkPrecedence = "secondary"
            contact.linkedId = primary_contact.id

    db.commit()

    
    all_related = db.query(Contact).filter(
        or_(
            Contact.id == primary_contact.id,
            Contact.linkedId == primary_contact.id
        )
    ).all()

    existing_emails = {c.email for c in all_related if c.email}
    existing_phones = {c.phoneNumber for c in all_related if c.phoneNumber}

    
    if (email and email not in existing_emails) or \
       (phone and phone not in existing_phones):

        new_secondary = Contact(
            email=email,
            phoneNumber=phone,
            linkPrecedence="secondary",
            linkedId=primary_contact.id
        )
        db.add(new_secondary)
        db.commit()
        db.refresh(new_secondary)

        all_related.append(new_secondary)

 
    emails = list({c.email for c in all_related if c.email})
    phones = list({c.phoneNumber for c in all_related if c.phoneNumber})
    secondary_ids = [
        c.id for c in all_related
        if c.linkPrecedence == "secondary"
    ]

  
    if primary_contact.email in emails:
        emails.remove(primary_contact.email)
        emails.insert(0, primary_contact.email)

    if primary_contact.phoneNumber in phones:
        phones.remove(primary_contact.phoneNumber)
        phones.insert(0, primary_contact.phoneNumber)

    return {
        "contact": {
            "primaryContactId": primary_contact.id,
            "emails": emails,
            "phoneNumbers": phones,
            "secondaryContactIds": secondary_ids
        }
    }