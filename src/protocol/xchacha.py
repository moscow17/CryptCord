import ctypes
import ctypes.util

library_path = ctypes.util.find_library("sodium") or ctypes.util.find_library("libsodium")
sodium = ctypes.cdll.LoadLibrary(library_path)

if not sodium._name:
    raise RuntimeError("Unable to locate libsodium")

CRYPTO_AEAD_XHCACHA20POLY1305_IETF_KEYBYTES = sodium.crypto_aead_xchacha20poly1305_ietf_keybytes()
CRYPTO_AEAD_XHCACHA20POLY1305_IETF_NPUBBYTES = sodium.crypto_aead_xchacha20poly1305_ietf_npubbytes()
CRYPTO_AEAD_XHCACHA20POLY1305_IETF_ABYTES = sodium.crypto_aead_xchacha20poly1305_ietf_abytes()

def crypto_aead_xchacha20poly1305_ietf_encrypt(message, ad, nonce, key):
    if len(nonce) is not CRYPTO_AEAD_XHCACHA20POLY1305_IETF_NPUBBYTES:
        raise ValueError("Invalid nonce")

    if len(key) is not CRYPTO_AEAD_XHCACHA20POLY1305_IETF_KEYBYTES:
        raise ValueError("Invalid key")

    message_len = ctypes.c_ulonglong(len(message))

    if ad is None:
        ad_len = ctypes.c_ulonglong(0)
    else:
        ad_len = ctypes.c_ulonglong(len(ad))

    ciphertext = ctypes.create_string_buffer(
        message_len.value + CRYPTO_AEAD_XHCACHA20POLY1305_IETF_ABYTES
    )
    ciphertext_len = ctypes.c_ulonglong(0)

    retval = sodium.crypto_aead_xchacha20poly1305_ietf_encrypt(
        ciphertext, ctypes.byref(ciphertext_len),
        message, message_len,
        ad, ad_len,
        None, nonce, key
    )

    if retval != 0:
        raise RuntimeError("Encrypting token failed")

    return ciphertext.raw

def crypto_aead_xchacha20poly1305_ietf_decrypt(ciphertext, ad, nonce, key):

    if len(nonce) != CRYPTO_AEAD_XHCACHA20POLY1305_IETF_NPUBBYTES:
        raise ValueError("Invalid nonce")

    if len(key) != CRYPTO_AEAD_XHCACHA20POLY1305_IETF_KEYBYTES:
        raise ValueError("Invalid key")

    decrypted = ctypes.create_string_buffer(
        len(ciphertext) - CRYPTO_AEAD_XHCACHA20POLY1305_IETF_ABYTES
    )
    decrypted_len = ctypes.c_ulonglong(0)
    ciphertext_len = ctypes.c_ulonglong(len(ciphertext))

    if ad is None:
        ad_len = ctypes.c_ulonglong(0)
    else:
        ad_len = ctypes.c_ulonglong(len(ad))

    retval = sodium.crypto_aead_xchacha20poly1305_ietf_decrypt(
        decrypted, ctypes.byref(decrypted_len),
        None,
        ciphertext, ciphertext_len,
        ad, ad_len,
        nonce, key
    )

    if retval != 0:
        raise RuntimeError("Decrypting token failed")

    return decrypted.raw

def generate_nonce():
    buffer = ctypes.create_string_buffer(CRYPTO_AEAD_XHCACHA20POLY1305_IETF_NPUBBYTES)
    sodium.randombytes(buffer, ctypes.c_ulonglong(CRYPTO_AEAD_XHCACHA20POLY1305_IETF_NPUBBYTES))
    return buffer.raw
