# Lab 3 Prelab, Part 6

from pycreate2 import Create2
import pyhop
import time

THRESHOLD_VAL = 30

# Define operators

def drive_to_wall(state, a):
    '''Operator: drives a given agent a to the wall.'''
    if not state.sees_wall[a]:
        state.sees_wall[a] = True
        return state
    return False

def rotate_from_wall(state, a):
    '''Operator: rotates a given agent a away from wall until it cannot see it anymore.'''
    if state.sees_wall[a]:
        state.sees_wall[a] = False
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


naw_state = pyhop.State('create2') # 'Not at wall' = naw
naw_state.sees_wall = { 'create2': True }



pyhop.pyhop(naw_state, tasks=[('drive', 'create2')], verbose=3)
