# -*- coding: utf-8 -*-

import os
import errno
from typing import Tuple

import aiofiles
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import (
    PrivateKeyTypes,
    PublicKeyTypes,
)
from pydantic import validate_call
from beans_logging import logger

from api.core.constants import WarnEnum
from api.core import utils


@validate_call
async def async_create_keys(
    rsa_keys_dir: str,
    key_size: int,
    private_key_fname: str,
    public_key_fname: str,
    warn_mode: WarnEnum = WarnEnum.DEBUG,
) -> None:
    """Async create RSA keys and save them to files.

    Args:
        rsa_keys_dir      (str     , required): RSA keys directory.
        key_size          (int     , required): RSA key size.
        private_key_fname (str     , required): RSA private key filename.
        public_key_fname  (str     , required): RSA public key filename.
        warn_mode         (WarnEnum, optional): Warning mode. Defaults to WarnEnum.DEBUG.

    Raises:
        OSError: If failed to create RSA keys.
    """

    _private_key_path = os.path.join(rsa_keys_dir, private_key_fname)
    _public_key_path = os.path.join(rsa_keys_dir, public_key_fname)
    if await aiofiles.os.path.isfile(
        _private_key_path
    ) and await aiofiles.os.path.isfile(_public_key_path):
        return

    _private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    _public_key = _private_key.public_key()

    _private_pem = _private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    _public_pem = _public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    await utils.async_create_dir(create_dir=rsa_keys_dir, warn_mode=warn_mode)

    if not await aiofiles.os.path.isfile(_private_key_path):
        try:
            async with aiofiles.open(_private_key_path, "wb") as _private_key_file:
                await _private_key_file.write(_private_pem)

        except OSError as err:
            if (err.errno == errno.EEXIST) and (warn_mode == WarnEnum.DEBUG):
                logger.debug(f"'{_private_key_path}' private key already exists!")
            else:
                logger.error(f"Failed to create '{_private_key_path}' private key!")
                raise

    if not await aiofiles.os.path.isfile(_public_key_path):
        try:
            async with aiofiles.open(_public_key_path, "wb") as _public_key_file:
                await _public_key_file.write(_public_pem)

        except OSError as err:
            if (err.errno == errno.EEXIST) and (warn_mode == WarnEnum.DEBUG):
                logger.debug(f"'{_public_key_path}' public key already exists!")
            else:
                logger.error(f"Failed to create '{_public_key_path}' public key!")
                raise

    return


@validate_call
async def async_get_private_key(private_key_path: str) -> PrivateKeyTypes:
    """Async read RSA private key from file.

    Args:
        private_key_path (str, required): RSA private key path.

    Raises:
        FileNotFoundError: If RSA private key file not found.

    Returns:
        PrivateKeyTypes: RSA private key.
    """

    if not await aiofiles.os.path.isfile(private_key_path):
        raise FileNotFoundError(f"Not found '{private_key_path}' private key!")

    _private_key: PrivateKeyTypes = None
    async with aiofiles.open(private_key_path, "rb") as _private_key_file:
        _private_key_bytes: bytes = await _private_key_file.read()
        _private_key: PrivateKeyTypes = serialization.load_pem_private_key(
            _private_key_bytes, password=None, backend=default_backend()
        )

    return _private_key


@validate_call
async def async_get_public_key(public_key_path: str) -> PublicKeyTypes:
    """Async read RSA public key from file.

    Args:
        public_key_path (str, required): RSA public key path.

    Raises:
        FileNotFoundError: If RSA public key file not found.

    Returns:
        PublicKeyTypes: RSA public key.
    """

    if not await aiofiles.os.path.isfile(public_key_path):
        raise FileNotFoundError(f"Not found '{public_key_path}' public key!")

    _public_key: PublicKeyTypes = None
    async with aiofiles.open(public_key_path, "rb") as _public_key_file:
        _public_key_bytes: bytes = await _public_key_file.read()
        _public_key: PublicKeyTypes = serialization.load_pem_public_key(
            _public_key_bytes, backend=default_backend()
        )

    return _public_key


@validate_call
async def async_get_keys(
    private_key_path: str, public_key_path: str
) -> Tuple[PrivateKeyTypes, PublicKeyTypes]:
    """Async read RSA keys from file.

    Args:
        private_key_path (str, required): RSA private key path.
        public_key_path  (str, required): RSA public key path.

    Returns:
        Tuple[PrivateKeyTypes, PublicKeyTypes]: Private and public keys.
    """

    _private_key = await async_get_private_key(private_key_path=private_key_path)
    _public_key = await async_get_public_key(public_key_path=public_key_path)

    return _private_key, _public_key


@validate_call
def create_keys(
    rsa_keys_dir: str,
    key_size: int,
    private_key_fname: str,
    public_key_fname: str,
    warn_mode: WarnEnum = WarnEnum.DEBUG,
) -> None:
    """Create RSA keys and save them to files.

    Args:
        rsa_keys_dir      (str     , required): RSA keys directory.
        key_size          (int     , required): RSA key size.
        private_key_fname (str     , required): RSA private key filename.
        public_key_fname  (str     , required): RSA public key filename.
        warn_mode         (WarnEnum, optional): Warning mode. Defaults to WarnEnum.DEBUG.

    Raises:
        OSError: If failed to create RSA keys.
    """

    _private_key_path = os.path.join(rsa_keys_dir, private_key_fname)
    _public_key_path = os.path.join(rsa_keys_dir, public_key_fname)
    if os.path.isfile(_private_key_path) and os.path.isfile(_public_key_path):
        return

    _private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend(),
    )
    _public_key = _private_key.public_key()

    _private_pem = _private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    _public_pem = _public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    utils.create_dir(create_dir=rsa_keys_dir, warn_mode=warn_mode)

    if not os.path.isfile(_private_key_path):
        try:
            with open(_private_key_path, "wb") as _private_key_file:
                _private_key_file.write(_private_pem)

        except OSError as err:
            if (err.errno == errno.EEXIST) and (warn_mode == WarnEnum.DEBUG):
                logger.debug(f"'{_private_key_path}' private key already exists!")
            else:
                logger.error(f"Failed to create '{_private_key_path}' private key!")
                raise

    if not os.path.isfile(_public_key_path):
        try:
            with open(_public_key_path, "wb") as _public_key_file:
                _public_key_file.write(_public_pem)

        except OSError as err:
            if (err.errno == errno.EEXIST) and (warn_mode == WarnEnum.DEBUG):
                logger.debug(f"'{_public_key_path}' public key already exists!")
            else:
                logger.error(f"Failed to create '{_public_key_path}' public key!")
                raise

    return


@validate_call
def get_private_key(private_key_path: str) -> PrivateKeyTypes:
    """Read RSA private key from file.

    Args:
        private_key_path (str, required): RSA private key path.

    Raises:
        FileNotFoundError: If RSA private key file not found.

    Returns:
        PrivateKeyTypes: RSA private key.
    """

    if not os.path.isfile(private_key_path):
        raise FileNotFoundError(f"Not found '{private_key_path}' private key!")

    _private_key: PrivateKeyTypes = None
    with open(private_key_path, "rb") as _private_key_file:
        _private_key_bytes: bytes = _private_key_file.read()
        _private_key: PrivateKeyTypes = serialization.load_pem_private_key(
            _private_key_bytes, password=None, backend=default_backend()
        )

    return _private_key


@validate_call
def get_public_key(public_key_path: str) -> PublicKeyTypes:
    """Read RSA public key from file.

    Args:
        public_key_path (str, required): RSA public key path.

    Raises:
        FileNotFoundError: If RSA public key file not found.

    Returns:
        PublicKeyTypes: RSA public key.
    """

    if not os.path.isfile(public_key_path):
        raise FileNotFoundError(f"Not found '{public_key_path}' public key!")

    _public_key: PublicKeyTypes = None
    with open(public_key_path, "rb") as _public_key_file:
        _public_key_bytes: bytes = _public_key_file.read()
        _public_key: PublicKeyTypes = serialization.load_pem_public_key(
            _public_key_bytes, backend=default_backend()
        )

    return _public_key


@validate_call
def get_keys(
    private_key_path: str, public_key_path: str
) -> Tuple[PrivateKeyTypes, PublicKeyTypes]:
    """Read RSA keys from file.

    Args:
        private_key_path (str, required): RSA private key path.
        public_key_path  (str, required): RSA public key path.

    Returns:
        Tuple[PrivateKeyTypes, PublicKeyTypes]: Private and public keys.
    """

    _private_key = get_private_key(private_key_path=private_key_path)
    _public_key = get_public_key(public_key_path=public_key_path)

    return _private_key, _public_key


__all__ = [
    "async_create_keys",
    "async_get_private_key",
    "async_get_public_key",
    "async_get_keys",
    "create_keys",
    "get_private_key",
    "get_public_key",
    "get_keys",
]
