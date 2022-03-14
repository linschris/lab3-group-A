# Lab 3 Prelab, Part 6

from pycreate2 import Create2
import pyhop
import time
import random

THRESHOLD_VAL = 30

# Helper methods

def get_state(state):
    state.sees_wall = {
        'create2': sees_wall(state.agent['create2'])
    }
    return state

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
    bot.drive_stop()



def rotate_right(bot):
    bot.drive_direct(-50, 50)
    time.sleep(.5)
    bot.drive_stop()


# Define operators

def drive_to_wall(state, a):
    '''Operator: drives a given agent a to the wall.'''
    if not state.sees_wall[a]:
        print(state.agent[a])
        drive_forward(state.agent[a]) 
        return state
    return False

def rotate_from_wall(state, a):
    '''Operator: rotates a given agent a away from wall until it cannot see it anymore.'''
    if state.sees_wall[a]:
        print(state.agent[a])
        rotate_right(state.agent[a])
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
    return [('drive_to_wall', a)]

pyhop.declare_methods('drive', go_to_wall)


# naw_state = pyhop.State('create2') # 'Not at wall' = naw
# naw_state.sees_wall = { 'create2': True }



# pyhop.pyhop(naw_state, tasks=[('drive', 'create2')], verbose=3)


def main():
    # Initalize bot
    # port = '/dev/tty.usbserial-DN0266RJ'
    # baud = {
    #     'default': 115200,
    #     'alt': 19200  # shouldn't need this unless you accidentally set it to this
    # }
    # bot = Create2(port=port, baud=baud['default'])
    # bot.start()
    # bot.full()
    # Inital bot state with bot sensor data
    bot = None
    bot_state = pyhop.State('bot_state')
    bot_state.agent = {'create2': bot }
    
    prev_time = time.time()
    while time.time() - prev_time < 5:
        bot_state = get_state(bot_state)
        print(bot_state)
        # Get and execute plan
        plan = pyhop.pyhop(bot_state, tasks=[('drive', 'create2')], verbose=3)
        # Execute plan string
        exec("{method}(bot_state, \"{agent}\")".format(method=plan[0][0], agent=plan[0][1]))


if __name__ == '__main__':
    main()
