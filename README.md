# Battleship Python project for Remotr python class
Developed by David Jones in 2016 as a project, tried having fun while early in my learning. 


# [pyp-c2-a1] Battleship game

Build a battleship game. It has to work in the console. You don’t need any external libraries, you can make it work just using plain python. You’d play against the console. The game will have 2 play modes: attack and defence.

### Defend mode

In this mode you place the ships and receive attacks from the computer; you’ll have to inform if the attack was successful or not.

When the game starts the computer will give you information about the grid (10x10) and tell you what ships you have available. For example:

1 submarine (size 3)
1 Aircraft (size 5)
2 Patrol boats (size 2)
Then you’ll be able to position them in the grid, indicating the first position and if they should be placed horizontally or vertically. Example:

```
Place the submarine on C3 vertically
Place the aircraft on A9 horizontally
```

At this point the computer must do some checks; namely:

* If the ship fits; it’s not out of bounds. For example, placing an Aircraft on the position H9 horizontally would make it go out of bounds
* If two ships collide. For example. Placing the submarine on C3 vertically and the aircraft on B1 horizontally.

After the setup is done (ship positioning) you’ll start receiving random attacks from the computer; 1 at a time. After the computer attacks it’ll ask for an answer from you (either miss, hit or sunk). You’ll inform the computer (seeing the grid on screen). If you cheat, the computer should know.

Of course the computer would never fire two shots at the same position; and would realize when it sunk all the ships.

Extra: Once the computer identifies it has hit a ship the attacks could stop being random and focus on sinking that particular ship it hit.

### Attack mode

In this mode the computer position the ships and you’ll have to sink all of them. The computer will position the ships randomly. After it’s done it’ll start asking for your shots. Once you fire your shot it’ll inform you if you missed, hit or sunk a ship. Once all the ships are sunk the game finishes and it’ll provide statistics about it.
