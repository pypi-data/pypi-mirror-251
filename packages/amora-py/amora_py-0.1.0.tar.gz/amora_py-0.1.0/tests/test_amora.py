#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest
import amora_py
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

def test_amora_zero_new():
	key = bytes([
		0x4f, 0x99, 0x70, 0x66, 0x2f, 0xac, 0xd3, 0x7d,
		0xc3, 0x6c, 0x0f, 0xd1, 0xda, 0xd0, 0x7e, 0xaa,
		0x04, 0x7c, 0x28, 0x54, 0x58, 0x3c, 0x92, 0x0f,
		0x52, 0x4b, 0x2b, 0x01, 0xd8, 0x40, 0x83, 0x1a,
	])
	amora = amora_py.Amora.amora_zero(key)
	payload = "sample_payload_just_for_testing"
	token = amora.encode(payload.encode(), 1)
	decoded = amora.decode(token, True)
	decoded = bytes(decoded).decode()
	assert payload == decoded

def test_amora_zero_from_str():
	key = "4f9970662facd37dc36c0fd1dad07eaa047c2854583c920f524b2b01d840831a"
	amora = amora_py.Amora.amora_zero_from_str(key)
	payload = "sample_payload_just_for_testing"
	token = amora.encode(payload.encode(), 1)
	decoded = amora.decode(token, True)
	decoded = bytes(decoded).decode()
	assert payload == decoded

def test_amora_zero_two_keys():
	key = bytes([
		0x4f, 0x99, 0x70, 0x66, 0x2f, 0xac, 0xd3, 0x7d,
		0xc3, 0x6c, 0x0f, 0xd1, 0xda, 0xd0, 0x7e, 0xaa,
		0x04, 0x7c, 0x28, 0x54, 0x58, 0x3c, 0x92, 0x0f,
		0x52, 0x4b, 0x2b, 0x01, 0xd8, 0x40, 0x83, 0x1a,
	])
	amora = amora_py.Amora.amora_zero(key)
	payload = "sample_payload_just_for_testing"
	token = amora.encode(payload.encode(), 1)
	key = "4f9970662facd37dc36c0fd1dad07eaa047c2854583c920f524b2b01d840831a"
	amora = amora_py.Amora.amora_zero_from_str(key)
	decoded = amora.decode(token, True)
	decoded = bytes(decoded).decode()
	assert payload == decoded

def test_amora_zero_key_invalid_chars():
	key = "ZXCV70662facd37dc36c0fd1dad07eaa047c2854583c920f524b2b01d840831a"
	with pytest.raises(ValueError, match="InvalidKey"):
		amora_py.Amora.amora_zero_from_str(key)

def test_amora_zero_key_too_short():
	key = "4f99"
	with pytest.raises(ValueError, match="InvalidKey"):
		amora_py.Amora.amora_zero_from_str(key)

def test_amora_zero_key_too_long():
	key = "4f9970662facd37dc36c0fd1dad07eaa047c2854583c920f524b2b01d840831a01234"
	with pytest.raises(ValueError, match="InvalidKey"):
		amora_py.Amora.amora_zero_from_str(key)

def test_amora_zero_wrong_encoding():
	key = "4f9970662facd37dc36c0fd1dad07eaa047c2854583c920f524b2b01d840831a"
	amora = amora_py.Amora.amora_zero_from_str(key)
	token = "xGAihaJSerdTCt-zpa0XRS-sY5F4H1SZ5mwRzpWc4rXYMY1NIgz8DpsGTD-JAdqmsIgTo6SRYl4m4"
	with pytest.raises(ValueError, match="WrongEncoding"):
		amora.decode(token, False)

def test_amora_zero_unsupported_version():
	key = "4f9970662facd37dc36c0fd1dad07eaa047c2854583c920f524b2b01d840831a"
	amora = amora_py.Amora.amora_zero_from_str(key)
	token = "oQEAAGgmXpFevpAoQpgcC7AFgwmbHKDTABRGdPQxfsIymRJPN4VWZdALbFb_E3Jd8_xGAi" \
		"haJSerdTCt-zpa0XRS-sY5F4H1SZ5mwRzpWc4rXYMY1NIgz8DpsGTD-JAdqmsIgTo6SRYl4m4"
	with pytest.raises(ValueError, match="UnsupportedVersion"):
		amora.decode(token, False)

def test_amora_one_new():
	x25519 = X25519PrivateKey.generate()
	secret_key = x25519.private_bytes_raw()
	public_key = x25519.public_key().public_bytes_raw()
	amora = amora_py.Amora.amora_one(secret_key, public_key)
	payload = "sample_payload_just_for_testing"
	token = amora.encode(payload.encode(), 1)
	decoded = amora.decode(token, True)
	decoded = bytes(decoded).decode()
	assert payload == decoded

def test_amora_one_from_str():
	secret_key = "778d0b92672b9a25ec4fbe65e3ad2212efa011e8f7035754c1342fe46191dbb3"
	public_key = "5cdd89c1bb6859c927c50b6976712f256cdbf14d7273f723dc121c191f9d6d6d"
	amora = amora_py.Amora.amora_one_from_str(secret_key, public_key)
	payload = "sample_payload_just_for_testing"
	token = amora.encode(payload.encode(), 1)
	decoded = amora.decode(token, True)
	decoded = bytes(decoded).decode()
	assert payload == decoded

def test_amora_one_encode_only():
	public_key = "5cdd89c1bb6859c927c50b6976712f256cdbf14d7273f723dc121c191f9d6d6d"
	amora = amora_py.Amora.amora_one_from_str(None, public_key)
	payload = "sample_payload_just_for_testing"
	token = amora.encode(payload.encode(), 1)
	assert len(token) == 143

def test_amora_one_decode_only():
	secret_key = "778d0b92672b9a25ec4fbe65e3ad2212efa011e8f7035754c1342fe46191dbb3"
	amora = amora_py.Amora.amora_one_from_str(secret_key, None)
	payload = "sample_payload_just_for_testing"
	token = "oQEAAGgmXpFevpAoQpgcC7AFgwmbHKDTABRGdPQxfsIymRJPN4VWZdALbFb_E3Jd8_xGAi" \
		"haJSerdTCt-zpa0XRS-sY5F4H1SZ5mwRzpWc4rXYMY1NIgz8DpsGTD-JAdqmsIgTo6SRYl4m4"
	decoded = amora.decode(token, False)
	decoded = bytes(decoded).decode()
	assert payload == decoded

def test_amora_one_expited_token():
	secret_key = "778d0b92672b9a25ec4fbe65e3ad2212efa011e8f7035754c1342fe46191dbb3"
	amora = amora_py.Amora.amora_one_from_str(secret_key, None)
	payload = "sample_payload_just_for_testing"
	token = "oQEAAGgmXpFevpAoQpgcC7AFgwmbHKDTABRGdPQxfsIymRJPN4VWZdALbFb_E3Jd8_xGAi" \
		"haJSerdTCt-zpa0XRS-sY5F4H1SZ5mwRzpWc4rXYMY1NIgz8DpsGTD-JAdqmsIgTo6SRYl4m4"
	with pytest.raises(ValueError, match="ExpiredToken"):
		amora.decode(token, True)

def test_amora_one_encryption_error():
	secret_key = "778d0b92672b9a25ec4fbe65e3ad2212efa011e8f7035754c1342fe46191dbb3"
	amora = amora_py.Amora.amora_one_from_str(secret_key, None)
	payload = "sample_payload_just_for_testing"
	token = "oQEAAGgmXpFevpAoQpgcC7AFgwmbHKDTABRGdPQxfsIymRJPN4VWZdALbFb_E3Jd8_xGAi" \
		"haJSerdTCt-zpa0XRS-sY5F4H1SZ5mwRzpWc4rXYMY1NIgz8DpsGTD-JAdqmsIgTo6SRYl4m8"
	with pytest.raises(ValueError, match="EncryptionError"):
		amora.decode(token, False)
