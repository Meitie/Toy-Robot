def name_the_robot():
    """This is the function to name the robot, as well as have the \n
robot greet the kids"""

    robot_name = input("What do you want to name your robot? ")
    print(f"{robot_name}: Hello kiddo!")
    return robot_name


def get_user_command(robot_name):
    """This function is used to ask the user for the command they wish \n
to send"""
    
    return input(f"{robot_name}: What must I do next? ")


def splitting_commands(user_command):
    """This takes the user command and splits it into a list of 2 inputs\n
in which the position 0 is the command and position 1 is the distance"""
    
    split_com = user_command.split(' ')
    return split_com


def legal_commands():
    """This function hosts every legal command that the function will have, \n
and it will return the legal commands"""

    legal_commands = [
        "off",
        "help",
        "forward",
        "back",
        "right",
        "left",
        "sprint",
        "reset"
    ]
    return legal_commands


def all_help():
    """This function prints a all the useable commands inside of the program"""

    print("""I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - Moves robot forward by x steps
BACK - Moves the robot backwards by x steps
RIGHT - Turns the robot right a flat 90 degrees
LEFT - Turns the robot left a flat 90 degrees
SPRINT - Shows every movemnt decending till no moves left\n""")


def is_valid_command(legal_commands, user_command):
    """This is to strip the users command with numbers, to just get the\n
command and check if it is a legal command."""

    if user_command.lower() in legal_commands:
        return True
    else:
        return False


def is_legal_movement(user_command, co_ords, degrees):
    """This function checks the current co-oridnates and checks if the \n
input of howfar the user should move forward or back is still in bounds of \n
the given safe area and returns true if the move is legal, else if the\n
movement goes out of bounds it returns false"""

    movement = user_command[0]
    steps = user_command[1]
    x = co_ords[0]
    y = co_ords[1]
    legal = True

    if movement == "back":
        steps = int(steps) * -1

    if degrees == 0:
        if ((y + int(steps)) > 200 or (y + int(steps)) < -200):
            return False
    elif degrees == 90:
        if ((x + int(steps)) > 100 or (x + int(steps)) < -100):
            return False
    elif degrees == 180:
        if ((y - int(steps)) > 200 or (y - int(steps)) < -200):
            return False
    elif degrees == 270:
        if ((x - int(steps)) > 100 or (x - int(steps)) < -100):
            return False
    return legal


def movements(robot_name, user_command):
    """This function takes what the user inputted and prints which direction\n
and how far the robot has moved"""

    distance = user_command[0]
    distance = distance.lower()
    steps = user_command[1]

    print(f" > {robot_name} moved {distance} by {steps} steps.")


def turn_direction(robot_name, direction, co_ords, user_commands, degrees):
    """Turn direction will check if the user input is either right or left\n
and stores that information and then checks against what degress the robot\n
is currently facing and then turn a sharp 90 degrees in the direction that\n
was commanded, and returns the new degrees which the robot is facing"""

    direction = "right" if user_commands[0].lower() == "right" else "left"
    
    if direction == "right":
        if (degrees + 90) == 360 or degrees == 360:
            degrees = 0
        else:
            degrees += 90
    elif direction == "left":
        if (degrees - 90) == -360 or degrees == 0:
            degrees = 270
        else:
            degrees -= 90

    print(f" > {robot_name} turned {direction}.")
    print(f" > {robot_name} now at position (%s,%s)." % co_ords)
    return degrees
     

def move_cords(user_command, co_ords, robot_name, direction, degrees):
    """This function takes the current co-ordinates, and checks them against\n
which direction the user is moving towards either forward or backwards and \n
then it will check which current degree's the robot is facing, and move the\n robot accordingly"""

    distance = user_command[0]
    distance = distance.lower()
    steps = user_command[1]
    x = co_ords[0]
    y = co_ords[1]

    if distance == "forward" or distance == "sprint":
        if degrees == 0:
            y += int(steps)
        elif degrees == 90:
            x += int(steps)
        elif degrees == 180:
            y -= int(steps)
        elif degrees == 270:
            x -= int(steps)
        print(f" > {robot_name} now at position ({x},{y}).")
        return (x,y)
    if distance == "back":
        if degrees == 0:
            y -= int(steps)
        elif degrees == 90:
            x -= int(steps)
        elif degrees == 180:
            y += int(steps)
        elif degrees == 270:
            x += int(steps)
        print(f" > {robot_name} now at position ({x},{y}).")
        return (x,y)


def calc_sprint(sprint_distance):
    """This is used to calculate how far the robot will sprint and be used to\n
to check if the distance it moves is a valid movement or not"""

    sprint_distance = int(sprint_distance)

    if sprint_distance == 0: return 0
    if sprint_distance > 0:
        sprinted = sprint_distance + calc_sprint(sprint_distance - 1)
        return sprinted


def sprint_movement(robot_name, sprint_distance):
    """This is used to calculate how far the robot will sprint as well as say\n
how many steps the robot has moved while sprinting"""

    sprint_distance = int(sprint_distance)

    if sprint_distance == 0: return 0
    if sprint_distance > 0:
        print(f" > {robot_name} moved forward by {sprint_distance} steps.")
        sprinted = sprint_distance + sprint_movement(robot_name, sprint_distance - 1)
        return sprinted


def proccess_user_command(robot_name, legal_commands):
    """This function is used to process the user command if it finds a legal\n
command it will continue on with process, if it is an illegal command, then\n
it will ask user for a new command"""

    co_ords = (0,0)
    direction = str()
    degrees = 0

    while True:
        user_command = get_user_command(robot_name)
        split_commands = splitting_commands(user_command)
        if is_valid_command(legal_commands, split_commands[0]) == False:
            print(f"{robot_name}: Sorry, I did not understand '{user_command}'.")
        else:
            if user_command.lower() == "reset":
                co_ords = (0,0)
                print(f" > {robot_name} now at position (%s,%s)." % co_ords)
            if user_command.lower() == "off":
                return print(f"{robot_name}: Shutting down..")
            if user_command.lower() == "help":
                all_help()
            if split_commands[0].lower() == "forward":
                if not len(split_commands) == 2:
                    print("Please make sure to only give a command as well as a distance")
                else:
                    legal_move = is_legal_movement(split_commands, co_ords, degrees)
                    if legal_move:
                        movements(robot_name, split_commands)
                        co_ords = move_cords(split_commands, co_ords, robot_name,direction, degrees)
                    else: 
                        print(f"{robot_name}: Sorry, I cannot go outside my safe zone.")
                        print(f" > {robot_name} now at position (%s,%s)." % co_ords)
            if split_commands[0].lower() == "back":
                if not len(split_commands) == 2:
                    print("Please make sure to only give a command as well as a distance")
                else:
                    legal_move = is_legal_movement(split_commands, co_ords, degrees)
                    if legal_move:
                        movements(robot_name, split_commands)
                        co_ords = move_cords(split_commands, co_ords, robot_name, direction, degrees)
                    else:
                        print("Please make sure to only give a command as well as a distance")
                        print(f" > {robot_name} now at position (%s,%s)." % co_ords)
            if split_commands[0].lower() == "right":
                degrees = turn_direction(robot_name, direction, co_ords,split_commands, degrees)
            if split_commands[0].lower() == "left":
                degrees = turn_direction(robot_name, direction, co_ords,split_commands, degrees)
            if split_commands[0].lower() == "sprint":
                if not len(split_commands) == 2:
                    print("Please make sure to only give a command as well as a distance")
                else:
                    sprint_distance = split_commands[1]
                    total_sprint = calc_sprint(sprint_distance)
                    legal_move = is_legal_movement(["", total_sprint], co_ords, degrees)
                    if legal_move:
                        sprinted = sprint_movement(robot_name, sprint_distance)
                        co_ords = move_cords([split_commands[0], str(sprinted)], co_ords, robot_name, direction, degrees)
                    else: 
                        print("Please make sure to only give a command as well as a distance")
                        print(f" > {robot_name} now at position (%s,%s)." % co_ords)


def robot_start():
    """This is the entry function, do not change\n
This is the start up process, by naming the robot, and then start to \n
proccess and handle the user inputs"""

    robot_name = name_the_robot()
    proccess_user_command(robot_name, legal_commands())


if __name__ == "__main__":
    robot_start()