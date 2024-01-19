def can_be_int(string: str) -> bool:
    try:
        int(string)
        return True
    except:
        return False
