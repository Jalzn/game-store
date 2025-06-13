import pytest
from app.rentals.schemas import RentalCreate, RentalReturn
from app.rentals.exceptions import (
    RentalAlreadyActiveException,
    RentalNotFoundException,
    RentalAlreadyReturnedException,
)

from app.rentals.services import RentalService
from app.rentals.models import Rental
from app.customers.schemas import CustomerCreate
from app.games.schemas import GameCreate

from tests.fixtures import session


@pytest.fixture
def rental_service(session):
    return RentalService(session)


@pytest.fixture
def customer(session):
    from app.customers.services import CustomerService

    service = CustomerService(session)
    return service.create_customer(
        CustomerCreate(
            name="Test Customer", email="test@customer.com", phone="(11) 99999-9999"
        )
    )


@pytest.fixture
def game(session):
    from app.games.services import GameService

    service = GameService(session)
    return service.create_game(
        GameCreate(title="Test Game", genre="Action", platform="PC", price=59.99)
    )


def test_create_rental_success(rental_service, customer, game):
    rental = rental_service.create_rental(
        RentalCreate(customer_id=customer.id, game_id=game.id)
    )

    assert rental.id is not None
    assert rental.return_date is None
    assert rental.customer_id == customer.id
    assert rental.game_id == game.id


def test_cannot_rent_same_game_twice_without_return(rental_service, customer, game):
    rental_service.create_rental(RentalCreate(customer_id=customer.id, game_id=game.id))

    with pytest.raises(RentalAlreadyActiveException):
        rental_service.create_rental(
            RentalCreate(customer_id=customer.id, game_id=game.id)
        )


def test_return_rental_success(rental_service, customer, game):
    rental = rental_service.create_rental(
        RentalCreate(customer_id=customer.id, game_id=game.id)
    )

    returned = rental_service.return_rental(rental.id, RentalReturn())

    assert returned.return_date is not None


def test_return_already_returned_rental(rental_service, customer, game):
    rental = rental_service.create_rental(
        RentalCreate(customer_id=customer.id, game_id=game.id)
    )
    rental_service.return_rental(rental.id, RentalReturn())

    with pytest.raises(RentalAlreadyReturnedException):
        rental_service.return_rental(rental.id, RentalReturn())


def test_get_rental_not_found(rental_service):
    with pytest.raises(RentalNotFoundException):
        rental_service.get_by_id(999)


def test_list_all_rentals(rental_service, customer, game):
    rental_service.create_rental(RentalCreate(customer_id=customer.id, game_id=game.id))
    rentals = rental_service.list_all()
    assert len(rentals) >= 1
