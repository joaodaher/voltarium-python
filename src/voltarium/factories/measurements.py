"""Factories for generating test measurement data."""

import random

import factory
from faker import Faker

from voltarium.models.measurements import Measurement
from voltarium.models.requests import ListMeasurementsParams

fake = Faker("pt_BR")


class MeasurementFactory(factory.Factory):
    """Factory for generating Measurement instances."""

    class Meta:
        model = Measurement

    measurement_consumption_id = factory.LazyFunction(lambda: fake.uuid4())
    consumer_unit_code = factory.LazyFunction(lambda: f"UC{fake.random_number(digits=6)}")
    utility_agent_code = factory.LazyFunction(lambda: random.randint(100000, 100009))
    reference_day = factory.LazyFunction(lambda: fake.date_this_year().strftime("%Y-%m-%d"))
    consumption_reference_date = factory.LazyFunction(
        lambda: fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S-03:00")
    )
    consumption = factory.LazyFunction(lambda: round(random.uniform(100.0, 10000.0), 2))
    consumption_type = factory.LazyFunction(lambda: random.choice(["AJUSTADO", "MEDIDO", "ESTIMADO"]))
    update_date = factory.LazyFunction(lambda: fake.date_time_this_year().strftime("%Y-%m-%dT%H:%M:%S-03:00"))
    measurement_status = factory.LazyFunction(lambda: random.choice(["CONSISTIDA", "REJEITADA"]))


class ListMeasurementsParamsFactory(factory.Factory):
    """Factory for generating ListMeasurementsParams instances."""

    class Meta:
        model = ListMeasurementsParams

    consumer_unit_code = factory.LazyFunction(lambda: f"UC{fake.random_number(digits=6)}")
    utility_agent_code = factory.LazyFunction(lambda: str(random.randint(100000, 100009)))
    start_datetime = factory.LazyFunction(lambda: "2024-09-01T00:00:00-03:00")
    end_datetime = factory.LazyFunction(lambda: "2024-09-30T23:59:59-03:00")
    measurement_status = factory.LazyFunction(lambda: random.choice(["CONSISTIDA", "REJEITADA", None]))
    next_page_index = None
