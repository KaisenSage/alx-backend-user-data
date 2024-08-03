#!/usr/bin/env python3
import bcrypt

# Task 5: Encrypting passwords
def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# Task 6: Check valid password
def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if the provided password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)

if __name__ == "__main__":
    password = "my_secret_password"
    hashed = hash_password(password)
    print(f"Original password: {password}")
    print(f"Hashed password: {hashed}")

    # Verify the password
    assert is_valid(hashed, password) == True
    assert is_valid(hashed, "wrong_password") == False
    print("Password verification successful!")
I
