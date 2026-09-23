from __future__ import annotations

from constants import UPDATE_FIELDS
from contact import Contact, validate_contact


class Node:
    """Nag-hold og isa ka Contact object ug reference pointer sa next node."""

    def __init__(self, contact: Contact, next_node: Node | None = None) -> None:
        """I-initialize ang isa ka singly linked list node."""
        self.contact = contact
        self.next = next_node


class Phonebook:
    """Ang tig-manage sa mga contacts gamit ang manual nga singly linked list."""

    def __init__(self) -> None:
        """Ang mag-create og empty phonebook asa ang head = None ug ang size = 0."""
        self.head: Node | None = None
        self.size: int = 0

    def _find_node_by_id(self, student_id: str) -> Node | None:
        """I-return ang node nga nag-contain sa student_id, o None kong wala makita."""
        current = self.head
        while current is not None:
            if current.contact.student_id == student_id:
                return current
            current = current.next
        return None

    def _student_id_exists(
        self,
        student_id: str,
        excluded_student_id: str | None = None,
    ) -> bool:
        """I-return ang True kong naa na'y laing contact nga nag-gamit sa student_id.

        Ang excluded_student_id gigamit sa UPDATE para dili mo-trigger and duplicate error 
        kong ang contact mag-keep ra sa iyang own current ID.
        """
        current = self.head
        while current is not None:
            if (
                current.contact.student_id == student_id
                and current.contact.student_id != excluded_student_id
            ):
                return True
            current = current.next
        return False

    def _phone_exists(
        self,
        phone_number: str,
        excluded_student_id: str | None = None,
    ) -> bool:
        """I-return ang True kong naa na'y laing contact nga nag-gamit sa phone_number."""
        current = self.head
        while current is not None:
            if (
                current.contact.phone_number() == phone_number
                and current.contact.student_id != excluded_student_id
            ):
                return True
            current = current.next
        return False

    def _insert_node_sorted(self, node: Node) -> None:
        """I-insert ang node sa sakto nga position para naka-alphabetical order ang list.

        I-handle ang empty list, insertion sa sugod (before head), sa tunga (middle),
        ug sa last (tail). I-update ang size og kaisa lang. Dili mogamit og sort() o sorted().
        """
        key = node.contact.sort_key()

        # Kong empty ang list o mas una ang key kaysa sa current head
        if self.head is None or key < self.head.contact.sort_key():
            node.next = self.head
            self.head = node
            self.size += 1
            return

        # Pag-traverse sa list para makita ang sakto nga insertion point
        previous = self.head
        current = self.head.next
        while current is not None and current.contact.sort_key() < key:
            previous = current
            current = current.next

        node.next = current
        previous.next = node
        self.size += 1

    def _detach_node(self, student_id: str) -> Node | None:
        """I-unlink ug i-return ang usa ka node, o i-return ang None kon wala makita.

        I-handle ang pag-remove kon usa ra ang node, kon head, middle, o tail.
        I-decrement/update ang size og kausa lang kon ma-remove ang node.
        """
        previous: Node | None = None
        current = self.head
        while current is not None:
            if current.contact.student_id == student_id:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                current.next = None
                self.size -= 1
                return current
            previous = current
            current = current.next
        return None

    def add_contact(self, contact: Contact) -> str:
        """I-add ang isa ka validated Contact ug i-return ang result status string.

        I-check isa ang duplicate student ID bago ang duplicate phone number.
        """
        if self._student_id_exists(contact.student_id):
            return f"ERROR DUPLICATE_ID {contact.student_id}"
        if self._phone_exists(contact.phone_number()):
            return f"ERROR DUPLICATE_PHONE {contact.phone_number()}"

        self._insert_node_sorted(Node(contact))
        return f"OK ADD {contact.student_id}"

    def find_contact(self, student_id: str) -> str:
        """I-return ang FOUND o ERROR NOT_FOUND response para sa gipangita nga student_id."""
        node = self._find_node_by_id(student_id)
        if node is None:
            return f"ERROR NOT_FOUND {student_id}"
        return f"FOUND | {node.contact}"

    def find_by_surname(self, surname: str) -> str:
        """I-return ang MATCHES ug CONTACT lines sumala sa order sa linked list."""
        target = surname.lower()
        lines: list[str] = []
        current = self.head
        while current is not None:
            if current.contact.surname.lower() == target:
                lines.append(f"CONTACT | {current.contact}")
            current = current.next

        result = [f"MATCHES {len(lines)}"]
        result.extend(lines)
        return "\n".join(result)

    def update_contact(
        self,
        target_student_id: str,
        field: str,
        new_value: str,
    ) -> str:
        """I-validate ug i-apply ang update sa usa ka contact.

        Kon mag-fail ang update, kinahanglang magpabilin nga intact ug walay kausaban
        ang original Contact ug linked list. Kon ang ID, SURNAME, o GIVEN_NAME ang nausab,
        kinahanglang i-detach ug i-reinsert ang node para magpabilin nga sorted.
        """
        node = self._find_node_by_id(target_student_id)
        if node is None:
            return f"ERROR NOT_FOUND {target_student_id}"

        if field not in UPDATE_FIELDS:
            return f"ERROR INVALID_FIELD {field}"

        old_value = node.contact.get_field(field)
        candidate = node.contact.copy_with_update(field, new_value)

        # I-validate ang candidate contact
        error = validate_contact(candidate)
        if error is not None:
            return error

        # Check kong duplicate ba ang bag-ong ID
        if field == "ID" and self._student_id_exists(
            candidate.student_id, excluded_student_id=target_student_id
        ):
            return f"ERROR DUPLICATE_ID {candidate.student_id}"

        # Check kong duplicate ba ang bag-ong phone number
        if self._phone_exists(
            candidate.phone_number(), excluded_student_id=target_student_id
        ):
            return f"ERROR DUPLICATE_PHONE {candidate.phone_number()}"

        # Kong nausab ang sorting fields, kinahanglan i-reinsert para magpabilin nga sorted
        reinsert_needed = field in ("ID", "SURNAME", "GIVEN_NAME")

        if reinsert_needed:
            detached = self._detach_node(target_student_id)
            detached.contact = candidate
            self._insert_node_sorted(detached)
        else:
            node.contact = candidate

        return f"OK UPDATE {field} | {old_value} -> {new_value}"

    def delete_contact(self, student_id: str) -> str:
        """I-delete ang isa ka contact ug i-return ang result message."""
        detached = self._detach_node(student_id)
        if detached is None:
            return f"ERROR NOT_FOUND {student_id}"
        return f"OK DELETE {student_id}"

    def list_contacts(self) -> str:
        """I-return ang LIST header kauban ang tanang CONTACT lines sumala sa ilang list order."""
        lines: list[str] = []
        current = self.head
        while current is not None:
            lines.append(f"CONTACT | {current.contact}")
            current = current.next

        result = [f"LIST {self.size}"]
        result.extend(lines)
        return "\n".join(result)

    def filter_by_country(self, country_codes: set[str]) -> str:
        """I-return ang COUNTRY_MATCHES kauban ang matching CONTACT lines."""
        lines: list[str] = []
        current = self.head
        
        while current is not None:
            if current.contact.country_code in country_codes:
                lines.append(f"CONTACT | {current.contact}")
            current = current.next

        result = [f"COUNTRY_MATCHES {len(lines)}"]
        result.extend(lines)
        return "\n".join(result)
