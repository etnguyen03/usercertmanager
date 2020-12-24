import re
import uuid

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

import base64
from cryptography.hazmat.primitives import serialization
from cryptography import x509


def validate_rsa_cert(value):
    try:
        x509.load_der_x509_certificate(base64.b64decode(value))
    except Exception:
        raise ValidationError(
            "This is not a valid RSA certificate", params={"value": value}
        )


def validate_rsa_key(value):
    try:
        serialization.load_der_private_key(base64.b64decode(value), password=None)
    except Exception:
        raise ValidationError(
            "This is not a valid RSA private key. Ensure it has no password.", params={"value": value}
        )


class KeyPair(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)

    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    modify_time = models.DateTimeField(auto_now=True)

    public_key = models.TextField(
        help_text="RSA public key in ASCII format. Do not include the BEGIN and END CERTIFICATE lines",
        validators=[
            validators.RegexValidator(
                regex=re.compile(
                    "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$",
                    flags=re.MULTILINE,
                ),
                message="This is not a valid key; it contains illegal characters. "
                "Ensure that you have removed the BEGIN and END CERTIFICATE lines.",
            ),
            validate_rsa_cert,
        ],
    )

    private_key = models.TextField(
        help_text="Unencrypted RSA private key in ASCII format. Do not include the BEGIN and END KEY lines",
        validators=[
            validators.RegexValidator(
                regex=re.compile(
                    "^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$",
                    flags=re.MULTILINE,
                ),
                message="This is not a valid key; it contains illegal characters. "
                "Ensure that you have removed the BEGIN and END CERTIFICATE lines.",
            ),
            validate_rsa_key,
        ],
    )

    client = models.ForeignKey(
        "Client",
        on_delete=models.CASCADE,
        help_text="The client that this key pair belongs to.",
    )

    application = models.ForeignKey(
        "Application",
        on_delete=models.CASCADE,
        help_text="The application that this key pair is valid for."
    )

    revoked = models.BooleanField(help_text="Whether this certificate was revoked by this program", default=False)


class Application(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    name = models.CharField(max_length=250, help_text="The name of this application.")

    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    modify_time = models.DateTimeField(auto_now=True)


class Client(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    name = models.CharField(max_length=250, help_text="Name of this client")

    create_time = models.DateTimeField(auto_now_add=True, editable=False)
    modify_time = models.DateTimeField(auto_now=True)
