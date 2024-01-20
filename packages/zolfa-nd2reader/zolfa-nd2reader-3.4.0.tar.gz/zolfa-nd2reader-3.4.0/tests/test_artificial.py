import unittest
from os import path
import struct

from zolfa.nd2reader.artificial import ArtificialND2
from zolfa.nd2reader.common import get_version, parse_version, parse_date, _add_to_metadata, _parse_unsigned_char, \
    _parse_unsigned_int, _parse_unsigned_long, _parse_double, check_or_make_dir
from zolfa.nd2reader.exceptions import InvalidVersionError


class TestArtificial(unittest.TestCase):
    def setUp(self):
        dir_path = path.dirname(path.realpath(__file__))
        check_or_make_dir(path.join(dir_path, 'test_data/'))
        self.test_file = path.join(dir_path, 'test_data/test.nd2')
        self.create_test_nd2()

    def create_test_nd2(self):
        with ArtificialND2(self.test_file) as artificial:
            self.assertIsNotNone(artificial.file_handle)
            artificial.close()
