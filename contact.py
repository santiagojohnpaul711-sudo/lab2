from __future__ import annotations

import re

from constants import COUNTRY_CODES

# Mga Regular na Expression(Regex) para sa pag validate sa atong mga Field
_STUDENT_ID_RE = re.compile(r"[A-Z0-9][A-Z0-9\-]*")
_NAME_RE = re.compile(r"[A-Za-z' \-]+")
_OCCUPATION_RE = re.compile(r"[A-Za-z0-9 .'\-/]+")
_AREA_CODE_RE = re.compile(r"\d+")
_LOCAL_NUMBER_RE = re.compile(r"\d+")


class Contact:
    """It represents sa usa ka contact nga makita sa ASEAN Phonebook."""

    def __init__(
        self,
        student_id: str,
        surname: str,
        given_name: str,
        occupation: str,
        country_code: str,
        area_code: str,
        local_number: str,
    ) -> None:
        """I-save ang 7 ka field sa contact nga dili i change ang original text."""
        self.student_id = student_id
        self.surname = surname
        self.given_name = given_name
        self.occupation = occupation
        self.country_code = country_code
        self.area_code = area_code
        self.local_number = local_number

    def phone_number(self) -> str:
        """I-return ang complite numbers sa telephone nga naka format nga country-area-local."""
        return f"{self.country_code}-{self.area_code}-{self.local_number}"

    def sort_key(self) -> tuple[str, str, str]:
        """I-return ang container sa surname, given name, ug student ID para sa pag-alphabetize. Naka-lowercase ang mga ngalan para sa comparison aron dili mausab ang original nga data.
        """
        return (self.surname.lower(), self.given_name.lower(), self.student_id)

    def get_field(self, field: str) -> str:
        """I-return ang bag-ong value sa gi-update nga field."""
        field_map = {
            "ID": self.student_id,
            "SURNAME": self.surname,
            "GIVEN_NAME": self.given_name,
            "OCCUPATION": self.occupation,
            "COUNTRY_CODE": self.country_code,
            "AREA_CODE": self.area_code,
            "LOCAL_NUMBER": self.local_number,
        }
        return field_map[field]

    def copy_with_update(self, field: str, new_value: str) -> Contact:
        """Mag-make ug mag-return og new instance sa Contact nga gi-update ang usa ka field. Dili i-modify ang existing Contact aron safe ang linked list kon mag-fail ang validation.
        """
        values = {
            "student_id": self.student_id,
            "surname": self.surname,
            "given_name": self.given_name,
            "occupation": self.occupation,
            "country_code": self.country_code,
            "area_code": self.area_code,
            "local_number": self.local_number,
        }
        field_to_kwarg = {
            "ID": "student_id",
            "SURNAME": "surname",
            "GIVEN_NAME": "given_name",
            "OCCUPATION": "occupation",
            "COUNTRY_CODE": "country_code",
            "AREA_CODE": "area_code",
            "LOCAL_NUMBER": "local_number",
        }
        values[field_to_kwarg[field]] = new_value
        return Contact(**values)

    def __str__(self) -> str:
        """I-return ang gikinahanglan nga format sa contact para sa output sa project."""
        country_name = COUNTRY_CODES.get(self.country_code, self.country_code)
        return (
            f"{self.student_id} - {self.surname}, {self.given_name} - "
            f"{self.occupation} - {country_name} - {self.phone_number()}"
        )


def is_valid_student_id(value: str) -> bool:
    """I-return ang True kong valid ang student ID format ug length."""
    if not (1 <= len(value) <= 20):
        return False
    return _STUDENT_ID_RE.fullmatch(value) is not None


def is_valid_name(value: str) -> bool:
    """I-return ang True kong ang value sakto nga surname o given name format."""
    if not (1 <= len(value) <= 40):
        return False
    if value != value.strip():
        return False
    return _NAME_RE.fullmatch(value) is not None


def is_valid_occupation(value: str) -> bool:
    """I-return ang True kong ang value nagsunod sa rules para sa occupation."""
    if not (1 <= len(value) <= 60):
        return False
    if value != value.strip():
        return False
    return _OCCUPATION_RE.fullmatch(value) is not None


def is_valid_area_code(value: str) -> bool:
    """I-return ang True kong ang area code naay sa 1 hangtod 6 ka digits."""
    if not (1 <= len(value) <= 6):
        return False
    return _AREA_CODE_RE.fullmatch(value) is not None


def is_valid_local_number(value: str) -> bool:
    """"I-return ang True kong ang local number naay sa 3 hangtod 12 ka digits."""""
    if not (3 <= len(value) <= 12):
        return False
    return _LOCAL_NUMBER_RE.fullmatch(value) is not None


def validate_contact(contact: Contact) -> str | None:
    """I-return ang unang validation error message, o None kong valid ang tanang field.
    I-check ang mga field gikan sa wala padulong sa tuo sumala sa order sa project specs.
    Ang COUNTRY_CODE mogamit sa format nga ERROR INVALID_COUNTRY <value>.
    """
    if not is_valid_student_id(contact.student_id):
        return "ERROR INVALID_VALUE STUDENT_ID"
    if not is_valid_name(contact.surname):
        return "ERROR INVALID_VALUE SURNAME"
    if not is_valid_name(contact.given_name):
        return "ERROR INVALID_VALUE GIVEN_NAME"
    if not is_valid_occupation(contact.occupation):
        return "ERROR INVALID_VALUE OCCUPATION"
    if contact.country_code not in COUNTRY_CODES:
        return f"ERROR INVALID_COUNTRY {contact.country_code}"
    if not is_valid_area_code(contact.area_code):
        return "ERROR INVALID_VALUE AREA_CODE"
    if not is_valid_local_number(contact.local_number):
        return "ERROR INVALID_VALUE LOCAL_NUMBER"
    return None
