import logging

from mytodolists.custom_exceptions import InputNotValidError


class CustomValidators:

    @classmethod
    def validator_whitespaces(cls, string: str):
        try:
            string_clean = string.strip()
            if string_clean == '':
                return False
            return string_clean
        except AttributeError:
            return False

    @classmethod
    def params_validator(cls, title, description, tags):
        title_clean = cls.validator_whitespaces(title)
        description_clean = cls.validator_whitespaces(
            description
        )
        if not title_clean or not description_clean or type(tags) != list:
            logging.debug(
                f'Title: {title_clean}, desc: {description_clean}, tag: {tags}'
            )
            raise InputNotValidError('Please insert valid parameters')
        return title_clean, description_clean
