import sys
import json
import warnings

import pathlib

from marshmallow import Schema, exceptions

from Libraries.USSL.ussl.utils.exceptions import ValidationError, SOARException

warnings.filterwarnings("ignore")


class BaseFunction:
    """
    Является базовым классом для всех скриптов, участвующих в обогащении и реагировании.

    При использовании класса необходимо реализовать метод ``function``.

    Автоматически принимаемые значения:

        ``input_json``: Первым аргументом принимает информацию, переданную на вход плейбука;

        ``secrets``: Вторым аргументом приниает секреты.

        ``ensure_ascii``: Указывает, должны ли символы не из набора ASCII быть экранированы. По умолчанию False.


    """
    input_model: Schema = None
    secrets_model: Schema = None

    def __init__(self, ensure_ascii: bool = False) -> None:
        """
        Инициализирует экземпляр класса.

        Args:
            ensure_ascii (bool): Указывает, должны ли символы не из набора ASCII быть экранированы. По умолчанию True.
        Returns:
            None
        """
        inputs = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
        secrets = pathlib.Path(sys.argv[2]).read_text(encoding='utf-8')
        self._input_json: dict = json.loads(inputs)
        self._secrets: dict = json.loads(secrets)

        self.ensure_ascii = ensure_ascii
        if self.input_model is not None:
            try:
                self.input_json = self.input_model.__init__().loads(inputs)
            except exceptions.ValidationError as e:
                if isinstance(e.messages, dict):
                    formatted_names = ', '.join(e.messages.keys())
                    self.output(f"Отсутствуют входные данные: {formatted_names}", 1)
                else:
                    self.output(f"Ошибка валидации входных данных: {e.__str__()}", 1)
        if self.secrets_model is not None:
            try:
                self.secrets = self.secrets_model.__init__().loads(secrets)
            except exceptions.ValidationError as e:
                if isinstance(e.messages, dict):
                    formatted_names = ', '.join(e.messages.keys())
                    self.output(f"Отсутствуют секреты: {formatted_names}", 1)
                else:
                    self.output(f"Ошибка валидации входных данных: {e.__str__()}", 1)

        try:
            self.input_json = self.validate_input(self.input_json
                                                  if self.input_model is not None
                                                  else self._input_json)
            self.secrets = self.validate_secrets(self.secrets
                                                 if self.secrets is not None
                                                 else self._secrets)
        except ValidationError as e:
            self.output(e.__str__(), e.return_code)
        except NotImplementedError:
            if self.input_model is None:
                self.input_json = self._input_json.copy()
            if self.secrets_model is None:
                self.secrets = self._secrets.copy()

        try:
            result, message = self.function()
        except SOARException as e:
            self.output(e.__str__(), e.return_code)
        except NotImplementedError:
            raise Exception('Метод function не реализован')
        else:
            self.output(result, message)

    def validate_input(self, input_json: dict) -> dict:
        """
        Метод для дополнительной валидации входных данных.

        При ошибке валидации выбрасывает ValidationError
        """
        raise NotImplementedError

    def validate_secrets(self, secrets: dict) -> dict:
        """
        Метод для дополнительной валидации секретов.

        При ошибке валидации выбрасывает ValidationError
        """
        raise NotImplementedError

    def function(self) -> (dict, str):
        """
        В этом методе необходимо реализовать функцию по обогащению
        или реагированию.

        Методу доступны переменные input_json и secrets.

        Для получения данных используйте переменные input_json и secrets класса BaseFunction.
        Для вывода ошибок необходимо использовать исключения из модуля exceptions.
        Returns:
            (dict, str): Результат обогащения или реагирования и сообщение о результате.
        """
        raise NotImplementedError('Метод function не реализован')

    def output(self,
               message: str,
               return_code: int = 0,
               **kwargs) -> None:
        """
        Выводит результат работы скрипта в формате JSON.

        Args:
            message (str): Сообщение о результате выполнения скрипта, которое будет выведено.
            return_code (int): Код возврата, указывающий на успешное выполнение (0) или ошибку (ненулевое значение).
            **kwargs: Дополнительные именованные аргументы. Например, результат сбора данных.

        Returns:
            None
        """
        # Обновляем входной JSON с результатом или сообщением об ошибке
        self._input_json['error' if return_code else 'result'] = message

        # Обновляем входной JSON с дополнительными аргументами
        self._input_json.update(kwargs)

        # Выводим входной JSON в форматированном виде
        print(json.dumps(self._input_json, ensure_ascii=self.ensure_ascii))

        # Завершаем выполнение скрипта с кодом 0 для успешного выполнения или ненулевым для ошибки
        exit(return_code)
