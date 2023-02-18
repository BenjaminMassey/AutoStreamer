# Auto Streamer

## Overview

Auto Streamer seeks to replace the jobs of lazy, greedy streamers. It provides an automated Twitch streamer that will intelligenty talk to its chat. It is written in Python, and uses tools like ChatGPT and Google Cloud's Speech to Text in order to achieve this.

## Example

[![Auto Streamer Exxample](https://img.youtube.com/vi/Vim87nP5ZAI/0.jpg)](https://www.youtube.com/watch?v=Vim87nP5ZAI)

## Dependencies

Here are the following to "pip install [library_name]":
- livesplit
- git+https://github.com/mmabrouk/chatgpt-wrapper
- datetime
- twitchio
- google-cloud-texttospeech
- playsound
- pyautogui
- pydirectinput

Some important links will be:
- https://codelabs.developers.google.com/codelabs/cloud-text-speech-python3
- https://medium.com/geekculture/using-chatgpt-in-python-eeaed9847e72
- https://github.com/mmabrouk/chatgpt-wrapper
- https://github.com/TwitchIO/TwitchIO
- https://livesplit.org/
- https://github.com/LiveSplit/LiveSplit.Server
- https://code.google.com/archive/p/mupen64-rr/downloads

## Usage

Depending on your settings, you will probably need to be juggling multiple programs, so it is important to make sure you understand what things must be hooked up.

Without Mupen, setup would be as easy as running "run.bat" if on Windows, or simply "main.py" and "twitch.py" concurrently.

With Mupen, one would need to make sure also be running Mupen64-recorder and their LiveSplit with a server running. Mupen must be the primary window focus to function correctly.

## Credits

This was made by Benjamin Massey: benjamin.w.massey@gmail.com