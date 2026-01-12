from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get all environment variables
print("Environment variables loaded from .env file:")
print("-" * 50)

# List all keys (this will show ALL environment variables, including system ones)
# To see only .env file keys, we need to track what was added
env_before = set(os.environ.keys())

# Reload to see what was added
from dotenv import dotenv_values

# This loads only from .env file (not system environment)
env_vars = dotenv_values('.env')

print("\nKeys from .env file:")
print("-" * 50)
for key in env_vars.keys():
    print(f"- {key}")

print(f"\nTotal keys in .env file: {len(env_vars)}")

# Optionally show values (be careful with sensitive data!)
print("\n" + "=" * 50)
print("Keys with values (use with caution!):")
print("=" * 50)
for key, value in env_vars.items():
    # Mask sensitive values
    if any(sensitive in key.upper() for sensitive in ['KEY', 'SECRET', 'PASSWORD', 'TOKEN']):
        masked_value = value[:4] + '*' * (len(value) - 4) if len(value) > 4 else '****'
        print(f"{key} = {masked_value}")
    else:
        print(f"{key} = {value}")
