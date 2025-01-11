import jwt


def encode_jwt(payload, key, algorithm):
    encoded = jwt.encode(payload, key, algorithm=algorithm)
    return encoded


def decode_jwt(token, key, algorithms):
    decoded = jwt.decode(token, key, algorithms=algorithms)
    return decoded

