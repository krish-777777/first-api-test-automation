from ai.agents import LoggingAgent, TestDataAgent, CRUDTestAgent

def run_agent_based_tests():
    # Step 1: Start logging
    log_agent = LoggingAgent()

    # Step 2: Generate test data
    test_data_agent = TestDataAgent()
    items = test_data_agent.generate_items(how_many=5)

    # Step 3: Run CRUD sequence
    crud_agent = CRUDTestAgent()
    crud_agent.run_crud_sequence(items)

if __name__ == "__main__":
    run_agent_based_tests()
