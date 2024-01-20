import unittest

import pandas as pd
from pandera_sampler import PanderaSampler
from test_schemas import PalmerPenguinsSchema, TestSchema


class TestPanderaSampler(unittest.TestCase):
    def setUp(self):
        self.sampler_penguins = PanderaSampler(schema=PalmerPenguinsSchema)
        self.sampler_test = PanderaSampler(TestSchema)

    def test_sample_penguins(self):
        df = self.sampler_penguins.sample(100)
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] > 0

    def test_sample_test(self):
        df = self.sampler_test.sample(100)
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] > 0
