def get_api_key():
    with open("api_key.key", "r") as f:
        return f.readline().strip()
