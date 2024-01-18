import base64
import json
import re
from io import StringIO

import yaml
from pydantic import ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError
from requests import PreparedRequest


class PydanticErrorInfo():
    def __init__(self, field):
        self.field = field
        self.__error_list = []

    def __add_error(self, message, value):
        self.__error_list.append((message, value))

    def raise_error(self):
        if len(self.__error_list) == 0:
            return

        validation_errors: list[InitErrorDetails] = list()
        for (message, value) in self.__error_list:
            validation_errors.append(
                InitErrorDetails(
                    type=PydanticCustomError("static_validation_check", message),
                    loc=(),
                    input=value,
                    ctx={},
                )
            )

        raise ValidationError.from_exception_data(title='static validation error', line_errors=validation_errors)

    def verify_alpha(self, allow_none, value):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Alpha validation is only for strings', value)
        else:
            allowed_chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
            for ch in value:
                if ch not in allowed_chars:
                    self.__add_error("Failing to pass validation: 'alpha'", value)
                    break

    def verify_alphanum(self, allow_none, value):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Alphanum validation is only for strings', value)
        else:
            allowed_chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
            for ch in value:
                if ch not in allowed_chars:
                    self.__add_error("Failing to pass validation: 'alphanum'", value)
                    break

    def verify_min(self, value, constraint):
        if not isinstance(value, int) and not isinstance(value, float):
            self.__add_error('`min` validation is only for numeric values', value)
        elif value < constraint:
            self.__add_error("Failing to pass validation: 'min'", value)

    def verify_max(self, value, constraint):
        if not isinstance(value, int) and not isinstance(value, float):
            self.__add_error('`max` validation is only for numeric values', value)
        elif value > constraint:
            self.__add_error("Failing to pass validation: 'max'", value)

    def verify_oneof(self, value, allowed_values):
        if not isinstance(value, str):
            self.__add_error('`oneof` validation is only for string values', value)
        elif value not in allowed_values:
            self.__add_error("Failing to pass validation: 'oneof'", value)

    def verify_min_length(self, value, constraint):
        if not isinstance(value, str) and not isinstance(value, list):
            self.__add_error('`min_length` validation is only for strings and lists.', value)
        elif len(value) < constraint:
            self.__add_error("Failing to pass validation: 'min_length'", value)

    def verify_max_length(self, value, constraint):
        if not isinstance(value, str) and not isinstance(value, list):
            self.__add_error('`max_length` validation is only for strings and lists.', value)
        elif len(value) > constraint:
            self.__add_error("Failing to pass validation: 'max_length'", value)

    def verify_base64(self, allow_none, value):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Base64 validation is only for strings', value)
        else:
            if not self.__is_base_64(value):
                self.__add_error("Failing to pass validation: 'base64'", value)

    def __is_base_64(self, value):
        try:
            base64.b64decode(value)
            return True
        except:  # noqa
            return False

    def __is_safe_url_base_64(self, value):
        try:
            base64.urlsafe_b64decode(value)
            return True
        except:  # noqa
            return False

    def verify_email(self, allow_none, value):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Email validation is only for strings', value)
        else:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            if not re.fullmatch(regex, value):
                self.__add_error("Failing to pass validation: 'email'", value)

    def verify_url(self, allow_none, value):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('URL validation is only for strings', value)
        else:
            prepared_request = PreparedRequest()
            try:
                prepared_request.prepare_url(value, None)
                return prepared_request.url
            except: # noqa
                self.__add_error("Failing to pass validation: 'url'", value)

    def verify_contain(self, allow_none, value, pattern):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Contain validation is only for strings', value)
        else:
            if pattern not in value:
                self.__add_error("Failing to pass validation: 'contain'", value)

    def verify_not_contain(self, allow_none, value, pattern):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Not contain validation is only for strings', value)
        else:
            if pattern in value:
                self.__add_error("Failing to pass validation: 'not_contain'", value)

    def verify_string_start_with(self, allow_none, value, pattern):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Starts with validation is only for strings', value)
        else:
            if not value.startswith(pattern):
                self.__add_error("Failing to pass validation: 'string_start_with'", value)

    def verify_string_not_start_with(self, allow_none, value, pattern):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Not starts with validation is only for strings', value)
        else:
            if value.startswith(pattern):
                self.__add_error("Failing to pass validation: 'string_not_start_with'", value)

    def verify_string_end_with(self, allow_none, value, pattern):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Ends with validation is only for strings', value)
        else:
            if not value.endswith(pattern):
                self.__add_error("Failing to pass validation: 'string_end_with'", value)

    def verify_string_not_end_with(self, allow_none, value, pattern):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Not ends with validation is only for strings', value)
        else:
            if value.endswith(pattern):
                self.__add_error("Failing to pass validation: 'string_not_end_with'", value)

    def verify_yaml(self, allow_none, value):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('Not ends with validation is only for strings', value)
        else:
            a = yaml.safe_load(StringIO(value))
            if not isinstance(a, dict):
                self.__add_error("Failing to pass validation: 'yaml'", value)

    def verify_jwt(self, allow_none, value):
        if allow_none and value is None:
            return

        if value is None:
            self.__add_error('Should not be null', value)
        elif not isinstance(value, str):
            self.__add_error('JWT validation is only for strings', value)
        else:
            comps = value.split('.')
            if len(comps) != 3:
                self.__add_error("Failing to pass validation: 'jwt'", value)
            elif not self.__is_safe_url_base_64(comps[0]) or not self.__is_safe_url_base_64(comps[1]):
                self.__add_error("Failing to pass validation: 'jwt'", value)
            else:
                p1 = base64.urlsafe_b64decode(comps[0]).decode('utf-8')
                p2 = base64.urlsafe_b64decode(comps[1]).decode('utf-8')

                try:
                    json.loads(p1)
                    json.loads(p2)
                except: # noqa
                    self.__add_error("Failing to pass validation: 'jwt'", value)
