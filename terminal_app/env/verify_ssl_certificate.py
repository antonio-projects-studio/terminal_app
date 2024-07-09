import certifi
import requests

from .env import CONFIG_DIR

CERTIFICATES_DIR = CONFIG_DIR / "certificates"


def verify_ssl_certificate(url: str):
    assert CERTIFICATES_DIR.exists(), "The folder must exist"
    assert CERTIFICATES_DIR.is_dir(), "The certificates folder should be a directory"

    for attempt in range(2):
        message: str
        try:
            requests.get(url=url, verify=True)
        except requests.exceptions.SSLError as ex:
            if attempt == 0:

                cert_file = certifi.where()

                for file in CERTIFICATES_DIR.iterdir():
                    if file.is_file():
                        if file.suffix == ".pem":
                            with open(file, "rb") as infile:
                                custom_cert = infile.read()
                            with open(cert_file, "ab") as outfile:
                                outfile.write(custom_cert)
                            print(f"Added the {file.name} to the certificates")

                continue

            print("INFO: the certificates were not installed")

    message = "Certificates found..."
    print(message)
