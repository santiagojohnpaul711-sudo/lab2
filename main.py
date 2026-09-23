from __future__ import annotations

import sys

from constants import COUNTRY_CODES
from contact import Contact, validate_contact
from phonebook import Phonebook

_MIN_COUNT = 0
_MAX_COUNT = 200

_KNOWN_COMMANDS = {
    "ADD",
    "FIND",
    "FIND_SURNAME",
    "UPDATE",
    "DELETE",
    "LIST",
    "COUNTRY",
}


def is_canonical_count(value: str) -> bool:
    """Return True for 0 or a nonzero decimal without signs/leading zeros."""
    if value == "0":
        return True
    if not value:
        return False
    if value[0] == "0":
        return False
    return value.isdigit()


def _handle_add(phonebook: Phonebook, fields: list[str]) -> str:
    if len(fields) != 8:
        return "ERROR MALFORMED ADD"

    _, student_id, surname, given_name, occupation, country_code, area_code, local_number = fields
    contact = Contact(
        student_id, surname, given_name, occupation, country_code, area_code, local_number
    )
    error = validate_contact(contact)
    if error is not None:
        return error
    return phonebook.add_contact(contact)


def _handle_find(phonebook: Phonebook, fields: list[str]) -> str:
    if len(fields) != 2:
        return "ERROR MALFORMED FIND"
    return phonebook.find_contact(fields[1])


def _handle_find_surname(phonebook: Phonebook, fields: list[str]) -> str:
    if len(fields) != 2:
        return "ERROR MALFORMED FIND_SURNAME"
    return phonebook.find_by_surname(fields[1])


def _handle_update(phonebook: Phonebook, fields: list[str]) -> str:
    if len(fields) != 4:
        return "ERROR MALFORMED UPDATE"
    _, target_student_id, field, new_value = fields
    return phonebook.update_contact(target_student_id, field, new_value)


def _handle_delete(phonebook: Phonebook, fields: list[str]) -> str:
    if len(fields) != 2:
        return "ERROR MALFORMED DELETE"
    return phonebook.delete_contact(fields[1])


def _handle_list(phonebook: Phonebook, fields: list[str]) -> str:
    if len(fields) != 1:
        return "ERROR MALFORMED LIST"
    return phonebook.list_contacts()


def _handle_country(phonebook: Phonebook, fields: list[str]) -> str:
    if len(fields) != 2:
        return "ERROR MALFORMED COUNTRY"

    raw_codes = fields[1]
    codes = raw_codes.split(",")
    if raw_codes == "" or any(code == "" for code in codes):
        return "ERROR INVALID_VALUE COUNTRY_CODES"

    for code in codes:
        if code not in COUNTRY_CODES:
            return f"ERROR INVALID_COUNTRY {code}"

    return phonebook.filter_by_country(set(codes))


_HANDLERS = {
    "ADD": _handle_add,
    "FIND": _handle_find,
    "FIND_SURNAME": _handle_find_surname,
    "UPDATE": _handle_update,
    "DELETE": _handle_delete,
    "LIST": _handle_list,
    "COUNTRY": _handle_country,
}


def process_input_line(phonebook: Phonebook, line: str) -> str:
    """Process one phonebook input line and return its exact output.

    Check field count before field values. The input processor may parse text,
    validate fields, and call Phonebook methods, but it must not relink nodes
    or directly change Phonebook.head.
    """
    if line == "":
        return "ERROR MALFORMED"

    fields = line.split("|")
    command = fields[0]

    if command not in _KNOWN_COMMANDS:
        return f"ERROR UNKNOWN_COMMAND {command}"

    return _HANDLERS[command](phonebook, fields)


def run_program(raw_input: str) -> str:
    """Process one complete ASEAN-PHONEBOOK 1.0 input.

    Validate the version line and input-count line, process exactly the
    requested input lines, and return all produced output joined by newlines.
    """
    lines = raw_input.splitlines()

    if not lines or lines[0] != "ASEAN-PHONEBOOK 1.0":
        return "ERROR VERSION"

    if len(lines) < 2:
        return "ERROR COMMAND_COUNT"

    count_line = lines[1]
    if not is_canonical_count(count_line):
        return "ERROR COMMAND_COUNT"

    count = int(count_line)
    if count < _MIN_COUNT or count > _MAX_COUNT:
        return "ERROR COMMAND_COUNT"

    available_lines = lines[2:]
    if len(available_lines) < count:
        return "ERROR COMMAND_COUNT"

    phonebook = Phonebook()
    outputs: list[str] = []
    for index in range(count):
        outputs.append(process_input_line(phonebook, available_lines[index]))

    return "\n".join(outputs)


def main() -> None:
    """Read standard input, run the phonebook program, and print its output."""
    output = run_program(sys.stdin.read())
    if output:
        print(output)

