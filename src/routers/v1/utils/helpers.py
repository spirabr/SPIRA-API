def user_helper(data) -> dict:
    if data == None:
        return None
    return {
        "id": str(data["_id"]),
        "username": data["username"],
        "email": data["email"],
    }
