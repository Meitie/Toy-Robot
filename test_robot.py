import unittest
from io import StringIO
from unittest.mock import patch
import sys
import robot


class TestRobot(unittest.TestCase):

    @patch("sys.stdin", StringIO("HAL"))
    def test_naming_robot(self):
        """This tests the name input and checks that the output is properly"""

        sys.stdout = StringIO()
        self.assertEqual(robot.name_the_robot(), "HAL")
        self.assertEqual(sys.stdout.getvalue().strip(), """What do you want to name your robot? HAL: Hello kiddo!""")


    def test_processing_inputs(self):
        """This is a test that checks if the commands passed through are\n
legal"""

        self.assertTrue(robot.is_valid_command(robot.legal_commands(), "Help"))
        self.assertTrue(robot.is_valid_command(robot.legal_commands(), "OFF"))
        self.assertTrue(robot.is_valid_command(robot.legal_commands(), "OfF"))
        self.assertTrue(robot.is_valid_command(robot.legal_commands(), "HeLP"))
        self.assertFalse(robot.is_valid_command(robot.legal_commands(), "Jump"))


    def test_move_forward(self):
        """Tests the movement output, when given forward and the distance it will make check output is the same"""

        sys.stdout = StringIO()
        robot.movements("Bob", ["forward", "100"])
        robot.movements("Bob", ["forward", "10"])
        self.assertEqual(sys.stdout.getvalue().strip(), """> Bob moved forward by 100 steps.\n > Bob moved forward by 10 steps.""")


    def test_co_ords_forward(self):
        """Tests the co-ordinates vs when the robot moves forwards"""

        sys.stdout = StringIO()
        self.assertEqual(robot.move_cords(["forward", "100"], (0, 0), "HAL", str(), 0), (0, 100))
        self.assertEqual(robot.move_cords(["forward", "10"], (0, 0), "HAL", str(), 0), (0, 10))
        self.assertEqual(robot.move_cords(["forward", "10"], (0, 10), "HAL", str(), 0), (0, 20))
        self.assertEqual(sys.stdout.getvalue().strip(), """> HAL now at position (0,100).\n > HAL now at position (0,10).\n > HAL now at position (0,20).""")


    def test_move_backward(self):
        """Testing the move back functionality of the program"""

        sys.stdout = StringIO()
        robot.movements("HAL", ["back", "53"])
        robot.movements("HAL", ["back", "8"])
        self.assertEqual(sys.stdout.getvalue().strip(), """> HAL moved back by 53 steps.\n > HAL moved back by 8 steps.""")


    def test_co_ords_back(self):
        """Testing the co-ordionates for when the robot moves backwards"""

        sys.stdout = StringIO()
        self.assertEqual(robot.move_cords(["back", "100"], (0, 0), "HAL", str(), 0), (0, -100))
        self.assertEqual(robot.move_cords(["back", "10"], (0, 30), "HAL", str(), 0), (0, 20))
        self.assertEqual(robot.move_cords(["back", "20"], (0, 10), "HAL", str(), 0), (0, -10))
        self.assertEqual(sys.stdout.getvalue().strip(), """> HAL now at position (0,-100).\n > HAL now at position (0,20).\n > HAL now at position (0,-10).""")


    def test_turning_right(self):
        """This tests the turning right functionality of the robot, \n
turning right is a 90 deg turn"""

        self.assertEqual(robot.turn_direction("HAL", "", (0,0), ["right"], 0), 90)
        self.assertEqual(robot.turn_direction("HAL", "", (0,0), ["right"], 90), 180)
        self.assertEqual(robot.turn_direction("HAL", "", (0,0), ["right"], 180), 270)
        self.assertEqual(robot.turn_direction("HAL", "", (0,0), ["right"], 270), 0)


    def test_turning_left(self):
        """This tests the turning left functionality of the robot, \n
turning left is a 90 deg turn"""

        self.assertEqual(robot.turn_direction("HAL", "", (0,0), ["left"], 0), 270)
        self.assertEqual(robot.turn_direction("HAL", "", (0,0), ["left"], 90), 0)
        self.assertEqual(robot.turn_direction("HAL", "", (0,0), ["left"], 180), 90)
        self.assertEqual(robot.turn_direction("HAL", "", (0,0), ["left"], 270), 180)


    def test_out_of_bounds(self):
        """This tests the out of bounds functionality to make sure that the \n
robot does not move out of bounds from the given area, a 200x400 rectangle"""

        self.assertTrue(robot.is_legal_movement(["forward", "90"], (0,0), 0))
        self.assertTrue(robot.is_legal_movement(["back", "50"], (0,0), 0))
        self.assertFalse(robot.is_legal_movement(["forward", "250"], (0,0), 0))
        self.assertFalse(robot.is_legal_movement(["back", "250"], (0,0), 0))
        self.assertTrue(robot.is_legal_movement(["back", "50"], (0,100), 0))
        self.assertTrue(robot.is_legal_movement(["back", "150"], (0,100), 0))
        self.assertTrue(robot.is_legal_movement(["forward", "400"], (0,-200), 0))
        self.assertTrue(robot.is_legal_movement(["forward", "200"], (-100,0), 90))
        self.assertTrue(robot.is_legal_movement(["forward", "50"], (-100,0), 90))
        self.assertFalse(robot.is_legal_movement(["back", "50"], (-100,0), 90))


    def test_spring_command(self):
        """This is to test the sprinting command functionality where it will \n
say on each line what is being done and then update the co-ordinates"""

        sys.stdout = StringIO()
        self.assertEqual(robot.sprint_movement("HAL", "5"), 15)
        self.assertEqual(robot.sprint_movement("HAL", "10"), 55)
        self.assertEqual(sys.stdout.getvalue().strip(), """> HAL moved forward by 5 steps.
 > HAL moved forward by 4 steps.
 > HAL moved forward by 3 steps.
 > HAL moved forward by 2 steps.
 > HAL moved forward by 1 steps.
 > HAL moved forward by 10 steps.
 > HAL moved forward by 9 steps.
 > HAL moved forward by 8 steps.
 > HAL moved forward by 7 steps.
 > HAL moved forward by 6 steps.
 > HAL moved forward by 5 steps.
 > HAL moved forward by 4 steps.
 > HAL moved forward by 3 steps.
 > HAL moved forward by 2 steps.
 > HAL moved forward by 1 steps.""")
    

if __name__ == '__main__':
    unittest.main()