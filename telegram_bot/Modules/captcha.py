import random
import string

def generate_captcha(length=6):
    """
    Generate a random alphanumeric CAPTCHA string.

    Parameters:
    - length: Length of the CAPTCHA string (default 6).

    Returns:
    - A random string of uppercase letters and digits.
    """
    characters = string.ascii_uppercase + string.digits
    captcha = ''.join(random.choice(characters) for _ in range(length))
    return captcha

# Example usage
if __name__ == "__main__":
    print("Generated CAPTCHA:", generate_captcha())
