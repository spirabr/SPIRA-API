from fastapi import Request


def get_header_bearer_token(req: Request) -> str:
    headers = req.headers["Authorization"].split(" ")
    if headers[0] != "Bearer":
        raise
    return headers[1]
