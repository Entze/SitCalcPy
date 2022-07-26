
# noinspection DuplicatedCode
import unittest

from scpy.causal_setting.causal_setting import CausalSetting
from scpy.function import Function


class TestConstructor(unittest.TestCase):

    def test_create_simple(self):
        t = CausalSetting()

