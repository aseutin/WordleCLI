# Wordle CLI Clone

## Getting started

### Pre-requisites:

#### Must have docker installed and running.

Ubuntu: https://docs.docker.com/engine/install/ubuntu/

If you are on mac, install docker desktop: https://docs.docker.com/engine/install/

### Running:

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
