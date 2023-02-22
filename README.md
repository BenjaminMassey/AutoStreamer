# Auto Streamer

## Overview

Auto Streamer seeks to replace the jobs of lazy, greedy streamers. It provides an automated Twitch streamer that will intelligenty talk to its chat. It is written in Python, and uses tools like ChatGPT and Google Cloud's Speech to Text in order to achieve this.

## Example

[![Auto Streamer Example](https://img.youtube.com/vi/Vim87nP5ZAI/0.jpg)](https://www.youtube.com/watch?v=Vim87nP5ZAI)

## Installation

Auto Streamer requires recent Python. You can install its dependencies with

```
python3 -m pip install -r requirements.txt
```

There are quite a few odd dependencies, so you may want to run this in some Python virtual environment.

## Usage

Depending on your settings, you will probably need to be juggling multiple programs, so it is important to make sure you understand what things must be hooked up.

Without Mupen, setup would be as easy as running `main.py` and `twitch.py` concurrently. Use `run.bat` for this on Windows; `run.sh` on Linux.

With Mupen, make sure to also be running `Mupen64-recorder` and their `LiveSplit` with a server running. Mupen must be the primary window focus to function correctly.

## References

- https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3
- https://medium.com/geekculture/using-chatgpt-in-python-eeaed9847e72
- https://github.com/mmabrouk/chatgpt-wrapper
- https://github.com/TwitchIO/TwitchIO
- https://livesplit.org/
- https://github.com/LiveSplit/LiveSplit.Server
- https://code.google.com/archive/p/mupen64-rr/downloads
- https://youtu.be/V7DK7NrmMPY
- https://obsproject.com/forum/resources/move-transition.913/

## Credits

This was made by Benjamin Massey: benjamin.w.massey@gmail.com
