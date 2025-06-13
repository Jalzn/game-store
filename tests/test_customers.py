from pytest import fixture
import pytest

from app.customers.exceptions import (
    CustomerAlreadyExistsException,
    CustomerInvalidEmailException,
    CustomerInvalidPhoneException,
    CustomerNotFoundException,
)
from app.customers.schemas import CustomerCreate, CustomerUpdate
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


def test_get_by_id_success(customers_service):
    schema = CustomerCreate(
        name="Jalmir", email="jalmir@email.com", phone="(38) 98401-0149"
    )
    created = customers_service.create_customer(schema)

    result = customers_service.get_by_id(created.id)

    assert result is not None
    assert result.id == created.id
    assert result.name == "Jalmir"


def test_get_by_id_not_found(customers_service):
    with pytest.raises(CustomerNotFoundException):
        customers_service.get_by_id(999)  # ID inexistente


def test_list_all(customers_service):
    # Garantir lista vazia no início
    result = customers_service.list_all()
    assert result == []

    # Criar dois clientes
    customers_service.create_customer(
        CustomerCreate(
            name="Cliente 1", email="cliente1@email.com", phone="(11) 99999-0001"
        )
    )
    customers_service.create_customer(
        CustomerCreate(
            name="Cliente 2", email="cliente2@email.com", phone="(11) 99999-0002"
        )
    )

    result = customers_service.list_all()
    assert len(result) == 2


def test_update_customer_success(customers_service):
    original = customers_service.create_customer(
        CustomerCreate(
            name="Original Name", email="original@email.com", phone="(11) 99999-0000"
        )
    )

    update_schema = CustomerUpdate(
        name="Updated Name", email="updated@email.com", phone="(11) 98888-0000"
    )

    updated = customers_service.update_customer(original.id, update_schema)

    assert updated.name == "Updated Name"
    assert updated.email == "updated@email.com"
    assert updated.phone == "(11) 98888-0000"


def test_update_customer_invalid_email(customers_service):
    customer = customers_service.create_customer(
        CustomerCreate(name="Test", email="test@email.com", phone="(11) 99999-0000")
    )

    update_schema = CustomerUpdate(email="invalid-email")

    with pytest.raises(CustomerInvalidEmailException):
        customers_service.update_customer(customer.id, update_schema)


def test_update_customer_invalid_phone(customers_service):
    customer = customers_service.create_customer(
        CustomerCreate(name="Test", email="test@email.com", phone="(11) 99999-0000")
    )

    update_schema = CustomerUpdate(phone="123456")

    with pytest.raises(CustomerInvalidPhoneException):
        customers_service.update_customer(customer.id, update_schema)


def test_update_customer_email_already_exists(customers_service):
    customers_service.create_customer(
        CustomerCreate(name="Customer A", email="a@email.com", phone="(11) 99999-0001")
    )
    customer_b = customers_service.create_customer(
        CustomerCreate(name="Customer B", email="b@email.com", phone="(11) 99999-0002")
    )

    update_schema = CustomerUpdate(email="a@email.com")

    with pytest.raises(CustomerAlreadyExistsException):
        customers_service.update_customer(customer_b.id, update_schema)


def test_update_customer_phone_already_exists(customers_service):
    customers_service.create_customer(
        CustomerCreate(name="Customer A", email="a@email.com", phone="(11) 99999-0001")
    )
    customer_b = customers_service.create_customer(
        CustomerCreate(name="Customer B", email="b@email.com", phone="(11) 99999-0002")
    )

    update_schema = CustomerUpdate(phone="(11) 99999-0001")

    with pytest.raises(CustomerAlreadyExistsException):
        customers_service.update_customer(customer_b.id, update_schema)


def test_delete_customer_success(customers_service):
    customer = customers_service.create_customer(
        CustomerCreate(
            name="To Delete", email="delete@email.com", phone="(11) 99999-0000"
        )
    )

    customers_service.delete_customer(customer.id)

    with pytest.raises(CustomerNotFoundException):
        customers_service.get_by_id(customer.id)


def test_delete_customer_not_found(customers_service):
    with pytest.raises(CustomerNotFoundException):
        customers_service.delete_customer(999)  # ID inexistente
