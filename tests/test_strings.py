import unittest
import six

from construct import String, PascalString, CString, UBInt16, GreedyString


class TestString(unittest.TestCase):
    def test_parse(self):
        s = String("foo", 5)
        self.assertEqual(s.parse(b"hello"), b"hello")

    def test_parse_utf8(self):
        s = String("foo", 12, encoding="utf8")
        self.assertEqual(s.parse(b"hello joh\xd4\x83n"), six.u("hello joh\u0503n"))

    def test_parse_padded(self):
        s = String("foo", 10, padchar=b"X", paddir="right")
        self.assertEqual(s.parse(b"helloXXXXX"), b"hello")

    def test_parse_padded_left(self):
        s = String("foo", 10, padchar=b"X", paddir="left")
        self.assertEqual(s.parse(b"XXXXXhello"), b"hello")

    def test_parse_padded_center(self):
        s = String("foo", 10, padchar=b"X", paddir="center")
        self.assertEqual(s.parse(b"XXhelloXXX"), b"hello")

    def test_build(self):
        s = String("foo", 5)
        self.assertEqual(s.build(b"hello"), b"hello")

    def test_build_utf8(self):
        s = String("foo", 12, encoding="utf8")
        self.assertEqual(s.build(six.u("hello joh\u0503n")), b"hello joh\xd4\x83n")

    def test_build_padded(self):
        s = String("foo", 10, padchar="X", paddir="right", encoding="utf8")
        self.assertEqual(s.build(six.u("hello")), b"helloXXXXX")

    def test_build_padded_left(self):
        s = String("foo", 10, padchar="X", paddir="left", encoding="utf8")
        self.assertEqual(s.build(six.u("hello")), b"XXXXXhello")

    def test_build_padded_center(self):
        s = String("foo", 10, padchar="X", paddir="center", encoding="utf8")
        self.assertEqual(s.build(six.u("hello")), b"XXhelloXXX")


class TestPascalString(unittest.TestCase):
    def test_parse(self):
        s = PascalString("foo", encoding="utf8")
        self.assertEqual(s.parse(b"\x05hello"), six.u("hello"))

    def test_build(self):
        s = PascalString("foo", encoding="utf8")
        self.assertEqual(s.build(six.u("hello world")), b"\x0bhello world")

    def test_parse_custom_length_field(self):
        s = PascalString("foo", length_field=UBInt16("length"), encoding="utf8")
        self.assertEqual(s.parse(b"\x00\x05hello"), six.u("hello"))

    def test_build_custom_length_field(self):
        s = PascalString("foo", length_field=UBInt16("length"), encoding="utf8")
        self.assertEqual(s.build(six.u("hello")), b"\x00\x05hello")


class TestCString(unittest.TestCase):
    def test_parse(self):
        s = CString("foo", encoding="utf8")
        self.assertEqual(s.parse(b"hello\x00"), six.u("hello"))

    def test_build(self):
        s = CString("foo", encoding="utf8")
        self.assertEqual(s.build(six.u("hello")), b"hello\x00")

    def test_parse_terminator(self):
        s = CString("foo", terminators=b"XYZ", encoding="utf8")
        self.assertEqual(s.parse(b"helloX"), six.u("hello"))
        self.assertEqual(s.parse(b"helloY"), six.u("hello"))
        self.assertEqual(s.parse(b"helloZ"), six.u("hello"))

    def test_build_terminator(self):
        s = CString("foo", terminators=b"XYZ", encoding="utf8")
        self.assertEqual(s.build(six.u("hello")), b"helloX")


class TestGreedyString(unittest.TestCase):
    def test_parse(self):
        s = GreedyString("foo", encoding="utf8")
        self.assertEqual(s.parse(b"hello\x00"), six.u("hello\x00"))

    def test_build(self):
        s = GreedyString("foo", encoding="utf8")
        self.assertEqual(s.build(six.u("hello")), b"hello")

