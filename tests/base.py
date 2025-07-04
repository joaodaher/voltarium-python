import random
import unittest

from voltarium.client import VoltariumClient
from voltarium.models.constants import API_BASE_URL_STAGING
from voltarium.sandbox import RETAILERS, UTILITIES


class SandboxTestCase(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.retailer = random.choice(RETAILERS)
        self.utility = random.choice(UTILITIES)

        self.agent_id = self.retailer.agent_code
        self.profile_id = random.choice(self.retailer.profiles)
        self.utility_id = self.utility.agent_code

        self.client = VoltariumClient(
            base_url=API_BASE_URL_STAGING,
            client_id=self.retailer.client_id,
            client_secret=self.retailer.client_secret,
        )
