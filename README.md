Tiny Space has you manage resource shipments to your space colony. It is an abstract strategy city building puzzle game.

On each game 'turn' you will place down the given (you can't choose!) resource to any of the tiles in your colony. Every tile in your colony grid can hold one resource. When the resources in your colony match one of the polyomino shaped 'Building Schematics', you may combine those resources into the respective structure, earning its bonus.

When the entire grid is full, game over! Try to maximise your score.

For now, several controls are only available through keyboard inputs:

* The number `1` enters `Resource Placement` mode, this is the default mode.
* The number `2` enters `Building Schematics` mode. Keep pressing `2` to toggle through each schematic.
* The number `3` when in `Building Schematics` mode will rotate the schematic by 90 degrees.

## Installing dependencies

Install [PyPoetry](https://python-poetry.org/docs/#installation).

Navigate to project directory and run `poetry install`. This creates a virtual environment with the correct version of Python, its dependencies and Tiny Space installed.


## Running the game

First, enter the virtual environment with `poetry shell`.

Then, `./run LOGLEVEL` to run the game.

Loglevel is optional and defaults to INFO. Logs less salient than the current configuration will be ignored. For example, if loglevel is set to WARNING you won't see any DEBUG or INFO logs.

Some possible values of LogLevel:
* DEBUG
* INFO
* WARNING
* ERROR
* CRITICAL
