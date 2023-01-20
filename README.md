# Wordle CLI Clone

## Getting started

### Pre-requisites:

#### Must have docker installed and running.

Ubuntu: https://docs.docker.com/engine/install/ubuntu/

If you are on mac, install docker desktop: https://docs.docker.com/engine/install/

### How to play:

Enter guesses by typing on the keyboard. Use backspace to edit your entry.

Once you are ready to submit your guess, just hit the return key.

When the game is won or lost, user input will no longer be reflected in the UI.

Once you are done playing, hit the escape key to exit safely.

### Running:

Note: Please make sure your terminal is sized to at least 70x50 before running the application. If the window is too small, the application will throw an exception prompting you to resize the window before trying again.

```
docker build -t wordle-cli .
docker run -it --rm --name wordle-cli-instance wordle-cli
```

### Architecture overview:

This project uses a MVC pattern to clearly separate out the game state from the ui. See more on MVC architecture [here](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller).

To trace through the code, start with `main.py` which should take you to `controller/controller.py` which handles user triggered events (keyboard input) and makes changes accordingly. The model and the view can be understood on their own without any larger context.

All dependencies and assumptions about the environment are captured via the provided `Dockerfile`.

Docstrings and type hints are provided throughout the repo to further clarify things.

### Development

#### Setup for local development:

This step sets up git pre-commit hook that runs the type checker, linter, fixer, and unit tests before allowing a local commit to be made. This is useful for maintaing code quality before anything makes it's way to the remote repo.

```
chmod +x setup.sh
source setup.sh
```

#### Run linter/fixer before merge:

```
docker build -t wordle-cli .
docker run --rm --name wordle-cli-instance wordle-cli black .
```

#### Static type checking before merge:

```
docker build -t wordle-cli .
docker run -it --rm --name wordle-cli-instance wordle-cli mypy .
```

#### Testing before merge:

```
docker build -t wordle-cli .
docker run -it --rm --name wordle-cli-instance wordle-cli pytest
```
