from __future__ import annotations

import re

from constants import COUNTRY_CODES

_STUDENT_ID_RE = re.compile(r"[A-Z0-9][A-Z0-9\-]*")
_NAME_RE = re.compile(r"[A-Za-z' \-]+")
_OCCUPATION_RE = re.compile(r"[A-Za-z0-9 .'\-/]+")
_AREA_CODE_RE = re.compile(r"\d+")
_LOCAL_NUMBER_RE = re.compile(r"\d+")


class Contact:
    """Represent one contact stored by the ASEAN Phonebook."""

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
        """Store all seven contact fields without changing their text."""
        self.student_id = student_id
        self.surname = surname
        self.given_name = given_name
        self.occupation = occupation
        self.country_code = country_code
        self.area_code = area_code
        self.local_number = local_number

    def phone_number(self) -> str:
        """Return the complete phone number as code-area-local."""
        return f"{self.country_code}-{self.area_code}-{self.local_number}"

    def sort_key(self) -> tuple[str, str, str]:
        """Return the surname, given-name, and student-ID sorting key.

        Name comparison must ignore capitalization, but the original stored
        spelling must remain unchanged.
        """
        return (self.surname.lower(), self.given_name.lower(), self.student_id)

    def get_field(self, field: str) -> str:
        """Return the current value of one supported UPDATE field."""
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
        """Return a proposed Contact containing one field change.

        Do not modify the current Contact. The proposed Contact is checked
        first so a failed UPDATE can leave the linked list unchanged.
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
        """Return the exact readable contact format required by the project."""
        country_name = COUNTRY_CODES.get(self.country_code, self.country_code)
        return (
            f"{self.student_id} - {self.surname}, {self.given_name} - "
            f"{self.occupation} - {country_name} - {self.phone_number()}"
        )


def is_valid_student_id(value: str) -> bool:
    """Return True when value follows the published student-ID rules."""
    if not (1 <= len(value) <= 20):
        return False
    return _STUDENT_ID_RE.fullmatch(value) is not None


def is_valid_name(value: str) -> bool:
    """Return True when value is a valid surname or given name."""
    if not (1 <= len(value) <= 40):
        return False
    if value != value.strip():
        return False
    return _NAME_RE.fullmatch(value) is not None


def is_valid_occupation(value: str) -> bool:
    """Return True when value follows the published occupation rules."""
    if not (1 <= len(value) <= 60):
        return False
    if value != value.strip():
        return False
    return _OCCUPATION_RE.fullmatch(value) is not None


def is_valid_area_code(value: str) -> bool:
    """Return True for an area code containing 1 to 6 digits."""
    if not (1 <= len(value) <= 6):
        return False
    return _AREA_CODE_RE.fullmatch(value) is not None


def is_valid_local_number(value: str) -> bool:
    """Return True for a local number containing 3 to 12 digits."""
    if not (3 <= len(value) <= 12):
        return False
    return _LOCAL_NUMBER_RE.fullmatch(value) is not None


def validate_contact(contact: Contact) -> str | None:
    """Return the first required validation error, or None when valid.

    Check fields from left to right using the order published in the project
    definition. COUNTRY_CODE uses ERROR INVALID_COUNTRY <value>.
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
