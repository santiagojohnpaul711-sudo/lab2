from __future__ import annotations

import sys

from constants import COUNTRY_CODES
from contact import Contact, validate_contact
from phonebook import Phonebook

# Minimum ug maximum number sa commands nga gitugotan sa system
_MIN_COUNT = 0
_MAX_COUNT = 200

# Set sa mga valid o gisuportahang commands
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
    """I-return ang True para sa 0 o sa number nga walay leading zeros and signs."""
    if value == "0":
        return True
    if not value:
        return False
    if value[0] == "0":
        return False
    return value.isdigit()


def _handle_add(phonebook: Phonebook, fields: list[str]) -> str:
    # dapat sakto nga 8 ka fields ang ipasa para sa ADD command
    if len(fields) != 8:
        return "ERROR MALFORMED ADD"

    _, student_id, surname, given_name, occupation, country_code, area_code, local_number = fields
    contact = Contact(
        student_id, surname, given_name, occupation, country_code, area_code, local_number
    )
    # I-validate una ang contact before i-add sa phonebook
    error = validate_contact(contact)
    if error is not None:
        return error
    return phonebook.add_contact(contact)


def _handle_find(phonebook: Phonebook, fields: list[str]) -> str:
    # Kailangan 2 ka fields ra: FIND ug ang Student ID
    if len(fields) != 2:
        return "ERROR MALFORMED FIND"
    return phonebook.find_contact(fields[1])


def _handle_find_surname(phonebook: Phonebook, fields: list[str]) -> str:
    # Kailanga 2 ka fields ra: FIND_SURNAME ug ang Surname
    if len(fields) != 2:
        return "ERROR MALFORMED FIND_SURNAME"
    return phonebook.find_by_surname(fields[1])


def _handle_update(phonebook: Phonebook, fields: list[str]) -> str:
    # Kailanga 4 ka fields: UPDATE, Student ID, Field Name, ug New Value
    if len(fields) != 4:
        return "ERROR MALFORMED UPDATE"
    _, target_student_id, field, new_value = fields
    return phonebook.update_contact(target_student_id, field, new_value)


def _handle_delete(phonebook: Phonebook, fields: list[str]) -> str:
    # Kailanga 2 ka fields ra: DELETE ug ang Student ID
    if len(fields) != 2:
        return "ERROR MALFORMED DELETE"
    return phonebook.delete_contact(fields[1])


def _handle_list(phonebook: Phonebook, fields: list[str]) -> str:
    # Kailanga 1 ka field ra gyud: ang word nga "LIST"
    if len(fields) != 1:
        return "ERROR MALFORMED LIST"
    return phonebook.list_contacts()


def _handle_country(phonebook: Phonebook, fields: list[str]) -> str:
    # Kailanga 2 ka fields: COUNTRY ug ang comma-separated country codes
    if len(fields) != 2:
        return "ERROR MALFORMED COUNTRY"

    raw_codes = fields[1]
    codes = raw_codes.split(",")
    # Check kong naa ba'y empty code o blangko sa gi-input
    if raw_codes == "" or any(code == "" for code in codes):
        return "ERROR INVALID_VALUE COUNTRY_CODES"

    # I-check kong valid ba ang matag country code nga naa sa COUNTRY_CODES dictionary
    for code in codes:
        if code not in COUNTRY_CODES:
            return f"ERROR INVALID_COUNTRY {code}"

    return phonebook.filter_by_country(set(codes))


# Dictionary dispatch pattern para i-map ang command name padulong sa handler function
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
    """I-process ang usa ka line sa input ug i-return ang sakto nga output string.

    I-check una ang number sa fields bago ang mga values. Dili pwede nga
    i-modify sa input processor ang linked list nodes o ang Phonebook.head directly.
    """
    if line == "":
        return "ERROR MALFORMED"

    fields = line.split("|")
    command = fields[0]

    # I-check kong naa ba sa system ang gi-input nga command
    if command not in _KNOWN_COMMANDS:
        return f"ERROR UNKNOWN_COMMAND {command}"

    return _HANDLERS[command](phonebook, fields)


def run_program(raw_input: str) -> str:
    """I-process ang tibuok input text sa ASEAN-PHONEBOOK 1.0.

    I-validate ang header line ug command count line, i-execute ang kung
    sakto ang kadaghang sa commands, ug i-return ang tanang outputs.
    """
    lines = raw_input.splitlines()

    # Check kong sakto ba ang header o version line
    if not lines or lines[0] != "ASEAN-PHONEBOOK 1.0":
        return "ERROR VERSION"

    # Check kong naa ba'y second line para sa command count
    if len(lines) < 2:
        return "ERROR COMMAND_COUNT"

    count_line = lines[1]
    # Check kong maayo ba ang format sa command count number
    if not is_canonical_count(count_line):
        return "ERROR COMMAND_COUNT"

    count = int(count_line)
    # Check kong naa ba sa range (0 hangtod 200) ang command count
    if count < _MIN_COUNT or count > _MAX_COUNT:
        return "ERROR COMMAND_COUNT"

    available_lines = lines[2:]
    # Check kong sakto ba ang gidaghanon sa lines kumpara sa gipangayo nga count
    if len(available_lines) < count:
        return "ERROR COMMAND_COUNT"

    phonebook = Phonebook()
    outputs: list[str] = []
    # I-loop ug i-process ang matag command line
    for index in range(count):
        outputs.append(process_input_line(phonebook, available_lines[index]))

    return "\n".join(outputs)


def main() -> None:
    """I-read ang standard input (stdin), i-run ang program, ug i-print ang output."""
    output = run_program(sys.stdin.read())
    if output:
        print(output)


if __name__ == "__main__":
    main()
