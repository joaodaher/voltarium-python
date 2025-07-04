import random
import unittest

from voltarium.client import VoltariumClient
from voltarium.models.constants import API_BASE_URL_STAGING
from voltarium.sandbox import CONCESSIONARIAS, VAREJISTAS


class SandboxTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.varejista = random.choice(VAREJISTAS)
        self.concessionaria = random.choice(CONCESSIONARIAS)

        self.agent_id = self.varejista.agent_code
        self.profile_id = random.choice(self.varejista.profiles)
        self.concessionaria_id = self.concessionaria.agent_code

        self.client = VoltariumClient(
            base_url=API_BASE_URL_STAGING,
            client_id=self.varejista.client_id,
            client_secret=self.varejista.client_secret,
        )
