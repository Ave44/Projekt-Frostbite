import unittest
from game.Player import Player

class PlayerTests(unittest.TestCase):

    def test_player_movement_diagonal_U_R(self):
        player = Player([64,64],[])
        player.speed = 10
        player.direction.x = 1
        player.direction.y = 1
        player.move()
        self.assertEqual(player.rect.topleft, [71,71], "Movement direction vector should be normalized")
    
    def test_player_movement_diagonal_U_L(self):
        player = Player([64,64],[])
        player.speed = 10
        player.direction.x = -1
        player.direction.y = 1
        player.move()
        self.assertEqual(player.rect.topleft, [-71,71], "Movement direction vector should be normalized")

    def test_player_movement_diagonal_D_R(self):
        player = Player([64,64],[])
        player.speed = 10
        player.direction.x = 1
        player.direction.y = -1
        player.move()
        self.assertEqual(player.rect.topleft, [71,-71], "Movement direction vector should be normalized")

    def test_player_movement_diagonal_D_L(self):
        player = Player([64,64],[])
        player.speed = 10
        player.direction.x = -1
        player.direction.y = -1
        player.move()
        self.assertEqual(player.rect.topleft, [-71,-71], "Movement direction vector should be normalized")


if __name__ == '__main__':
    unittest.main()