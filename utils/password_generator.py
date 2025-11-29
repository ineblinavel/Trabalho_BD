import random
import string

def generate_password(length=6):
    """Gera uma senha aleatória simples."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))
