# Simple example on how to create a way to chat about custom data

## Tools
* [Anaconda](https://www.anaconda.com/)

## How to run it
1. Copy the .env-sample to .env and fill in all variables
1. Create python environment ```conda create -n ${PWD##*/} python=3.10```
1. Check that the chromedriver_py version in the "requirements.txt" file is the same as your Chrome browser version. If not, update the version inside the requirements.txt file.
1. Install dependencies ```pip install -r requirements```
1. Run example ```python main.py```