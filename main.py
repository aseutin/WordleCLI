"""Simple entrypoint into the application. Responsible for kicking off the
controller."""
from controller.wordle_controller import WordleController

if __name__ == "__main__":
    WordleController()
