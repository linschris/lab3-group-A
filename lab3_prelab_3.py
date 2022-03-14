"""
The "travel from home to the park" example from my lectures.
Author: Dana Nau <nau@cs.umd.edu>, May 31, 2013
This file should work correctly in both Python 2.7 and Python 3.2.
"""

''' 
Prelab 3, Part 3
Christopher Linscott
'''

import pyhop

def taxi_rate(dist):
    return (1.5 + 0.5 * dist)

def ticket_rate():
    return 500

def walk(state,a,x,y):
    if state.loc[a] == x:
        state.loc[a] = y
        return state
    else: return False

def call_taxi(state,a,x):
    state.loc['taxi'] = x
    return state
    
def ride_taxi(state,a,x,y):
    if state.loc['taxi']==x and state.loc[a]==x:
        state.loc['taxi'] = y
        state.loc[a] = y
        state.owe[a] = taxi_rate(state.dist[x][y])
        return state
    else: return False

def pay_driver(state,a):
    if state.cash[a] >= state.owe[a]:
        state.cash[a] = state.cash[a] - state.owe[a]
        state.owe[a] = 0
        return state
    else: return False

def buy_plane_ticket(state, a):
    if state.cash[a] >= ticket_rate():
        state.cash[a] -= ticket_rate()
        state.loc['plane'] = 'airport'
        return state
    return False

def fly_on_plane(state, a, x, y):
    if state.loc['plane'] == x and state.loc[a] == x:
        state.loc['plane'] = y
        state.loc[a] = y
        return state
    return False

pyhop.declare_operators(walk, call_taxi, ride_taxi, pay_driver, buy_plane_ticket, fly_on_plane)
print('')
pyhop.print_operators()



def travel_by_foot(state,a,x,y):
    if state.dist[x][y] <= 2:
        return [('walk',a,x,y)]
    return False

def travel_by_taxi(state,a,x,y):
    if state.cash[a] >= taxi_rate(state.dist[x][y]):
        return [('call_taxi',a,x), ('ride_taxi',a,x,y), ('pay_driver',a)]
    return False

def travel_by_plane(state, a, x, y):
    if state.cash[a] >= ticket_rate():
        return [('buy_plane_ticket', a), ('travel', a, x, 'airport'), ('fly_on_plane', a, 'airport', y)]
    return False


pyhop.declare_methods('travel',travel_by_foot,travel_by_taxi, travel_by_plane)
print('')
pyhop.print_methods()

state1 = pyhop.State('state1')
state1.loc = {'me':'home'}
state1.cash = {'me':20}
state1.owe = {'me':0}
state1.dist = {'home':{'park':8}, 'park':{'home':8}}

state2 = pyhop.State('state2')
state2.cash = {'sammy': 40}
state2.loc = {'sammy': 'home'}
state2.owe = {'sammy': 0}
state2.dist = {'home':{'oxy': 20}, 'oxy':{'home': 20}}

state3 = pyhop.State('state3')
state3.cash = {'lex': 1000}
state3.loc = {'lex': 'oxy'}
state3.owe = {'lex': 0 }
state3.dist = {'oxy':{'airport': 25, 'ny': 2025}, 'airport':{'oxy': 25, 'ny': 2000 } }



print("""
********************************************************************************
Call pyhop.pyhop(state1,[('travel','me','home','park')]) with different verbosity levels
********************************************************************************
""")

# print("- If verbose=0 (the default), Pyhop returns the solution but prints nothing.\n")
# pyhop.pyhop(state1,[('travel','me','home','park')])

# print('- If verbose=1, Pyhop prints the problem and solution, and returns the solution:')
pyhop.pyhop(state1,[('travel','me','home','park')],verbose=1)

# print('- If verbose=2, Pyhop also prints a note at each recursive call:')
# pyhop.pyhop(state1,[('travel','me','home','park')],verbose=2)

# print('- If verbose=3, Pyhop also prints the intermediate states:')
# pyhop.pyhop(state1,[('travel','me','home','park')],verbose=3)

pyhop.pyhop(state2,[('travel','sammy','home','oxy')],verbose=1)

pyhop.pyhop(state3,[('travel','lex','oxy','ny')],verbose=1)
