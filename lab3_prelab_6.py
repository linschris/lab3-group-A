# Lab 3 Prelab, Part 6

from pycreate2 import Create2
import pyhop
import time

THRESHOLD_VAL = 30

# Helper methods
def get_state(state):
    state.sees_wall = {
        'create2': sees_wall(state.bot['create2'])
    }

def sees_wall(bot):
    sensor = bot.get_sensors()
    # sensor_list --> L FR CL CR FR R
    sensor_list = [sensor.light_bumper_left, sensor.light_bumper_front_left, sensor.light_bumper_center_left, sensor.light_bumper_center_right, sensor.light_bumper_front_right, sensor.light_bumper_right]

    # Check if any of the IR sensors register a wall.
    for sensor_val in sensor_list:
        if sensor_val > THRESHOLD_VAL:
            return True

    # Check if any of the bumper sensors register anything.
    return sensor.bumps_wheeldrops.bump_left or sensor.bumps_wheeldrops.bump_right

def drive_forward(bot):
    bot.drive_direct(100, 100)
    time.sleep(.5)
    # bot.drive_stop()


def rotate_right(bot):
    bot.drive_direct(-50, 50)
    time.sleep(.5)
    # bot.drive_stop()


# Define operators

def drive_to_wall(state, a):
    '''Operator: drives a given agent a to the wall.'''
    if not state.sees_wall[a]:
        drive_forward(state.bot[a]) 
        get_state(state)
        return state
    return False

def rotate_from_wall(state, a):
    '''Operator: rotates a given agent a away from wall until it cannot see it anymore.'''
    if state.sees_wall[a]:
        rotate_right(state.bot[a])
        get_state(state)
        return state
    return False 

pyhop.declare_operators(drive_to_wall, rotate_from_wall)

# Define methods

def go_to_wall(state, a):
    '''
        A method for driving the robot. \n
            - Precondition: 
                - Checks if robot is at wall.
            -  State Change:
                - If robot is at wall, rotate away from wall.
                - Otherwise, drive until you see a wall.
    '''
    if state.sees_wall[a]:
        return [('rotate_from_wall', a)]
    elif not state.sees_wall[a]:
        return [('drive_to_wall', a)]
    return False

pyhop.declare_methods('drive', go_to_wall)


def main():
    # Initalize bot
    port = '/dev/tty.usbserial-DN026A6A'
    baud = {
        'default': 115200,
        'alt': 19200  # shouldn't need this unless you accidentally set it to this
    }
    bot = Create2(port=port, baud=baud['default'])
    bot.start()
    bot.full()


    # Inital bot state
    bot_state = pyhop.State('bot_state')
    bot_state.bot = {'create2': bot }
    while True:
        get_state(bot_state)
        # Get and execute plan
        plan = pyhop.pyhop(bot_state, tasks=[('drive', 'create2')], verbose=1)
        # Execute plan string
        exec("bot_state = {method}(bot_state, \"{agent}\")".format(method=plan[0][0], agent=plan[0][1]))
if __name__ == '__main__':
    main()
