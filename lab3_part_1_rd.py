import pyhop

# Declare state and variable bindings
maze_state = pyhop.State('maze') 
goal_state = pyhop.Goal('maze')

maze_state.loc = {'me': {'x': 0, 'y': 0}}
maze_state.last_direction = {'me': {'direction': 'null'}}
goal_state.loc = {'me': {'x': 2, 'y': 4}}

# N, S, E, W --> North, South, East, West
maze_state.direction = {'me': 'N'}

# 0 is open, 1 is wall
maze_state.maze = {'maze': [
    # North
    #[0,1,1],
    #[0,1,0],
    #[0,0,0]
    [0,1,1,1,0],
    [0,1,0,0,0],
    [0,0,0,1,0],
    [0,1,1,1,0],
    [0,1,0,0,0]
]}

# Operators 
# Move
# a = agent = 'me'



def move_east(state, a, x, y):
    # If there's no wall to right and we're not at right edge of maze, we can move right
    if x < len(state.maze['maze'][0]) - 1 and state.maze['maze'][y][x+1] != 1: 
        state.loc[a]['x'] = x+1
        state.last_direction[a]['direction'] = 'west'
        return state
    return False

def move_west(state, a, x, y):
    # if there is no wall to the left and we're not at left edge of maze, we can mvoe
    if x > 0 and state.maze['maze'][y][x-1] != 1: #
        state.loc[a]['x'] = x-1
        state.last_direction[a]['direction'] = 'east'
        return state
    return False

def move_north(state, a, x, y):
    #if there is no wall above we can move up
    if y > 0 and state.maze['maze'][y-1][x] != 1:
        state.loc[a]['y'] = y - 1
        state.last_direction[a]['direction'] = 'south'
        return state
    return False
    
def move_south(state, a, x ,y):
    # if there is no
    if y < len(state.maze['maze']) - 1 and state.maze['maze'][y+1][x] != 1:
        state.loc[a]['y'] = y + 1
        state.last_direction[a]['direction'] = 'north'
        return state
    return False

pyhop.declare_operators(move_east, move_west, move_north, move_south)

# Methods
# move_towards_goal, rotate 

def move_towards_goal(state, a, goal):
    x = state.loc[a]['x']
    y = state.loc[a]['y']
    # print("x: {x} y: {y}".format(x=x,y=y))
    if goal.loc[a]['x'] == x and goal.loc[a]['y'] == y:
        # We're done
        return []
    availableDirections = {'north': False, 'east': False, 'south': False, 'west': False}
    # East
    if x < len(state.maze['maze'][0]) - 1 and state.maze['maze'][y][x+1] != 1: 
        availableDirections['east'] = True

    # West
    if x > 0 and state.maze['maze'][y][x-1] != 1 : 
        availableDirections['west'] = True

    # North
    if y > 0 and  state.maze['maze'][y-1][x] != 1:
        availableDirections['north'] = True

    # South
    if y < len(state.maze['maze']) - 1 and state.maze['maze'][y+1][x] != 1:
        availableDirections['south'] = True

    lastDirection = state.last_direction[a]['direction']
    if lastDirection == 'north':
        directions = ['east','west','south','north']
    elif lastDirection == 'south':
        directions = ['east','west','north','south']
    elif lastDirection == 'east':
        directions = ['north','south','west','east']
    else:
        directions = ['south','north','east','west']
    
    if lastDirection is not 'null':
        directions.remove(lastDirection)
        directions.append(lastDirection)

    for direction in directions:
        if availableDirections[direction]:
            return [('move_{dir}'.format(dir=direction), a, x, y), ('move_toward_goal', a, goal_state)]

    # At this point nothing happened, so we're done. We should never get here
    return []


pyhop.declare_methods('move', move_towards_goal)



# Use planner to get a plan
pyhop.print_state(maze_state)
pyhop.print_goal(goal_state)

pyhop.pyhop(maze_state,[('move_toward_goal', 'me', goal_state)],verbose=1)

