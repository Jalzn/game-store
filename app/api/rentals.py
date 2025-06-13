from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.rentals.schemas import RentalCreate, RentalReturn
from app.rentals.services import RentalService
from app.rentals.exceptions import (
    RentalAlreadyActiveException,
    RentalNotFoundException,
    RentalAlreadyReturnedException,
)

router = APIRouter(prefix="/rentals", tags=["rentals"])


@router.post("/")
def create_rental(schema: RentalCreate, session: Session = Depends(get_session)):
    service = RentalService(session)
    try:
        rental = service.create_rental(schema)
        return rental
    except RentalAlreadyActiveException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Rental already active for this customer and game",
        )


@router.put("/{rental_id}/return")
def return_rental(
    rental_id: int, schema: RentalReturn, session: Session = Depends(get_session)
):
    service = RentalService(session)
    try:
        return service.return_rental(rental_id, schema)
    except RentalNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Rental not found"
        )
    except RentalAlreadyReturnedException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Rental already returned"
        )


@router.get("/")
def list_rentals(session: Session = Depends(get_session)):
    service = RentalService(session)
    return service.list_all()
