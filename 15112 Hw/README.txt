>>>>Description
“In the beginning” is a 3D game where users can generate an initial 3D land terrain 
which serves as a canvas for their world to come. In the beginning, the user will have
starting items, a lake located in the valleys of the 3D terrain they created, infinite 
rocks, and infinite shrubs. By strategically placing the rocks and plants, the user 
can discover new world elements like trees and fire to build their way to more complex
elements. And in the end, they will have a whole world that started from a blank canvas 
and a body of water!

>>>>How to run the project
Download all files grayScott, ProjectionOperationsWithDrag, worldElements, 
BoidTest, DayNight, and cmu_112_graphics. Make you you have PIL installed as well. Open grayScott.py,
and simply press run.

No libraries besides PIL are used.

>>>>Hack the game:
All the items are stored under appStarted as app.can<item name>. Simply change 
the item's app.can<itemName> field to be true and that item is accessible.

There are keyboard shortcuts for the items so you dont have to click the buttons 
each time. These are found in the keyPressed method, but are also listed at the bottom of this txt file.



    #switch to rock mode and/or plant mode
    if event.key == "r" - rock
                    "s" - seed
                    "p" - planet
                    "d" - dirt
                    "t" - tree
                    "f" - flower
                    "o" - fruit
                    "m" - steel 
                    "0" - tool (the Purple thing) 
                    "1" - iron 
                    "2" - coal
                    "3" - diamonds
                    "4" - gold
                    "." - expand the map
