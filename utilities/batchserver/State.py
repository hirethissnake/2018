class State:
    def __init__(self, width, height, numSnakes):
        """
        Initialize the State class.

        param1: integer - width of board
        param2: integer - height of board
        param3: integer - number of snakes to create
        """

        self.width = width  # declare size of board
        self.height = height

        self.state = {
        	"you": "you",
        	"turn": 1,
        	"snakes": [
        		{
        			"taunt": "gotta go fast",
        			"name": "sneakysnake",
        			"id": "you",
        			"health_points": 100,
        			"coords": [
        				[
        					11,
        					5
        				],
        				[
        					11,
        					6
        				],
        				[
        					11,
        					7
        				]
        			]
        		}
        	],
        	"height": 20,
        	"width": 20,
        	"game_id": "gameid",
        	"food": [
        		[
        			5,
                    4
        		]
        	],
        	"dead_snakes": []
        }
