# -*- coding: utf-8 -*-

from typing import Any, Dict, Optional, List

from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import Security, Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.constants import ErrorCodeEnum, ALPHANUM_HOST_REGEX
from app.config import config
from app.core.utils import validator
from app.helpers.crypto import jwt as jwt_helper
from app.core.exceptions import BaseHTTPException


_http_bearer = HTTPBearer(auto_error=False)


def auth_jwt(
    request: Request,
    authorization: Optional[HTTPAuthorizationCredentials] = Security(_http_bearer),
) -> Dict[str, Any]:
    """Dependency function to authenticate the access token (JWT) and get the payload.

    Args:
        request       (Request                     , required): The FastAPI request object.
        authorization (HTTPAuthorizationCredentials, required): 'Authorization: Bearer <access_token>' header credentials.

    Raises:
        BaseHTTPException: If the access token is missing.
        BaseHTTPException: If the access token has expired.
        BaseHTTPException: If the access token is invalid.

    Returns:
        Dict[str, Any]: The decoded access token payload.
    """

    if not authorization:
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.TOKEN_INVALID,
            message="Not authenticated!",
            headers={"WWW-Authenticate": 'Bearer error="missing_token"'},
        )

    _access_token: str = authorization.credentials
    if not validator.is_valid(val=_access_token, pattern=ALPHANUM_HOST_REGEX):
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.TOKEN_INVALID,
            message="Invalid access token!",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    _payload: Dict[str, Any] = None
    try:
        _payload: Dict[str, Any] = jwt_helper.decode(
            token=_access_token,
            key=config.api.security.jwt.secret,
            algorithm=config.api.security.jwt.algorithm,
        )
    except ExpiredSignatureError:
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.TOKEN_EXPIRED,
            message="Access token has expired!",
            headers={"WWW-Authenticate": 'Bearer error="expired_token"'},
        )
    except InvalidTokenError:
        raise BaseHTTPException(
            error_enum=ErrorCodeEnum.TOKEN_INVALID,
            message="Invalid access token!",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
        )

    request.state.user_id = _payload.get("sub")
    return _payload


def get_user_id(payload: Dict[str, Any] = Depends(auth_jwt)) -> str:
    """Dependency function to get the user ID from the token payload.

    Args:
        payload (Dict[str, Any], required): The decoded access token payload.

    Returns:
        str: The user ID.
    """

    _user_id: str = payload.get("sub")
    return _user_id


def is_auth(user_id: str = Depends(get_user_id)) -> bool:
    """Dependency function to check if the user is authenticated.

    Args:
        user_id (str, required): The user ID.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """

    if not user_id:
        return False

    return True


class AuthRoleDep:
    def __init__(self, allow_level: int, allow_owner: bool = False):
        self.allow_level = allow_level
        self.allow_owner = allow_owner

    def __call__(
        self, request: Request, payload: Dict[str, Any] = Depends(auth_jwt)
    ) -> Dict[str, Any]:
        """Dependency function to check the role level of the user.

        Args:
            request (Request       , required): The FastAPI request object.
            payload (Dict[str, Any], required): The decoded access token (JWT) payload.

        Raises:
            BaseHTTPException: If the user has insufficient role privileges.

        Returns:
            Dict[str, Any]: The decoded access token payload.
        """

        if self.allow_owner:
            _auth_user_id: str = payload.get("sub")
            _path_params: List[str] = list(request.path_params.values())
            if _path_params and (_path_params[0] == _auth_user_id):
                return payload

        _token_level: int = payload.get("role_level")
        if self.allow_level < _token_level:
            raise BaseHTTPException(
                error_enum=ErrorCodeEnum.FORBIDDEN,
                message="You do not have enough role privileges!",
                description="The request requires higher role privileges.",
                headers={
                    "WWW-Authenticate": 'Bearer error="insufficient_role", error_description="The request requires higher privileges."'
                },
            )

        return payload


class AuthScopeDep:
    def __init__(self, allow_scope: str, allow_owner: bool = False):
        self.allow_scope = allow_scope
        self.allow_owner = allow_owner

    def __call__(
        self, request: Request, payload: Dict[str, Any] = Depends(auth_jwt)
    ) -> Dict[str, Any]:
        """Dependency function to check the scope permissions of the user.

        Args:
            request (Request       , required): The FastAPI request object.
            payload (Dict[str, Any], required): The decoded access token (JWT) payload.

        Raises:
            BaseHTTPException: If the user has insufficient scope permissions.

        Returns:
            Dict[str, Any]: The decoded access token payload.
        """

        if self.allow_owner:
            _auth_user_id: str = payload.get("sub")
            _path_params: List[str] = list(request.path_params.values())
            if _path_params and (_path_params[0] == _auth_user_id):
                return payload

        _token_all_scope: str = payload.get("scope")
        _token_scope_list: List[str] = _token_all_scope.split(" ")
        if self.allow_scope not in _token_scope_list:
            raise BaseHTTPException(
                error_enum=ErrorCodeEnum.FORBIDDEN,
                message="You do not have enough scope permissions!",
                description="The request requires more scope permissions.",
                headers={
                    "WWW-Authenticate": 'Bearer error="insufficient_scope", error_description="The request requires more scope permissions."'
                },
            )

        return payload


class AuthRoleOrScopeDep:
    def __init__(self, allow_level: int, allow_scope: str, allow_owner: bool = False):
        self.allow_level = allow_level
        self.allow_scope = allow_scope
        self.allow_owner = allow_owner

    def __call__(
        self, request: Request, payload: Dict[str, Any] = Depends(auth_jwt)
    ) -> Dict[str, Any]:
        """Dependency function to check the role level and scope permissions of the user.

        Args:
            request (Request       , required): The FastAPI request object.
            payload (Dict[str, Any], required): The decoded access token (JWT) payload.

        Raises:
            BaseHTTPException: If the user has insufficient role privileges or scope permissions.

        Returns:
            Dict[str, Any]: The decoded access token payload.
        """

        if self.allow_owner:
            _auth_user_id: str = payload.get("sub")
            _path_params: List[str] = list(request.path_params.values())
            if _path_params and (_path_params[0] == _auth_user_id):
                return payload

        _token_level: int = payload.get("role_level")
        _token_all_scope: str = payload.get("scope")
        _token_scope_list: List[str] = _token_all_scope.split(" ")
        if (self.allow_level < _token_level) and (
            self.allow_scope not in _token_scope_list
        ):
            raise BaseHTTPException(
                error_enum=ErrorCodeEnum.FORBIDDEN,
                message="You do not have enough permissions!",
                description="The request requires higher role privileges or more scope permissions.",
                headers={
                    "WWW-Authenticate": 'Bearer error="insufficient_permissions", error_description="The request requires higher role privileges or more scope permissions."'
                },
            )

        return payload


get_superadmin = AuthRoleDep(allow_level=1)
get_admin = AuthRoleDep(allow_level=10)
get_normal_user = AuthRoleDep(allow_level=40)
get_free_user = AuthRoleDep(allow_level=50)


__all__ = [
    "auth_jwt",
    "get_user_id",
    "is_auth",
    "get_superadmin",
    "get_admin",
    "get_normal_user",
    "get_free_user",
    "AuthRoleDep",
    "AuthScopeDep",
    "AuthRoleOrScopeDep",
]
