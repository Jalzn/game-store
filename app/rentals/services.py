from datetime import datetime
from typing import List
from sqlmodel import Session, select
from app.rentals.models import Rental
from app.rentals.schemas import RentalCreate, RentalReturn
from app.rentals.exceptions import (
    RentalNotFoundException,
    RentalAlreadyActiveException,
    RentalAlreadyReturnedException,
)


class RentalService:
    def __init__(self, session: Session):
        self.session = session

    def create_rental(self, schema: RentalCreate) -> Rental:
        # Verificar se o cliente já tem esse jogo alugado e ainda não devolveu
        existing_rental = self.session.exec(
            select(Rental).where(
                (Rental.customer_id == schema.customer_id)
                & (Rental.game_id == schema.game_id)
                & (Rental.return_date == None)
            )
        ).first()

        if existing_rental:
            raise RentalAlreadyActiveException

        rental = Rental(customer_id=schema.customer_id, game_id=schema.game_id)
        self.session.add(rental)
        self.session.commit()
        self.session.refresh(rental)
        return rental

    def return_rental(self, rental_id: int, schema: RentalReturn) -> Rental:
        rental = self.session.get(Rental, rental_id)
        if not rental:
            raise RentalNotFoundException

        if rental.return_date is not None:
            raise RentalAlreadyReturnedException

        rental.return_date = schema.return_date or datetime.now()

        self.session.add(rental)
        self.session.commit()
        self.session.refresh(rental)
        return rental

    def get_by_id(self, rental_id: int) -> Rental:
        rental = self.session.get(Rental, rental_id)
        if not rental:
            raise RentalNotFoundException
        return rental

    def list_all(self) -> List[Rental]:
        return list(self.session.exec(select(Rental)))
