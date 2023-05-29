from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, Encoding, NoEncryption, PrivateFormat, PublicFormat, pkcs12
import datetime

# Create a RSA private key
private_key     =   rsa.generate_private_key(
                        65537,
                        4096
                    )

# Convert it into a bytes stream
private_key_bytes   =   private_key.private_bytes(
                            Encoding.PEM,
                            PrivateFormat.PKCS8,
                            NoEncryption()
                        )

with open("keys/private_key.pem", "wb+") as priv_key:
    priv_key.write(private_key_bytes)

# Create a public key using the private key
public_key  =   private_key.public_key()

# Convert the public into a byte stream
public_key_bytes    =   public_key.public_bytes(
                            Encoding.PEM,
                            PublicFormat.SubjectPublicKeyInfo
                        )

with open("keys/public_key.pem", "wb+") as pub_key:
    pub_key.write(public_key_bytes)

subject =   issuer = x509.Name([
                          x509.NameAttribute(NameOID.COUNTRY_NAME, u"MY"),
                          x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"WP"),
                          x509.NameAttribute(NameOID.LOCALITY_NAME, u"KL"),
                          x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Educational Institute Corp")
                      ])

cert    =   x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                issuer
            ).public_key(
                public_key
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.datetime.utcnow()
            ).not_valid_after(
                datetime.datetime.utcnow() + datetime.timedelta(days=3560)
            ).add_extension(
                x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
                critical=False,
            ).sign(private_key, hashes.SHA256())

with open("keys/certificate/company.crt", "wb+") as certificate:
    certificate.write(cert.public_bytes(serialization.Encoding.PEM))


# Generate the signature container using PKCS12
p12     =   pkcs12.serialize_key_and_certificates(b"Signature", private_key, cert, None, NoEncryption())

with open("keys/certificate/company.p12", "wb+") as pfx:
    pfx.write(p12)
