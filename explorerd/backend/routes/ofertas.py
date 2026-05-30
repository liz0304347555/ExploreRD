from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Oferta
from schemas import OfertaResponse
from typing import List

router = APIRouter(prefix="/ofertas", tags=["Ofertas"])

@router.get("/", response_model=List[OfertaResponse])
def get_ofertas(db: Session = Depends(get_db)):
    return db.query(Oferta).filter(Oferta.activo == True).all()

@router.get("/{oferta_id}", response_model=OfertaResponse)
def get_oferta(oferta_id: int, db: Session = Depends(get_db)):
    oferta = db.query(Oferta).filter(Oferta.id == oferta_id).first()
    if not oferta:
        raise HTTPException(status_code=404, detail="Oferta no encontrada")
    return oferta
