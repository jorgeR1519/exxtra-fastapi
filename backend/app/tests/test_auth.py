from app.core.security import create_access_token, decode_access_token, hash_password, verify_password


def test_password_hashing_roundtrip() -> None:
    password = "super-secret-123"
    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password) is True


def test_access_token_roundtrip() -> None:
    token = create_access_token("user-id-1", "admin01", "administrador", "demo@example.com")
    payload = decode_access_token(token)

    assert payload["sub"] == "user-id-1"
    assert payload["usuario"] == "admin01"
    assert payload["tipo"] == "administrador"
    assert payload["email"] == "demo@example.com"
