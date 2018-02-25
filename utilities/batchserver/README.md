# BatchServer
## Running the server
Navigate your terminal to the server's directory and then run the following command:

`python main.py [OPTIONS]`

### Options
| Flag | Description | Default |
|------|:-------------:|---------:|
-d, --directory | Output directory for saved game.json files | replays
-f, --food | Amount of food on board at any given time | 2
-s, --snakes | File containing snake URLs | snakes.txt
-g, --games | Number of games to simulate | 5