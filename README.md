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

### Development

#### Setup for local development:  # sets up git hook

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
