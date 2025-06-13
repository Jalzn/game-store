from typing import List
from sqlmodel import Session, select
from app.customers.exceptions import *
from app.customers.models import Customer
from app.customers.schemas import CustomerCreate, CustomerUpdate

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

    def get_by_id(self, customer_id: int) -> Customer:
        customer = self.session.get(Customer, customer_id)
        if not customer:
            raise CustomerNotFoundException
        return customer

    def list_all(self) -> List[Customer]:
        return list(self.session.exec(select(Customer)))

    def update_customer(self, customer_id: int, schema: CustomerUpdate) -> Customer:
        customer = self.get_by_id(customer_id)

        if schema.email and not validate_email(schema.email):
            raise CustomerInvalidEmailException

        if schema.phone and not validate_phone(schema.phone):
            raise CustomerInvalidPhoneException

        # Evitar duplicação de email/telefone
        if (
            schema.email
            and schema.email != customer.email
            and self.exists_by_email(schema.email)
        ):
            raise CustomerAlreadyExistsException

        if (
            schema.phone
            and schema.phone != customer.phone
            and self.exists_by_phone(schema.phone)
        ):
            raise CustomerAlreadyExistsException

        if schema.name:
            customer.name = schema.name
        if schema.email:
            customer.email = schema.email
        if schema.phone:
            customer.phone = schema.phone

        self.session.add(customer)
        self.session.commit()
        self.session.refresh(customer)

        return customer

    def delete_customer(self, customer_id: int) -> None:
        customer = self.get_by_id(customer_id)
        self.session.delete(customer)
        self.session.commit()

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
