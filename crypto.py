from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat

"""
@return   tuple[bytes, bytes]

@brief
Create a RSA keypair using PEM, PKCS8 with no passwords.
Only use this function on first use of the program so that
The keys do not get overwritten.
"""
def create_RSA_keypair() -> tuple[bytes, bytes] :
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

    # Create a public key using the private key
    public_key  =   private_key.public_key()

    # Convert the public into a byte stream
    public_key_bytes    =   public_key.public_bytes(
                                Encoding.PEM,
                                PublicFormat.SubjectPublicKeyInfo
                            )

    return private_key_bytes, public_key_bytes

"""
@params     bytes
@params     bytes

@return     tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]

@brief
Loads the RSA keypair from the database as bytes
Serializes them into proper key formats
Returns the key formats
"""
def load_RSA_from_database(
            private_key_bytes : bytes,
            public_key_bytes : bytes) -> tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:

    private_key     =   serialization.load_pem_private_key(private_key_bytes, None)
    public_key      =   serialization.load_pem_public_key(public_key_bytes)

    return private_key, public_key

"""
@params     bytes
@params     string
@params     rsa.RSAPrivateKey

@return     bool

@brief
Compares the signature with the file, before checking whether the signature matches the file.
Once checked, return whether it is true or false
"""
def verify_school_transcript(signature : bytes, transcript : str, private_key : rsa.RSAPrivateKey):

    # Load the public key
    pad         =   padding.PKCS1v15()
    algo        =   hashes.SHA256()

    # Load the file and signature
    with open(transcript, 'rb+') as data:
        digest  =   data.read()

    # Reconstruct signature
    valid       =   private_key.sign(digest, pad, algo)

    # Verify
    if not signature == valid:
        return False

    return True

# Refactor private, public key
private_key_bytes, public_key_bytes = create_RSA_keypair()
private_key, public_key = load_RSA_from_database(private_key_bytes, public_key_bytes)

# Paste that byte stream into a file
with open("keys/private_key.key", 'wb+') as privkey:
    privkey.write(private_key_bytes)

print("Created private key")

# Paste that byte stream into a file
with open("keys/public_key.pem", 'wb+') as pubkey:
    pubkey.write(public_key_bytes)

print("Created public key")

# Convert "school transcript" into byte stream
with open('data/test_photo.png', 'rb') as exam_result:
    digest  =   exam_result.read()

# Use standard SSL padding format of PKCS1 v1.5
pading     =   padding.PKCS1v15()
hash_algo   =   hashes.SHA256()

# Sign the "school transcript" using private key, and SHA256 hashing algorithm)
signature = private_key.sign(
                digest,
                pading,
                hash_algo
            )

# Sanaty check whether the signing is valid
verify  =   public_key.verify(
                signature,
                digest,
                pading,
                hash_algo
            )

# Right signature to file, or database
with open('signature/test_photo.sig', 'wb+') as sig:
    sig.write(signature)
    print("Successfully written signature file")

signature_file  =   open('signature/test_photo.sig', 'rb+')

verify_signature    =   verify_school_transcript(signature_file.read(), 'data/test_photo.png', private_key)

print("The signature is valid: {0}".format(verify_signature))
