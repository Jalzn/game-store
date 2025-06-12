from pytest import fixture
import pytest

from app.customers.exceptions import (
    CustomerAlreadyExistsException,
    CustomerInvalidEmailException,
    CustomerInvalidPhoneException,
)
from app.customers.schemas import CustomerCreate
from app.customers.services import CustomerService

from tests.fixtures import session


@fixture
def customers_service(session):
    return CustomerService(session)


def test_customer_success(customers_service):
    schema = CustomerCreate(
        name="Jalmir Ferreira", email="jalmir@email.com", phone="(38) 98401-0149"
    )

    customer = customers_service.create_customer(schema)

    assert customer is not None
    assert customer.id is not None
    assert customer.email == "jalmir@email.com"
    assert customer.phone == "(38) 98401-0149"


def test_customer_already_exists_by_email(customers_service):
    schema = CustomerCreate(
        name="Foo Bar", email="foobar@email.com", phone="(38) 98401-0149"
    )

    customers_service.create_customer(schema)

    schema = CustomerCreate(
        name="Foo Bar", email="foobar@email.com", phone="(38) 98401-0148"
    )

    with pytest.raises(CustomerAlreadyExistsException):
        customers_service.create_customer(schema)


def test_customer_already_exists_by_phone(customers_service):
    schema = CustomerCreate(
        name="Foo Bar", email="foobar@email.com", phone="(38) 98401-0149"
    )

    customers_service.create_customer(schema)

    schema = CustomerCreate(
        name="Foo Bar", email="barfoo@email.com", phone="(38) 98401-0149"
    )

    with pytest.raises(CustomerAlreadyExistsException):
        customers_service.create_customer(schema)


def test_customer_invalid_email(customers_service):
    schema = CustomerCreate(
        name="Foobar", email="invalido-email", phone="(38) 98401-0149"
    )

    with pytest.raises(CustomerInvalidEmailException):
        customers_service.create_customer(schema)


def test_customer_invalid_phone(customers_service):
    schema = CustomerCreate(name="Foobar", email="teste@email.com", phone="123456")

    with pytest.raises(CustomerInvalidPhoneException):
        customers_service.create_customer(schema)
