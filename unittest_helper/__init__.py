# from typing import Any, TypeGuard
# import unittest
# from unittest.util import safe_repr


# class batterTestCase(unittest.TestCase):

#     def assertIsInstance[T](self: unittest.TestCase, obj: T, cls, msg=None) -> TypeGuard[T]:
#         """Same as self.assertTrue(isinstance(obj, cls)), with a nicer
#             default message."""
#         if not isinstance(obj, cls):
#             standardMsg = '%s is not an instance of %r' % (safe_repr(obj), cls)
#             self.fail(self._formatMessage(msg, standardMsg))
#             return False
#         return True


# class TestAssertIsInstance(unittest.TestCase):
#     def test_assertIsInstance(self, obj: Any):

#         if self.assertIsInstance(obj, int):
#             obj
