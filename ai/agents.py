from typing import List, Dict, Any, Optional
from faker import Faker
import random, string, json
from framework.http_client import HttpClient
from framework.logger import get_test_logger
from .gemini_client import GeminiClient

logger = get_test_logger()
fake = Faker()

class LoggingAgent:
    def __init__(self):
        logger.info("LoggingAgent initialized. Logs will be saved to logs/tests.log.")

class TestDataAgent:
    def __init__(self, llm: Optional[GeminiClient] = None):
        self.llm = llm or GeminiClient()

    def _fallback_generate(self, n: int = 3) -> List[Dict[str, Any]]:
        datasets = []
        for _ in range(n):
            name = fake.sentence(nb_words=3).rstrip(".")[:100]
            price = round(random.uniform(1.0, 1000.0), 2)
            desc = fake.text(max_nb_chars=120)
            tags = [fake.word() for _ in range(random.randint(0, 4))] or None
            datasets.append({"name": name, "price": price, "description": desc, "tags": tags})
        # Add a few edge-ish cases
        datasets.append({"name": "x", "price": 1.0, "description": None, "tags": []})
        datasets.append({"name": "A"*100, "price": 99999.99, "description": "Z"*200, "tags": ["edge", "max"]})
        return datasets

    def generate_items(self, how_many: int = 3) -> List[Dict[str, Any]]:
        system = "You are an expert QA test data generator. Produce diverse, valid JSON payloads for creating items."
        user = json.dumps({
            "schema": {
                "name": "string (1..100)",
                "price": "float > 0",
                "description": "string (optional, <= 500)",
                "tags": ["string", "... up to 10"]
            },
            "count": how_many
        })
        data = None
        if self.llm:
            data = self.llm.generate_json(system, user)
        if data and isinstance(data, dict) and "items" in data:
            logger.info("LLM-generated test data received.")
            return data["items"]
        logger.info("Using fallback test data generator.")
        return self._fallback_generate(how_many)


class CRUDTestAgent:
    def __init__(self, client: Optional[HttpClient] = None):
        self.client = client or HttpClient()
        self.created_ids: List[int] = []

    def run_crud_sequence(self, items: List[Dict[str, Any]]) -> None:
        created_ids = []
        # CREATE
        for payload in items:
            r = self.client.post("/items", json=payload)
            assert r.status_code == 200, f"Create failed: {r.text}"
            body = r.json()
            created_ids.append(body["id"])
            # Basic validations
            assert body["name"] == payload["name"]
            assert float(body["price"]) == float(payload["price"])
        logger.info(f"Created: {created_ids}")

        # READ single + list
        for item_id in created_ids:
            r = self.client.get(f"/items/{item_id}")
            assert r.status_code == 200, f"Get {item_id} failed"
            got = r.json()
            assert got["id"] == item_id
        r = self.client.get("/items")
        assert r.status_code == 200
        lst = r.json()
        assert all("id" in i for i in lst)

        # UPDATE first item
        if created_ids:
            first_id = created_ids[0]
            updated = {"name": "Updated Name", "price": 42.42, "description": "Updated desc", "tags": ["updated"]}
            r = self.client.put(f"/items/{first_id}", json=updated)
            assert r.status_code == 200
            got = r.json()
            assert got["name"] == "Updated Name"
            # PATCH same item
            patch = {"name": "Patched Name", "price": 84.84}
            r = self.client.patch(f"/items/{first_id}", json=patch)
            assert r.status_code == 200
            got = r.json()
            assert got["name"] == "Patched Name"

        # DELETE all
        for item_id in created_ids:
            r = self.client.delete(f"/items/{item_id}")
            assert r.status_code == 200
        logger.info("CRUD sequence completed successfully.")


    def create_item(self):
        payloads = TestDataAgent().generate_items(1)
        payload = payloads[0]
        r = self.client.post("/items", json=payload)
        assert r.status_code == 200, f"Create failed: {r.text}"
        body = r.json()
        self.created_ids.append(body["id"])
        logger.info(f"Created item: {body}")
        return body

    def read_item(self):
        assert self.created_ids, "No items created yet."
        item_id = self.created_ids[0]
        r = self.client.get(f"/items/{item_id}")
        assert r.status_code == 200, f"Get {item_id} failed"
        body = r.json()
        logger.info(f"Read item: {body}")
        return body

    def update_item(self):
        assert self.created_ids, "No items created yet."
        item_id = self.created_ids[0]
        updated = {"name": "Updated Name", "price": 42.42, "description": "Updated desc", "tags": ["updated"]}
        r = self.client.put(f"/items/{item_id}", json=updated)
        assert r.status_code == 200, f"Update {item_id} failed"
        body = r.json()
        logger.info(f"Updated item: {body}")
        return body

    def patch_item(self):
        assert self.created_ids, "No items created yet."
        item_id = self.created_ids[0]
        patch = {"name": "Patched Name", "price": 84.84}
        r = self.client.patch(f"/items/{item_id}", json=patch)
        assert r.status_code == 200, f"Patch {item_id} failed"
        body = r.json()
        logger.info(f"Patched item: {body}")
        return body

    def delete_item(self):
        assert self.created_ids, "No items created yet."
        for item_id in self.created_ids:
            r = self.client.delete(f"/items/{item_id}")
            assert r.status_code == 200, f"Delete {item_id} failed"
            logger.info(f"Deleted item {item_id}")
        self.created_ids.clear()
