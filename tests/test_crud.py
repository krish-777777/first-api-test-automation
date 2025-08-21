import pytest
from ai.agents import TestDataAgent, CRUDTestAgent

test_data_agent = TestDataAgent()
crud_agent = CRUDTestAgent()

def test_generate_data():
    test_data_agent.generate_items()

def test_create_item():
    crud_agent.create_item()

def test_read_item():
    crud_agent.read_item()

def test_update_item():
    crud_agent.update_item()

def test_patch_item():
    crud_agent.patch_item()

def test_delete_item():
    crud_agent.delete_item()
