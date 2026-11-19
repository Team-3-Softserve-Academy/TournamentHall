import re

FORBIDDEN_SYMBOLS_PATTERN = re.compile(r"[;'[\].,()]")
ALLOWED_ROLES = {"lord", "knight", "commonfolk"}


def has_forbidden_symbols(value: str) -> bool:
    return bool(FORBIDDEN_SYMBOLS_PATTERN.search(value))


def validate_registration_form(form_data: dict) -> list[str]:
    errors = []

    login = (form_data.get("login") or "").strip()
    password = form_data.get("password") or ""
    in_game_name = (form_data.get("in_game_name") or "").strip()
    role = (form_data.get("role") or "").strip().lower()
    house = (form_data.get("house") or "").strip()
    image_url = (form_data.get("image_url") or "").strip()

    if not login:
        errors.append("Логін є обов'язковим.")
    elif has_forbidden_symbols(login):
        errors.append("Логін містить заборонені символи: ; ' [ ] . , ( )")

    if not password:
        errors.append("Пароль є обов'язковим.")
    elif len(password) < 4:
        errors.append("Пароль має містити щонайменше 4 символи.")

    if not in_game_name:
        errors.append("Ігрове ім'я є обов'язковим.")
    elif has_forbidden_symbols(in_game_name):
        errors.append("Ігрове ім'я містить заборонені символи: ; ' [ ] . , ( )")

    if role not in ALLOWED_ROLES:
        errors.append("Оберіть коректну роль: Lord, Knight або Commonfolk.")


    if role in {"lord", "knight"}:
        if not house:
            errors.append("Для лорда та лицаря необхідно вказати Дім (House).")
        elif has_forbidden_symbols(house):
            errors.append("Назва Дому містить заборонені символи: ; ' [ ] . , ( )")

        if not image_url:
            errors.append("Для лорда та лицаря необхідно вказати посилання на зображення.")
        elif not (image_url.startswith("http://") or image_url.startswith("https://")):
            errors.append("Посилання на зображення має починатися з http:// або https://")

    return errors