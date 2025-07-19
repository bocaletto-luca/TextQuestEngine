import pytest
from engine.core.parser import Parser, Action

@pytest.fixture
def parser():
    return Parser()

def test_normalize_removes_punctuation_and_lowercases(parser):
    tokens = parser.normalize("Guarda, l'Oggetto!")
    assert tokens == ["guarda", "l'", "oggetto"]

def test_parse_move_verb(parser):
    action = parser.parse("vai casa", {}, SimpleNamespace(rooms={"casa": None}))
    assert isinstance(action, Action)
    assert action.command == "move"
    assert action.target == "casa"
    assert action.indirect is None

def test_parse_direct_room(parser):
    world = SimpleNamespace(rooms={"casa": None})
    action = parser.parse("casa", {}, world)
    assert action.command == "move"
    assert action.target == "casa"

def test_parse_inventory_command(parser):
    action = parser.parse("inventario", {}, None)
    assert action.command == "inventory"
    assert action.target is None

def test_parse_use_with_indirect(parser):
    action = parser.parse("usa chiave con porta", {}, None)
    assert action.command == "use"
    assert action.target == "chiave"
    assert action.indirect == "porta"

def test_parse_save_slot(parser):
    action = parser.parse("salva slot1", {}, None)
    assert action.command == "save"
    assert action.target == "slot1"

def test_unknown_command_returns_none(parser):
    assert parser.parse("xyz", {}, SimpleNamespace(rooms={})) is None
