import time
from ai.agents import LoggingAgent, TestDataAgent, CRUDTestAgent
from tests.schemas import ItemPayload
from framework.logger import get_test_logger

logger = get_test_logger()

def main():
    # Initialize agents
    LoggingAgent()
    data_agent = TestDataAgent()
    crud_agent = CRUDTestAgent()

    # Generate test data (AI if available, else fallback)
    items = data_agent.generate_items(how_many=3)
    # Validate locally with Pydantic before sending
    valid_items = []
    for i, it in enumerate(items):
        try:
            valid = ItemPayload(**it).model_dump()
            valid_items.append(valid)
        except Exception as e:
            logger.error(f"Item {i} invalid and will be skipped: {e}")

    if not valid_items:
        logger.error("No valid items to test.")
        return

    # Run CRUD
    crud_agent.run_crud_sequence(valid_items)
    logger.info("All tests passed. See logs/tests.log.")

if __name__ == "__main__":
    main()
