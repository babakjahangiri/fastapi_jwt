from passlib.context import CryptContext


class PasswordContext:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> str:
        """
        Verify a plaintext password against its hashed version.

        :param plain_password: The plaintext password to verify.
        :param hashed_password: The hashed version of the password.
        :return: True if passwords match, False otherwise.
        """

        return PasswordContext.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Hash a plaintext password using the specified cryptographic scheme.

        :param plain_password: The plaintext password.
        :return: The hashed password.
        """
        return PasswordContext.pwd_context.hash(plain_password)

    @staticmethod
    def needs_rehash_password(hashed_password: str) -> bool:
        """
        Check if a hashed password needs to be rehashed.

        :param hashed_password: The hashed password to check.
        :return: True if the password needs rehashing, False otherwise.
        """
        return PasswordContext.pwd_context.needs_update(hashed_password)

    @staticmethod
    def verify_and_update(plain_password: str, hashed_password: str) -> tuple | None:
        """
        Verify a password and, if it's using a deprecated hashing algorithm,
        return a new hash for it.

        :param plain_password: The plaintext password to verify.
        :param hashed_password: The hashed version of the password.
        :return: A tuple of (verification_result, new_hash). If no new hash is
                 needed, new_hash will be None.
        """
        return PasswordContext.pwd_context.verify_and_update(
            plain_password, hashed_password
        )
