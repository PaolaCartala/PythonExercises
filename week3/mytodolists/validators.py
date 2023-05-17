def validator_whitespaces(string: str):
    try:
        string_clean = string.strip()
        if string_clean == '':
            return False
        return string_clean
    except AttributeError:
        return False
