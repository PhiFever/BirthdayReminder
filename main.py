import os


def get_env(env_name: str) -> str:
    """Get the value of an environment variable."""
    try:
        return os.environ[env_name]
    except KeyError:
        raise ValueError(f"Environment variable {env_name} not found")


if __name__ == "__main__":
    email = get_env("EMAIL")
    pwd = get_env("PWD")
    smtp= get_env("SMTP")
