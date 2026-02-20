"""Factories for generating test measurement data.

Values match real CCEE API format:
- identificadorMedicaoConsumo: UC-CODE-YYYYMM-NNN or UUID
- consumption types: AJUSTADO, MEDIDO, ESTIMADO
- measurement status: CONSISTIDA, REJEITADA
- datetime: ISO 8601 with -03:00 (Brasília)
"""

import random
from datetime import date, timedelta

import factory
from faker import Faker

from voltarium.models.measurements import Measurement
from voltarium.models.requests import ListMeasurementsParams
from voltarium.sandbox import UTILITIES

fake = Faker("pt_BR")


def _random_reference_day() -> str:
    """Generate CCEE-valid reference day (YYYY-MM-DD, from Aug 2024 onwards)."""
    start = date(2024, 8, 1)
    end = date(2025, 12, 31)
    delta = (end - start).days
    random_days = random.randint(0, delta)
    d = start + timedelta(days=random_days)
    return d.strftime("%Y-%m-%d")


def _measurement_id(consumer_code: str, ref_day: str) -> str:
    """Generate CCEE-style measurement ID: UC-CODE-YYYYMM-NNN."""
    yyyymm = ref_day[:7].replace("-", "")  # 2024-09 -> 202409
    seq = random.randint(1, 999)
    return f"{consumer_code}-{yyyymm}-{seq:03d}"


class MeasurementFactory(factory.Factory):
    """Factory for generating Measurement instances matching real CCEE API format."""

    class Meta:
        model = Measurement

    consumer_unit_code = factory.LazyFunction(
        lambda: random.choice(["UC-TESTE", "UC123456", "UC789012", f"UC{fake.random_number(digits=6)}"])
    )
    reference_day = factory.LazyFunction(_random_reference_day)
    measurement_consumption_id = factory.LazyAttribute(
        lambda obj: _measurement_id(obj.consumer_unit_code, obj.reference_day)
    )
    utility_agent_code = factory.LazyFunction(lambda: random.choice(UTILITIES).agent_code)
    consumption_reference_date = factory.LazyAttribute(lambda obj: f"{obj.reference_day}T00:00:00-03:00")
    consumption = factory.LazyFunction(lambda: round(random.uniform(100.0, 10000.0), 2))
    consumption_type = factory.LazyFunction(lambda: random.choice(["AJUSTADO", "MEDIDO", "ESTIMADO"]))
    update_date = factory.LazyAttribute(
        lambda obj: f"{obj.reference_day}T{random.randint(8, 18):02d}:{random.randint(0, 59):02d}:00-03:00"
    )
    measurement_status = factory.LazyFunction(lambda: random.choice(["CONSISTIDA", "REJEITADA"]))


class ListMeasurementsParamsFactory(factory.Factory):
    """Factory for generating ListMeasurementsParams instances."""

    class Meta:
        model = ListMeasurementsParams

    consumer_unit_code = factory.LazyFunction(lambda: random.choice(["UC-TESTE", "UC123456"]))
    utility_agent_code = factory.LazyFunction(lambda: str(random.choice(UTILITIES).agent_code))
    start_datetime = factory.LazyFunction(lambda: "2024-09-01T00:00:00-03:00")
    end_datetime = factory.LazyFunction(lambda: "2024-09-30T23:59:59-03:00")
    measurement_status = factory.LazyFunction(lambda: random.choice(["CONSISTIDA", "REJEITADA", None]))
    next_page_index = None
