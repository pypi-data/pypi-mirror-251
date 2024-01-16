import unittest
import re
import time
from uuid_v9 import uuid, verify_checksum

uuid_regex = {
    'v9': re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-9[0-9a-f]{3}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I),
    'generic': re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
}

class TestUuidV9(unittest.TestCase):
    def test_validate_as_version_9_uuid(self):
        id1 = uuid()
        id2 = uuid('a1b2c3d4')
        id3 = uuid('', False)
        id4 = uuid('a1b2c3d4', False)

        self.assertTrue(uuid_regex['v9'].match(id1))
        self.assertTrue(uuid_regex['generic'].match(id1))
        self.assertTrue(uuid_regex['v9'].match(id2))
        self.assertTrue(uuid_regex['generic'].match(id2))
        self.assertTrue(uuid_regex['v9'].match(id3))
        self.assertTrue(uuid_regex['generic'].match(id3))
        self.assertTrue(uuid_regex['v9'].match(id4))
        self.assertTrue(uuid_regex['generic'].match(id4))

    def test_generate_sequential_ids(self):
        id1 = uuid()
        time.sleep(2)
        id2 = uuid()
        time.sleep(2)
        id3 = uuid()

        self.assertTrue(bool(id1))
        self.assertTrue(bool(id2))
        self.assertTrue(bool(id3))
        self.assertTrue(id1 < id2)
        self.assertTrue(id2 < id3)

    def test_generate_sequential_ids_with_prefix(self):
        id1 = uuid('a1b2c3d4')
        time.sleep(2)
        id2 = uuid('a1b2c3d4')
        time.sleep(2)
        id3 = uuid('a1b2c3d4')

        self.assertTrue(bool(id1))
        self.assertTrue(bool(id2))
        self.assertTrue(bool(id3))
        self.assertTrue(id1 < id2)
        self.assertTrue(id2 < id3)
        self.assertEqual(id1[:8], 'a1b2c3d4')
        self.assertEqual(id2[:8], 'a1b2c3d4')
        self.assertEqual(id3[:8], 'a1b2c3d4')
        self.assertEqual(id1[14:18], id2[14:18])
        self.assertEqual(id2[14:18], id3[14:18])

    def test_generate_non_sequential_ids(self):
        idS = uuid('', False)
        time.sleep(2)
        idNs = uuid('', False)

        self.assertTrue(bool(idS))
        self.assertTrue(bool(idNs))
        self.assertNotEqual(idS[:4], idNs[:4])

    def test_generate_non_sequential_ids_with_prefix(self):
        idS = uuid('a1b2c3d4', False)
        time.sleep(2)
        idNs = uuid('a1b2c3d4', False)

        self.assertTrue(bool(idS))
        self.assertTrue(bool(idNs))
        self.assertEqual(idS[:8], 'a1b2c3d4')
        self.assertEqual(idNs[:8], 'a1b2c3d4')
        self.assertNotEqual(idS[14:18], idNs[14:18])

    def test_generate_ids_without_version(self):
        id = uuid('', True, False)
        self.assertTrue(bool(id))
        self.assertTrue(uuid_regex['generic'].match(id))

    def test_generate_ids_with_checksum(self):
        id = uuid('', True, True, True)
        self.assertTrue(bool(id))
        self.assertTrue(verify_checksum(id))
        self.assertTrue(uuid_regex['v9'].match(id))
        self.assertTrue(uuid_regex['generic'].match(id))

if __name__ == '__main__':
    unittest.main()
