from __future__ import annotations

import hashlib
import hmac
import os
import posixpath
import secrets
import pyscrypt

SALT_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
DEFAULT_PBKDF2_ITERATIONS = 600_000

_os_alt_seps: list[str] = list(
    sep for sep in [os.sep, os.path.altsep] if sep is not None and sep != "/"
)


def gen_salt(length: int) -> str:
    """Generate a random string of SALT_CHARS with specified ``length``."""
    if length <= 0:
        raise ValueError("Salt length must be at least 1.")
    return "".join(secrets.choice(SALT_CHARS) for _ in range(length))


def _hash_internal(method: str, salt: str, password: str) -> tuple[str, str]:
    method, *args = method.split(":")
    salt_bytes = salt.encode("utf-8")
    password_bytes = password.encode("utf-8")

    if method == "hash":
        if not args:
            n, r, p, dkLen = 2**15, 8, 1, 64
        elif len(args) == 4:
            try:
                n, r, p, dkLen = map(int, args)
            except ValueError:
                raise ValueError("'hash' takes 4 integer arguments.") from None
        else:
            raise ValueError("'hash' takes exactly 4 arguments (n, r, p, dkLen).")

        hash_hex = pyscrypt.hash(
            password=password_bytes,
            salt=salt_bytes,
            N=n,
            r=r,
            p=p,
            dkLen=dkLen
        ).hex()

        return (
            hash_hex,
            f"hash:{n}:{r}:{p}:{dkLen}"
        )

    elif method == "pbkdf2":
        if not args:
            hash_name = "sha256"
            iterations = DEFAULT_PBKDF2_ITERATIONS
        elif len(args) == 1:
            hash_name = args[0]
            iterations = DEFAULT_PBKDF2_ITERATIONS
        elif len(args) == 2:
            hash_name = args[0]
            iterations = int(args[1])
        else:
            raise ValueError("'pbkdf2' takes 0–2 arguments (hash_name[:iterations]).")

        hash_hex = hashlib.pbkdf2_hmac(
            hash_name,
            password_bytes,
            salt_bytes,
            iterations
        ).hex()

        return (
            hash_hex,
            f"pbkdf2:{hash_name}:{iterations}"
        )

    else:
        raise ValueError(f"Invalid hash method '{method}'.")
    

def generate_password_hash(
    password: str, method: str = "hash", salt_length: int = 16
) -> str:
    """Securely hash a password for storage."""
    salt = gen_salt(salt_length)
    hash_hex, actual_method = _hash_internal(method, salt, password)
    return f"{actual_method}${salt}${hash_hex}"


def check_password_hash(pwhash: str, password: str) -> bool:
    """Securely check that a stored password hash matches a plaintext password."""
    try:
        method, salt, hashval = pwhash.split("$", 2)
    except ValueError:
        return False

    try:
        calculated_hash, _ = _hash_internal(method, salt, password)
    except Exception:
        return False

    return hmac.compare_digest(calculated_hash, hashval)


def safe_join(directory: str, *pathnames: str) -> str | None:
    """Safely join untrusted path components to a trusted base directory."""
    if not directory:
        directory = "."

    parts = [directory]

    for filename in pathnames:
        if filename != "":
            filename = posixpath.normpath(filename)

        if (
            any(sep in filename for sep in _os_alt_seps)
            or os.path.isabs(filename)
            or filename == ".."
            or filename.startswith("../")
        ):
            return None

        parts.append(filename)

    return posixpath.join(*parts)