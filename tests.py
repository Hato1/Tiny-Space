import pytest

from buildings import Building
from grid import Grid
from resources import Iron
from tiles import Tile

# Assuming Grid has a method to compare equality that is meaningful for tests
# If not, you might need to implement a utility function for comparing Grid objects


@pytest.mark.parametrize(
    "rotation, expected_id",
    [
        (0, "rotation_0"),
        (1, "rotation_90"),
        (2, "rotation_180"),
        (3, "rotation_270"),
        # Edge cases
        (4, "rotation_full_circle"),
        # (-1, "rotation_negative"),
        # Error cases
        # (None, "rotation_none"),
        # ("a", "rotation_string"),
        # (5, "rotation_out_of_bounds"),
    ],
)
def test_get_schematic(rotation, expected_id):
    rotations = [
        Grid(initial=[[Tile(Iron), Tile(Iron)], [Tile(Iron), Tile()]]),
        Grid(initial=[[Tile(Iron), Tile(Iron)], [Tile(), Tile(Iron)]]),
        Grid(initial=[[Tile(), Tile(Iron)], [Tile(Iron), Tile(Iron)]]),
        Grid(initial=[[Tile(Iron), Tile()], [Tile(Iron), Tile(Iron)]]),
    ]

    class TestBuilding(Building):
        name = "Test building"
        _schematic = rotations[0]

    # expected_grid = Grid()  # This needs to be replaced with the expected Grid object after rotation

    result = TestBuilding.get_schematic(rotation)

    # Assert
    assert isinstance(result, Grid), f"Type is actually {type(result)}"
    assert (
        result == rotations[rotation % 4]
    ), f"Failed for {expected_id}. Expected {rotations[rotation % 4]}. Got {result}"
