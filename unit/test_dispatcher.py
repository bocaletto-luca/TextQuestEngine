import pytest
from types import SimpleNamespace
from engine.core.dispatcher import EventDispatcher

@pytest.fixture
def dispatcher():
    return EventDispatcher()

@pytest.fixture
def dummy_world():
    # Due stanze collegate est<->ovest e un oggetto "chiave"
    room_a = SimpleNamespace(id="a", name="Room A", description="A", 
                              coords=[0,0],
                              connections={"est": "b"},
                              items=["chiave"])
    room_b = SimpleNamespace(id="b", name="Room B", description="B", 
                              coords=[1,0],
                              connections={"ovest": "a"},
                              items=[])
    items = {"chiave": SimpleNamespace(names=["chiave"], description="Una chiave")}
    return SimpleNamespace(rooms={"a": room_a, "b": room_b}, items=items)

@pytest.fixture
def state():
    return {"current_room": "a", "inventory": [], "time": 0, "variables": {}, "missions": {}}

def test_handle_move_by_direction(dispatcher, state, dummy_world):
    result = dispatcher.dispatch(SimpleNamespace(command="move", target="est"), state, dummy_world)
    assert state["current_room"] == "b"
    assert "arrivato in Room B" in result

def test_handle_move_invalid(dispatcher, state, dummy_world):
    result = dispatcher.dispatch(SimpleNamespace(command="move", target="nord"), state, dummy_world)
    assert result == "Non puoi andare lì."
    assert state["current_room"] == "a"

def test_handle_look_room(dispatcher, state, dummy_world):
    # look senza target restituisce descrizione stanza
    result = dispatcher.dispatch(SimpleNamespace(command="look", target=None), state, dummy_world)
    assert "Room A" in result and "A" in result

def test_handle_look_object(dispatcher, state, dummy_world):
    result = dispatcher.dispatch(SimpleNamespace(command="look", target="chiave"), state, dummy_world)
    assert result == "Una chiave"

def test_handle_inventory_empty(dispatcher, state, dummy_world):
    result = dispatcher.dispatch(SimpleNamespace(command="inventory", target=None), state, dummy_world)
    assert result == "L'inventario è vuoto."

def test_handle_take_and_drop(dispatcher, state, dummy_world):
    # prendi la chiave
    res1 = dispatcher.dispatch(SimpleNamespace(command="take", target="chiave"), state, dummy_world)
    assert "Hai raccolto chiave" in res1
    assert "chiave" in state["inventory"]
    assert "chiave" not in dummy_world.rooms["a"].items

    # lascia la chiave
    res2 = dispatcher.dispatch(SimpleNamespace(command="drop", target="chiave"), state, dummy_world)
    assert "Hai lasciato chiave" in res2
    assert "chiave" not in state["inventory"]
    assert "chiave" in dummy_world.rooms["a"].items
