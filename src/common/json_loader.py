def read_file_from_json(payload: dict) -> (str, str):
    filename = payload.get("filename")
    payload = payload.get("base64")
    return filename, payload
