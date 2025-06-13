from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.database import get_session
from app.customers.schemas import CustomerCreate
from app.customers.services import CustomerService
from app.customers.exceptions import (
    CustomerAlreadyExistsException,
    CustomerInvalidEmailException,
    CustomerInvalidPhoneException,
)

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/")
def create_customer(schema: CustomerCreate, session: Session = Depends(get_session)):
    service = CustomerService(session)
    try:
        customer = service.create_customer(schema)
        return customer
    except CustomerAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Customer already exists"
        )
    except CustomerInvalidEmailException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email"
        )
    except CustomerInvalidPhoneException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone"
        )
