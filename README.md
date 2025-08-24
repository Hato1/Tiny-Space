Tiny Space is an abstract strategy city building puzzle game where you manage resource shipments to your space colony.

As a recently appointed Space Systems Architect, you're in the early stages of setting up your first colony. There's just one problem, due to logistical issues, supply shipments from earth are coming out of order! It's your duty to clear landing space for material shipments, and when possible combine those materials into useful structures & clear space.

On each game 'turn' you will place down the given (you can't choose!) resource to any empty tile in your colony. When the resources in your colony match one of the polyomino shaped 'Building Schematics', you may combine those resources into the respective structure, earning its bonus.

When the entire grid is full, game over! Try to maximise your score.

For now, several controls are only available through keyboard inputs:

* The number `3` when in `Building Schematics` mode will rotate the schematic by 90 degrees.

## How to play

A web version is available at https://hato1.github.io/Tiny-Space/.

Windows EXE: TODO

Mac App: TODO

From source: Install dependencies and run main.py



## Installing dependencies

1. Ensure you have a version of Python as specified in pyproject.toml available.
2. Install [PyPoetry](https://python-poetry.org/docs/#installation).
3. Navigate to project directory and run `poetry install`. This creates a virtual environment with the correct version of Python, its dependencies and Tiny Space installed.
4. Run the game to test everything worked with `poetry run python main.py`


## Development tips

You can activate the poetry environment using `eval $(poetry env activate)` from the project directory.

Please install pre-commit with `pre-commit install` to ensure your commits get auto-formatted and pass the linters.

Log level can be configured by argument. EG: `./main.py LOGLEVEL`

Loglevel defaults to INFO. Logs less salient than the current configuration will be ignored. For example, if loglevel is set to WARNING you won't see any DEBUG or INFO logs.

Some possible values of LogLevel:
* DEBUG (10)
* INFO (20)
* WARNING (30)
* ERROR (40)
* CRITICAL (50)
