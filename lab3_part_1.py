import pyhop

# Declare state and variable bindings
maze_state = pyhop.State('maze') 
goal_state = pyhop.Goal('maze')

maze_state.loc = {'me': {'x': 0, 'y': 0}}
maze_state.last_direction = {'me': {'direction': 'null'}}
goal_state.loc = {'me': {'x': 2, 'y': 2}}

# N, S, E, W --> North, South, East, West
maze_state.direction = {'me': 'N'}

# 0 is open, 1 is wall
maze_state.maze = {'maze': [
    # North
    [0,1,1],
    [0,1,0],
    [0,0,0]
]}

# Operators 
# Move
# a = agent = 'me'

def move(state, a, x, y):
    if x < len(state.maze['maze'][0]) and y < len(state.maze['maze']) and x >= 0 and y >= 0:
        if state.maze['maze'][y][x] == 0:
            state.loc[a]['x'] = x
            state.loc[a]['y'] = y
            state.maze['maze'][y][x] = 2
    return False


            


# Method
def move_east(state, a, goal):
    # If there's no wall to right and we're not at right edge of maze, we can move right
    x = state.loc[a]['x']
    y = state.loc[a]['y']
    if x == goal.loc[a]['x'] and y == goal.loc[a]['y']:
        return []
    if x < len(state.maze['maze'][0]) - 1 and state.maze['maze'][y][x+1] != 1: 
        return [('move', a, x+1, y), ('move_toward_goal', a, goal_state)]
    return False

def move_west(state, a, goal):
    # if there is no wall to the left and we're not at left edge of maze, we can move west
    x = state.loc[a]['x']
    y = state.loc[a]['y']
    if x == goal.loc[a]['x'] and y == goal.loc[a]['y']:
        return []
    if x > 0 and state.maze['maze'][y][x-1] != 1: #
        return [('move', a, x-1, y), ('move_toward_goal', a, goal_state)]
    return False

def move_north(state, a, goal):
    #if there is no wall above we can move up
    x = state.loc[a]['x']
    y = state.loc[a]['y']
    if x == goal.loc[a]['x'] and y == goal.loc[a]['y']:
        return []
    if y > 0 and state.maze['maze'][y-1][x] != 1:
        return [('move', a, x, y-1), ('move_toward_goal', a, goal_state)]
    return False
    
def move_south(state, a, goal):
    # if there is no wall below
    x = state.loc[a]['x']
    y = state.loc[a]['y']
    if x == goal.loc[a]['x'] and y == goal.loc[a]['y']:
        return []
    if y < len(state.maze['maze']) - 1 and state.maze['maze'][y+1][x] != 1:
        return [('move', a, x, y+1), ('move_toward_goal', a, goal_state)]
    return False


# Methods
# move_towards_goal, rotate 

pyhop.declare_operators(move)
pyhop.declare_methods('move_toward_goal', move_west, move_north, move_east, move_south)


# Use planner to get a plan
pyhop.print_state(maze_state)
pyhop.print_goal(goal_state)

pyhop.seek_plan(maze_state,tasks=[('move_toward_goal', 'me', goal_state)], plan=[], depth=1, verbose=3)

