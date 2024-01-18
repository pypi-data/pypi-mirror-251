def boolean_validator(field, value, error):
    if value and value not in ["true", "false"]:
        error(field, "Must be a boolean value: true or false")

S_RES_PARTNER_GET = {"_id": {"type": "integer"}}

S_RES_PARTNER_RETURN_GET = {
    "id": {"type": "integer", "required": True},
    "email": {"type": "string", "required": True, "empty": False},
    "name": {"type": "string", "required": True, "empty": False},
    "address": {
        "type": "dict",
        "schema": {
            "street": {"type": "string"},
            "zip": {"type": "string"},
            "city": {"type": "string"},
            "state": {"type": "string"},
            "country": {"type": "string"},
        },
    },
    "lang": {"type": "string"}
}

S_RES_PARTNER_VALIDATE = {"_id": {"type": "integer"}}

S_RES_PARTNER_SEARCH = {
    "vat": {"type": "string", "nullable": True, "empty": True},
    "email": {"type": "string", "nullable": True, "empty": True},
    "phone": {"type": "string", "nullable": True, "empty": True},
    "member": {"type": "string", "check_with": boolean_validator},
    "coop_candidate": {"type": "string", "check_with": boolean_validator},
}

S_RES_PARTNER_RETURN_SEARCH = {
    "count": {"type": "integer"},
    "rows": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {"type": "integer", "required": True},
                "email": {"type": "string", "required": True, "empty": False},
                "name": {"type": "string", "required": True, "empty": False},
                "address": {
                    "type": "dict",
                    "schema": {
                        "street": {"type": "string"},
                        "zip": {"type": "string"},
                        "city": {"type": "string"},
                        "state": {"type": "string"},
                        "country": {"type": "string"},
                    },
                },
                "lang": {"type": "string"}
            }
        }
    }
}
