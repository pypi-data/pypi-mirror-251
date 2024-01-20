# UUID v9

The v9 UUID supports both time-based sequential and random non-sequential IDs with an optional prefix, an optional checksum, and sufficient randomness to avoid collisions.

<!-- To learn more about UUID v9, please visit the website: https://uuid-v9.jhunt.dev -->

## Installation

Install UUID v9 from PyPI.

```bash
python3 -m pip install uuid-v9
```

## Usage

```python
from uuid_v9 import uuid, is_uuidv9, is_uuid

ordered_id = uuid()
prefixed_ordered_id = uuid('a1b2c3d4') # up to 8 hexadecimal characters
unordered_id = uuid('', False)
prefixed_unordered_id = uuid('a1b2c3d4', False)
ordered_id_without_version = uuid('', True, False)
ordered_id_with_checksum = uuid('', True, True, True)

const is_valid_v9 = is_uuidv9(ordered_id, true) # UUID v9 validator with checksum
const is_valid = is_uuid(ordered_id_without_version) # generic UUID validator
```

### Command Line

```bash
python3 uuid_v9.py
python3 uuid_v9.py --prefix 'a1b2c3d4'
python3 uuid_v9.py --unordered
python3 uuid_v9.py --noversion
python3 uuid_v9.py --checksum
```

## Compatibility

Some UUID validators will not accept some v9 UUIDs. Three possible workarounds are:

1) Use the built-in validator (recommended)
2) Use compatibility mode*
3) Bypass the validator (not recommended)

*Compatibility mode adds version and variant digits to immitate v1 or v4 UUIDs based on whether or not you have a timestamp.

## Format

Here is the UUID v9 format: `xxxxxxxx-xxxx-9xxx-8xxx-xxxxxxxxxxyy`

x = prefix/timestamp/random, y = checksum (optional), 9 = version (optional), 8 = variant (compatibility mode)

## License

This project is licensed under the [MIT License](LICENSE).