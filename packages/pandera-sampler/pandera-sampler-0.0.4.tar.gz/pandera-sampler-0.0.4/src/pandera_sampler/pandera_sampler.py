import numpy as np
import pandas as pd
import pandera as pa


class PanderaSampler:
    schema: pa.SchemaModel
    defaults: dict

    def __init__(self, schema: pa.SchemaModel):
        self.schema = schema
        self.defaults = self.get_defaults()

    def get_defaults(self):
        checks_dict = {}
        annotation_default = self.schema._collect_fields()
        for arg_name, arg_value in annotation_default.items():
            annotation_info, field_info = arg_value
            checks_dict.update({arg_name: {"type": annotation_info.arg, "checks": {}}})
            for check in field_info.checks:
                checks_dict[arg_name]["checks"].update(check._check_kwargs)
        return checks_dict

    def sample(self, size):
        defaults = self.defaults
        rng = np.random.default_rng()
        data = {}
        for arg, value in defaults.items():
            type_ = value["type"]
            checks = value["checks"]

            if issubclass(type_, np.integer) or issubclass(type_, int):
                value = self._sample_ints(rng, checks, size, type_)

            elif issubclass(type_, np.floating) or issubclass(type_, float):
                value = self._sample_floats(rng, checks, size)

            elif issubclass(type_, str):
                value = self._sample_strs(rng, checks, size)

            elif issubclass(type_, np.datetime64):
                value = self._sample_dates(rng, checks, size)

            data.update({arg: value})
        return pd.DataFrame(data)

    def _sample_ints(self, rng, checks, size, type_):
        big_number = 2**10
        min_value = checks["min_value"] if "min_value" in checks else -big_number
        max_value = checks["max_value"] if "max_value" in checks else big_number
        allowed_values = (
            list(checks["allowed_values"]) if "allowed_values" in checks else []
        )
        if "allowed_values" in checks:
            value = rng.choice(allowed_values, size=size)
        else:
            value = rng.integers(
                low=min_value,
                high=max_value,
                size=size,
                dtype=type_,
            )
        return value

    def _sample_floats(self, rng, checks, size):
        big_number = float(2**20)
        min_value = checks["min_value"] if "min_value" in checks else -big_number
        max_value = checks["max_value"] if "max_value" in checks else big_number
        value = rng.uniform(
            low=min_value,
            high=max_value,
            size=size,
        ).astype(type)
        return value

    def _sample_strs(self, rng, checks, size):
        allowed_values = (
            list(checks["allowed_values"]) if "allowed_values" in checks else []
        )
        value = rng.choice(allowed_values, size=size, replace=True)
        return value

    def _sample_dates(self, rng, checks, size):
        min_value = (
            checks["min_value"]
            if "min_value" in checks
            else np.datetime64("1970-01-01")
        )
        max_value = (
            checks["max_value"]
            if "max_value" in checks
            else np.datetime64("2030-01-01")
        )

        days_diff = (max_value - min_value).astype(int) + 1
        random_days = np.random.randint(0, days_diff, size=size)
        random_dates = min_value + random_days.astype("timedelta64[D]")
        random_dates = [np.datetime64(date) for date in random_dates]
        return random_dates
