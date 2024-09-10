import paramiko
import os


class SSHClient(paramiko.SSHClient):
    def __init__(self, name: str, password: str | None = None) -> None:
        self.config = paramiko.SSHConfig.from_path(
            os.path.expanduser("~/.ssh/config")
        ).lookup(name)
        super().__init__()

        self.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))

        if self.config.get("identityfile"):
            self.config.update({"key_filename": self.config["identityfile"]})
            self.config.pop("identityfile")

        self.config.update({"username": self.config["user"]})
        self.config.pop("user")
        if password:
            self.config.update({"password": password})

        self.connect(**self.config)  # type: ignore
