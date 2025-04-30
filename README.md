# Python code overview

For this task, I chose to recreate a classic memory game Simon. It is a game where a player must memorize and repeat a growing sequence of colored button presses. The game shows a sequence of colored buttons, and the player must repeat the sequence correctly. With each level, the sequence gets longer by one button press and the challenge increases. My implementation uses Python with Tkinter for the graphical interface.

# Running with Docker

## Prerequisites

X server VcXsrv for GUI display must be installed on your system.

# Building the Docker image

The following code was run in the terminal window of the project directory:

docker build -t simon-game:latest .

docker tag simon-game:latest kristina26/simon-game:latest

docker login

docker push kristina26/simon-game:latest

The Docker image has been pushed to Docker Hub with the tag: kristina26/simon-game:latest

# Running the container

The container can be run from the Docker GUI or by running a command:

docker run -it --rm simon-game:latest

The container includes a startup script that automatically configures the display connection to work with most setups.

# Technical challenges

The biggest challenge was running a GUI application in Docker. To overcome this issue, I configured the container to connect to the host's X server, used host.docker.internal:0.0 to connect to Windows/macOS hosts, and included X11 utilities for compatibility.
Another challenge was audio functionality. The initial idea was to use different sound effects (different .mp3 files) for different colored buttons. This implementation worked when running the application locally but there were issues when the program was run on Docker. Instead, the basic system sound root.bell() was used for audio.

# Dockerfile

The Dockerfile uses a base image python:3.9-slim.

Installs essential dependencies for Tkinter and X11 and copies requirements.txt (although no external Python packages are required).

It creates a startup script for proper display configuration.

Cleans up after package installation to reduce image size.

# Usage

To run the application:

Start an X server on your host system.

Run the Docker container:

docker pull kristina26/simon-game:latest
docker run -it --rm kristina26/simon-game:latest

