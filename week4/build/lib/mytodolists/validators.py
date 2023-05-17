import logging

from mytodolists.custom_exceptions import InputNotValidException


def validator_whitespaces(string: str):
    try:
        string_clean = string.strip()
        if string_clean == '':
            return False
        return string_clean
    except AttributeError:
        return False


def params_validator(title, description, tags):
    title_clean = validator_whitespaces(title)
    description_clean = validator_whitespaces(
        description
    )
    if not title_clean or not description_clean or type(tags) != list:
        logging.error(
            f'Title: {title_clean}, desc: {description_clean}, tag: {tags}'
        )
        raise InputNotValidException('Please insert valid parameters')
    return title_clean, description_clean
