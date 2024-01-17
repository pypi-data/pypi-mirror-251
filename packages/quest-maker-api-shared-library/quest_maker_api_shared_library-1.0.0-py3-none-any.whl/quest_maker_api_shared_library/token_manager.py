from datetime import datetime, timedelta
from typing import Any, Optional

import jwt
from bson import ObjectId


class TokenManager:
    def __init__(self,
                 key: str,
                 jwt_expiration_time_in_minutes: int,
                 algorithm: str = "HS256") -> None:
        self.key = key
        self.jwt_expiration_time_in_minutes = jwt_expiration_time_in_minutes
        self.algorithm = algorithm

    def encode_token(
            self,
            identifier: Any,
            scope="create modify:own view:own") -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=self.jwt_expiration_time_in_minutes),
            "iat": datetime.utcnow(),
            "scope": scope,
            "sub": identifier
        }
        return jwt.encode(payload=payload, key=self.key, algorithm=self.algorithm)

    def decode_token(
            self,
            token: str) -> Optional[Any]:
        try:
            print(f"Decoding token: {token}")
            print(f"Using key: {self.key}")
            payload = jwt.decode(
                jwt=token, key=self.key, algorithms=[self.algorithm])
            if payload:
                return payload
            raise ValueError(
                "Scope for the token is invalid."
            )
        except jwt.ExpiredSignatureError:
            raise ValueError(
                "Signature expired. Please re-authenticate.")
        except jwt.InvalidTokenError:
            raise ValueError(
                "Invalid token. Please log in again.")
