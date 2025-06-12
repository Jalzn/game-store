from sqlmodel import Session, select
from app.customers.exceptions import (
    CustomerAlreadyExistsException,
    CustomerInvalidEmailException,
    CustomerInvalidPhoneException,
)
from app.customers.models import Customer
from app.customers.schemas import CustomerCreate

from app.utils import validate_email, validate_phone


class CustomerService:
    def __init__(self, session: Session):
        self.session = session

    def create_customer(self, schema: CustomerCreate) -> Customer:
        if not validate_email(schema.email):
            raise CustomerInvalidEmailException

        if not validate_phone(schema.phone):
            raise CustomerInvalidPhoneException

        if self.exists_by_email(schema.email):
            raise CustomerAlreadyExistsException

        if self.exists_by_phone(schema.phone):
            raise CustomerAlreadyExistsException

        customer = Customer(name=schema.name, email=schema.email, phone=schema.phone)

        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)

        return customer

    def exists_by_email(self, email: str) -> bool:
        customer = self.session.exec(
            select(Customer).where(Customer.email == email)
        ).first()
        return True if customer else False

    def exists_by_phone(self, phone: str) -> bool:
        customer = self.session.exec(
            select(Customer).where(Customer.phone == phone)
        ).first()
        return True if customer else False
