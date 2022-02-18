# vim-metroidvania

Contribution to Game jam for metroid:
https://itch.io/jam/metroidvania-month-15

# Idea

Metroid style game, using only keyboard and graphics will be rendered text like in a terminal(but in reality its pixelgraphics). 

Player moves through levels

    o     o     o  
                        eunints
_____________X_________nesnt   sritn

Ammo: 
xxxxxxxx  ddddddddd     iiiii    wwwwwWWWW   $$$$$  0000  bbbbb

Killing ASCII characters and words(the monsters) while collecting loot from them in form of ASCII characters. Same characters that are used in VIM commands. These are also the weapons used to kill characters and move through the map. As the game progresses new characters are introduced..


# Controls so far during debug and development.

Arrows - change char in spritesheet for debug

# Resources 
https://opengameart.org/content/mv-platformer-weapon-set-animated

# random thoughts / vim movement playground.

Different mana is required for allowing to type different chars.

Liero style hook with hook aim using vim movement, hooked char is comparable to cursor. Player position is separate.
copy physics of liero.

Player needs to select, delete, copy, paste, pure movement of player, goto row to complete levels.

Vim characters may be found in air-drops and retrieved by moving player over them and pressing x. So a level might require you
to first discover what needs to be done to reach goal, lets say delete a line that blocks further access to map, and then copy/past another line
to have a bridge over a gap but before that is done, one needs to collect the appropriate vim commands by navigating through the map with the hook. 

levels can be small and made in such a way that it requires using a specific set of commands quickly. Can have timelimits on maps, other maps can have used vim command limit. 

As the player unlocks more vim commands it can finish levels that was previously to difficult or even impossible.


