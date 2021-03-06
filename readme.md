# Rock Paper Scissors 101

This code downloads all the data from Rock Paper Scissors with 101 different symbols by David C. Lovelace by webscrapping, from [this url](https://www.umop.com/rps101/1.htm) and then crawls until it reaches 101.

It generates a JSON: `result.json` which contains all the data easy to use, and stores the pictures corresponding to the symbols in a folder called `images` with their respective file names, including gifs.

The JSON is organized like that:
```json
{
    "DYNAMITE": { // the symbol
        "id": 1, // its ID
        "imagefile": "symbols/1.png", // the location of the image of the symbol
        // what it can beat
        "TORNADO": "outclasses TORNADO",
        "QUICKSAND": "clears QUICKSAND",
        "PIT": "creates PIT"
        ...
    }
    ...
}
```

There is a simple python script called `example.py` that shows a way to use this JSON file, in a very simple example.

## The game
I coded a game to learn to play Rock Paper Scissors, that helps to learn and memorize all of the different symbols.
It is far from perfection, but it works, kinda.

The game is located in the file `learn.py` and uses a file called `gameData.json` to store the data, if you want to save it and use it anywhere. It is already created if you run the game for the first time, and delete it if you want to reset your game.

Here is a screenshot of the game running in Powershell:

![img](screenshot.png)