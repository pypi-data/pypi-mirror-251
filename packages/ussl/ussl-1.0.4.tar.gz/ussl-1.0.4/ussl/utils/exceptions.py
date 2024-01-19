from typing import List


class SOARException(Exception):
    _return_code: int = 1

    @property
    def return_code(self):
        return self._return_code


class ProtocolError(SOARException):
    pass


class ProtocolConnectionError(SOARException):
    pass


class ProtocolExecutionError(SOARException):
    pass


class ValidationError(SOARException):
    args: List[str]

    def __init__(self, property_names: List[str] = None) -> None:
        self.args = property_names


class NoInputData(ValidationError):
    _return_code: int = 1
    _MISSING_INPUTS = 'Отсутствуют обязательные входные аргументы: {names}.'

    def __str__(self):
        return self._MISSING_INPUTS.format(names=', '.join(self.args))


class NoSecrets(ValidationError):
    _return_code: int = 1
    _MISSING_SECRETS = 'Отсутствуют секреты: {names}.'

    def __str__(self):
        return self._MISSING_SECRETS.format(names=', '.join(self.args))


class BadSecrets(ValidationError):
    _return_code: int = 1
    _BAD_SECRETS = 'Переданы невалидные секреты: {err}.'

    def __str__(self):
        return self._BAD_SECRETS.format(err=self.error)


class PermissionsError(SOARException):
    _return_code: int = 1
    _PERMISSIONS_ERROR = 'Отсутствуют необходимые права: {err}.'

    def __str__(self):
        return self._PERMISSIONS_ERROR.format(err=', '.join(self.args))
