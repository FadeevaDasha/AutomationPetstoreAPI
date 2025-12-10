NOTES_SCHEMA = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "status": {"type": "integer"},
        "message": {
            "type": "string",
            "enum": ["Successful Request", "Note successfully created"]
        },
        "data": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "title": {"type": "string"},
                "description": {"type": "string"},
                "completed": {"type": "boolean"},
                "created_at": {"type": "string"},
                "updated_at": {"type": "string"},
                "category": {"type": "string"},
                "user_id": {"type": "string"}
            },
            "required": ["id", "title", "description", "completed", "created_at", "updated_at", "category", "user_id"],
            "additionalProperties": False
        }
    },
    "required": ["success", "status", "message", "data"],
    "additionalProperties": False
}