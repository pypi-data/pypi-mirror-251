import numpy as np
import pandera as pa
from pandera.typing import Series


class PalmerPenguinsSchema(pa.SchemaModel):
    species: Series[str] = pa.Field(isin=["Adelie", "Gentoo", "Chinstrap"])
    island: Series[str] = pa.Field(isin=["Torgersen", "Biscoe", "Dream"])
    bill_length_mm: Series[float] = pa.Field(ge=32.1, le=59.6, nullable=True)
    bill_depth_mm: Series[float] = pa.Field(ge=13.1, le=21.5, nullable=True)
    flipper_length_mm: Series[float] = pa.Field(ge=172, le=231, nullable=True)
    body_mass_g: Series[float] = pa.Field(ge=2700, le=6300, nullable=True)
    sex: Series[str] = pa.Field(isin=["male", "female"], nullable=True)
    year: Series[int] = pa.Field(ge=2007, le=2009)


class TestSchema(pa.SchemaModel):
    date_example: Series[np.datetime64] = pa.Field(ge=np.datetime64("2010-01-01"))
    boolean_example: Series[int] = pa.Field(isin=[0, 1])
    int_example: Series[int] = pa.Field(ge=0)
    int_example_2: Series[int] = pa.Field(isin=[i for i in range(0, 8)])
    int_example_3: Series[int] = pa.Field(ge=1, le=31)
    float_example: Series[float] = pa.Field(ge=0)
