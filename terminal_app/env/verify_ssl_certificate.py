import certifi
import requests

from pathlib import Path


def verify_ssl_certificate(url: str, certificate_folder: Path):
    assert certificate_folder.exists(), "The folder must exist"
    assert certificate_folder.is_dir(), "The certificates folder should be a directory"

    for attempt in range(2):
        message: str
        try:
            requests.get(url=url, verify=True)
        except requests.exceptions.SSLError as ex:
            if attempt == 0:

                cert_file = certifi.where()

                for file in certificate_folder.iterdir():
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
