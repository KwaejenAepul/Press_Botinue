# Press Botinue
a discord bot for the Press Continue community server

[discord](https://discord.gg/4YzzH9hrZB)

[youtube](https://www.youtube.com/@PressContinue)

## Features
- Simple warning system
- Word filter that deletes banned words and gives a warning
- Event reminder for the discord community's monthly challenge
- Basic mod tools to ban and mass remove messages

## Usage
Install discord.py, dotenv and python-dateutil according to their respective install instructions

Create a `.env` file that contains `TOKEN=your-bot-token` 

To run the both simply open the folder in your terminal and run `python3 main.py`

Initialise the database with`!init_db`.

This will create a database with a table for the warnings of the past 7 days, timeouts of the past 30 days, banned words, and a table for every member that has been warned at least once with total warnings and timeouts the member has had

All configuration is done in `utils/config.py`


# Commands

### You need to have ban member priviledges to use any of these commands

`addword [word]` add one or multiple words to the word filter

`deleteword [word]` delete one or multiple words from the word filter

`listword` list the words in the word filter

`warn [@member] [reason]` warn member if a member had 3 warnings in the last 7 days they will get a timeout

`warnings [@member]` see current warnings and total warnings and timeouts of member

`purge [n]` delete the last n number of messages

`challengeon [true/false]` turn on or off the message reminder

`challengeedit [the challenge]` edit what the current challenge is

 
 
