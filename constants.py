from typing import Final


COUNTRY_CODES: Final[dict[str, str]] = {
    "60": "Malaysia",
    "62": "Indonesia",
    "63": "Philippines",
    "65": "Singapore",
    "66": "Thailand",
    "84": "Vietnam",
    "95": "Myanmar",
    "670": "Timor-Leste",
    "673": "Brunei Darussalam",
    "855": "Cambodia",
    "856": "Lao PDR",
}

UPDATE_FIELDS: Final[frozenset[str]] = frozenset({
    "ID",
    "SURNAME",
    "GIVEN_NAME",
    "OCCUPATION",
    "COUNTRY_CODE",
    "AREA_CODE",
    "LOCAL_NUMBER",
})
