<h1 align="center">💥BAM!💥</h1>

BAM! is a bomberman-like game written in Python with the use of:
#### [PyGame](https://www.pygame.org)
Used for graphics, sounds and input handling. It is one of the most popular Python libraries for game development.
#### [PodSixNet](https://www.pygame.org/project-PodSixNet-1069-.html)
Used for networking. It makes writing a client-server application much easier without having to worry about sockets and other low-level stuff.

## How to run the game?
In order to start playing the game you have to:
1. Run the `GameServer.exe` on one of the computers
2. Input the host ip (we recommend using hamachi for this) or leave it empty to run the server locally
3. Run `Client.exe` for 3 players and input either host ip, or leave the input empty if server is run locally
4. Have fun!

## Game rules 📜
- Each player starts with the same amount of bombs (3)
- Each player places a bomb in order to destroy crates from which items drop, and to kill other players
- Items dropped from crates include powerups for speed, bomb range, or temporary immunity to explosions
- Each game consists of 3 players
- The map consists of indestructible walls in order to make the game more interesting

## Winning conditions 🎖️
- Each player dies for one round after being hit by an explosion
- Each game consists of rounds. A round ends when there is only one player left on the map
- The game ends when a player wins 5 rounds

## Game flow 🎮
- Players join the server lobby and wait for the game to start
- Each game lasts until one player wins 5 rounds
- Each round starts with players spawning in the corners of the map
- Each player breaks crates in order to get to other players and to get powerups or play however they want
- After each round ends, another one starts if no player has won 5 rounds in total
- After the game ends, players return to the game lobby
