from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import ContactoMensaje
from schemas import ContactoCreate, ContactoResponse

router = APIRouter(prefix="/contacto", tags=["Contacto"])

@router.post("/", response_model=ContactoResponse)
def enviar_mensaje(contacto: ContactoCreate, db: Session = Depends(get_db)):
    nuevo = ContactoMensaje(**contacto.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
