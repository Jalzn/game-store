class CustomerInvalidEmailException(Exception):
    pass


class CustomerInvalidPhoneException(Exception):
    pass


class CustomerAlreadyExistsException(Exception):
    pass


class CustomerNotFoundException(Exception):
    pass
