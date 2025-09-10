"""Factories for contract-related models."""

import random
from datetime import datetime, timedelta
from typing import Any

import factory
from factory.fuzzy import FuzzyChoice
from faker import Faker

from voltarium.models import CreateContractRequest
from voltarium.sandbox import RETAILERS, UTILITIES


class CreateContractRequestFactory(factory.Factory):  # type: ignore
    """Factory for CreateContractRequest using sandbox data."""

    class Meta:
        model = CreateContractRequest

    class Params:
        sandbox_retailer = FuzzyChoice(RETAILERS)  # type: ignore
        sandbox_utility = FuzzyChoice(UTILITIES)  # type: ignore

    @factory.lazy_attribute  # type: ignore
    def retailer_agent_code(obj: Any) -> int:
        return obj.sandbox_retailer.agent_code

    @factory.lazy_attribute  # type: ignore
    def retailer_profile_code(obj: Any) -> int:
        return random.choice(obj.sandbox_retailer.profiles)

    @factory.lazy_attribute  # type: ignore
    def utility_agent_code(obj: Any) -> int:
        return obj.sandbox_utility.agent_code

    consumer_unit_code = factory.Faker("numerify", text="########")
    document_type = FuzzyChoice(["CPF"])  # type: ignore

    @factory.lazy_attribute  # type: ignore
    def document_number(obj: Any) -> str:
        f = Faker("pt_BR")
        return "".join(filter(str.isdigit, f.cpf()))

    @factory.lazy_attribute  # type: ignore
    def reference_month(obj: Any) -> str:
        future_date = datetime.now() + timedelta(days=random.randint(30, 90))
        return future_date.strftime("%Y-%m")

    @factory.lazy_attribute  # type: ignore
    def start_date(obj: Any) -> str:
        future_date = datetime.now() + timedelta(days=random.randint(1, 30))
        return future_date.strftime("%Y-%m-%d")

    end_date = None
    comment = factory.Faker("text", max_nb_chars=120)

    # Required business fields (minimal stub content for sandbox acceptance)
    corporate_name = factory.Faker("company")
    consumer_unit_name = factory.Faker("company")

    @factory.lazy_attribute
    def representantes_legais(obj: Any) -> list[dict]:
        f = Faker("pt_BR")
        f_en = Faker("en_US")
        # Generate ASCII-only contact name without special chars per API rule
        raw_name = f_en.name()
        cleaned_name = "".join(ch for ch in raw_name if ("A" <= ch <= "Z") or ("a" <= ch <= "z") or ch == " ")
        cleaned_name = " ".join(cleaned_name.split())  # collapse multiple spaces
        return [
            {
                "nomeContato": cleaned_name,
                "nomeEmail": f.email(),
                "numeroDocumento": "".join(filter(str.isdigit, f.cpf())),
                "tipoContato": "UNIDADE_CONSUMIDORA",
                "tipoDocumento": "CPF",
            }
        ]

    consumer_unit_address = factory.Faker("address")

    @factory.lazy_attribute
    def consumer_unit_phone(obj: Any) -> str:
        ddd = random.randint(11, 99)
        numero = random.randint(100000000, 999999999)  # 9 digits
        return f"({ddd:02d}) {numero // 10000:05d}-{numero % 10000:04d}"

    # For CPF requests, branch fields must not be provided
    branch_consumer_unit_cnpj = None
    branch_consumer_unit_address = None
