import sys
import random
from sys import exit
from textwrap import dedent

# You can use this if you don't wan't the same number generated consecutively
class MyRand(object):
    def __init__(self, min, max):
        self.last = None
        self.min = min
        self.max = max

    def __call__(self):
        r = random.randint(self.min, self.max)
        while r == self.last:
            r = random.randint(self.max, self.max)
        self.last = r
        return r

randint = MyRand(1, 6)

class Player:
    def __init__(self, name, current_position):
        self.name = name
        self.current_position = current_position
        self.started = False
        self.quit = False

    def __str__(self):
        return self.name


class Game(object):

    Game_dict={
        'snakes':{35:4,43:9,49:33,59:23,69:50,76:45,82:64,86:47,93:52,98:14},
        'ladders':{6:58,13:31,18:61,46:68,70:89,79:84}
    }

    def __init__(self, player1, player2):
        self.players = [
            Player(player1, 0),
            Player(player2, 0),
        ]
        self.turn = 0
        self.game_started = False

    def snake_or_ladder(self, player):
        for x, y in self.Game_dict.items():
            if player.current_position in y:
                a = player.current_position
                b = y[player.current_position]

                player.current_position = b

                if x == 'ladders':
                    print(f"Wooow!!! The ladder at position {a} has taken you to position {b}.")
                    print(f"Your current position is {player.current_position}.")
                else:
                    print(f"Oooopps!!! The snake at position {a} retarded you to position {b}.")
                    print(f"Your current position is {player.current_position}.")

    def play(self, player):
        letter = ''
        while letter not in ['p', 'q']:
            print("Press letter 'p' to get the dice rolling or q to quit")
            letter = input("Roll dice >")

        if letter.lower() == 'q':
            player.quit = True
            return

        roll = randint()
        print(f'{player} rolled {roll}')

        if not player.started:
            if roll != 6:
                print(dedent("""
                    You didn't get a 6!!!
                    Roll dice again."""))
                return
            else:
                print(dedent("""
                    You got a 6!!!
                    Roll dice again."""))
                player.started = True
                return self.play(player)

        new_position = player.current_position + roll
        if new_position>100:
            print("The end position is 100. Try again next time.")
            return
        player.current_position = new_position

        self.snake_or_ladder(player)

        if roll == 6:
            self.play(player)


    def start_game(self):
        print(dedent(f"""
        Hi {self.players[0]} and {self.players[1]}, Welcome to snakes and ladders. You are at the start
        position and you will need a 'six' to leave the start
        position.
        """))
        while True:
            if self.game_started:# If false: returns nothing unlike if true
                self.turn ^= 1  #use xor to flip turn between 0 and 1
            else:
                self.game_started = True
            player = self.players[self.turn]
            print(f'\nYour turn {player}\n')
            self.play(player)

            print(f"{player}'s current position is {player.current_position}")

            self.possibly_end_game(player)

    def possibly_end_game(self, player):
        if player.current_position==100:
            print("Congratulations! You have finished the game")
            exit(0)
        elif player.quit:
            print(f"{player} quits! You have finished the game")
            exit(1)


player1, player2 = sys.argv[1], sys.argv[2]
print("players", player1, player2)

a_game = Game(player1, player2)
a_game.start_game()


''' PSEUDOCODE I USED TO THINK THIS THROUGH
play
   play or quit
   if quit
      set player quit
      return

   roll
   if not started:
      if not six
        print not six
        return
      else
        set started
        return play
   move
   snake_or_ladder
   if 6 play


while True
   set turn
   play
   if game_ended
     exit
'''
