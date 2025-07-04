"""Factory for Token model."""

import factory

from voltarium.models.token import Token


class TokenFactory(factory.Factory):
    """Factory for creating Token instances."""

    class Meta:
        model = Token

    access_token = factory.Faker("uuid4")
    expires_in = factory.Faker("pyint", min_value=300, max_value=3600)
    token_type = "Bearer"
    scope = factory.Faker("word")
    refresh_expires_in = factory.Faker("pyint", min_value=0, max_value=7200)
    not_before_policy = 0
