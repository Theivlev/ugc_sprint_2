import requests


def check_auth(url):
    """Переход на нужный адрес и получение данных."""

    def check_auth(func):
        def wrapper(*args, **kwargs):
            try:
                data = requests.get(url).json()
            except Exception as e:
                return {"message": f"ошибка {e}"}
            if isinstance(data, dict) and data["detail"] == "Unauthorized":
                return {"message": "No permissions. Authorization."}
            return func(data, *args, **kwargs)

        wrapper.__name__ = func.__name__
        return wrapper

    return check_auth
