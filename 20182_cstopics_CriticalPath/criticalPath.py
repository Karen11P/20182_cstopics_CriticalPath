from utils import argmin_random_tie, count, first
import utils
import search
import sys, getopt
import logging
import os
import pygame
from pygame.locals import *

assignment_2=[]
def update(assignment):
	global assignment_2
	for a in range(len(assignment)):
		b = 0
		exist = False
		if assignment[a] not in assignment_2:
			assignment_2.append(assignment[a])
		for b in range(len(assignment_2)):
			if assignment_2[b] in assignment[a]:
				exist = True
			else:
				value = assignment_2[b]
		if exist == False:
			assignment_2.remove(value)

#----------------------------------------------------------
#CSP
class CSP(search.Problem):
    def __init__(self, variables, domains, neighbors, constraints):
        variables = variables or list(domains.keys())
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = ()
        self.curr_domains = None
        self.nassigns = 0

    def assign(self, var, val, assignment):
        assignment[var] = val
        self.nassigns += 1

    def nconflicts(self, var, val, assignment):
        def conflict(var2):
            return (var2 in assignment and
                    not self.constraints(var, val, var2, assignment[var2]))
        return count(conflict(v) for v in self.neighbors[var])

    def display(self, assignment):
        update(assignment)
        print('CSP with assignment:', assignment)
       
    def actions2(self, var, assignment):
        domain = []
        if var in assignment:
            domain.append(assignment[var])
        else:
            domain = [val for val in self.domains[var]
                    if self.nconflicts(var, val, assignment) == 0]
        return domain

    def goal_test(self, state):
        assignment = dict(state)
        return (len(assignment) == len(self.variables)
                and all(self.nconflicts(variables, assignment[variables], assignment) == 0
                        for variables in self.variables))

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def suppose(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def choices(self, var):
        return (self.curr_domains or self.domains)[var]

#----------------------------------------------------------
#CSP Backtracking Search
def first_unassigned_variable(assignment, csp):
    return first([var for var in csp.variables if var not in assignment])

def unordered_domain_values(var, assignment, csp):
    return csp.choices(var)

def no_inference(csp, var, value, assignment, removals):   
    return True

def backtracking_search(csp,
                        select_unassigned_variable=first_unassigned_variable,
                        order_domain_values=unordered_domain_values,
                        inference=no_inference):
    def backtrack(assignment):
        if len(assignment) == len(csp.variables):
            return assignment
        var = select_unassigned_variable(assignment, csp)

        for value in order_domain_values(var, assignment, csp):
            if 0 == csp.nconflicts(var, value, assignment):
                csp.assign(var, value, assignment)
                removals = csp.suppose(var, value)
                update_domain(csp,assignment)
                if inference(csp, var, value, assignment, removals):
                    result = backtrack(assignment)    
                    if result is not None:
                        return result
                csp.restore(removals)
        csp.unassign(var, assignment)
        return None

    result = backtrack({})
    return result

#----------------------------------------------------------
#Ask for processes, predecessors and time
abc = ["i","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U"] 
print("--------------------------------------------------------------------------------")
while(1):
	try:
		n_processes = int(input("How many processes are required?: "))
		if(n_processes > 20):
			print("Invalid! Maximum 20 processes")
		else:
			break;
	except:
		print("Invalid! Only numbers")
variables = list(range(0,n_processes+2))

print("")
print("Enter the processes, the first one is the start and the last one is the end")
name_processes = ["start"]
for i in range(n_processes):
	print(abc[i+1]," process: ")
	while(1):
		valor = input()
		if(valor == ''):
			print("Enter the name of the process")
		else:
			break;
	name_processes.append(valor)
name_processes.append("end")

processes = ''
for i in range(n_processes+1):
	processes = processes+abc[i]
processes = processes + "e"

predecessors = ["i"]
print("")
print("Enter the predecessor (letter) of each process, if it doesn't have one enter i, the process e is the end")
print("The first process doesn't have a predecessor")
for i in range(n_processes):
	print("   ",processes[i+1],name_processes[i+1])
for i in range(n_processes):
	print(processes[i+2]," depends on: ")
	while(1):
		correct = True
		valor = input()
		if(valor == ''):
			print("Enter the predecessor")
			correct = False
		else:
			for letter in valor:
				if((letter not in processes)or(letter == processes[i+2])or(letter == '')or(letter == "e")):
					print("Enter the letter of the process, don't use the same process")
					correct = False
		if(correct):
			break
	predecessors.append(valor)

time = [0]
print("")
print("Enter the time (hours) that each process takes")
for i in range(n_processes):
	print("   ",abc[i+1],name_processes[i+1])
for i in range(n_processes):
	print(abc[i+1]," takes: ")
	while(1):
		try:
			time.append(int(input()))
			break;
		except:
			print("Invalid! Only numbers")
time.append(0)

#----------------------------------------------------------
#Organize each processes
number_process = []
for i in range(n_processes+2):
	number_process.append(0)
j = 0;
for x in range(len(number_process)):
	for y in range(len(predecessors)):
		for letter in predecessors[y]:
			if((processes[number_process.index(x)] == letter)and(number_process[processes.index(processes[y+1])] == 0)):
				j = j+1
				number_process[processes.index(processes[y+1])] = j

#----------------------------------------------------------
#Generate the constraint tree
neighbors = {}
for x in range(n_processes+2):
	array = []
	if(x != 0):
		for letter in predecessors[x-1]:
			array.append(number_process[processes.index(letter)])
	for y in range(n_processes+1):
		for letter in predecessors[y]:
			if(processes[x] == letter):
				array.append(number_process[y+1])
	neighbors[number_process[x]] = array

depend_on = {}
for x in range(n_processes+2):
	array = []
	if(x != 0):
		for letter in predecessors[x-1]:
			array.append(processes[processes.index(letter)])
	for y in range(n_processes+1):
		for letter in predecessors[y]:
			if(processes[x] == letter):
				array.append(processes[y+1])	
	depend_on[processes[x]] = array
print("--------------------------------------------------------------------------------")	

#----------------------------------------------------------
#Print assignment
name = []
def update_domain(csp, assignment):
    csp.display(assignment)
    for Xi in csp.variables:
        domain = csp.actions2(Xi,assignment)
        print(Xi,'->',name_processes[processes.index(domain[0])])
    print(" ")	

#----------------------------------------------------------
#CSP problem formulation
def different_values_constraint(A, a, B, b):
	boolean = True
	if (a==b):
		boolean = False
	elif a not in depend_on[b]:
		boolean = False
	elif a in assignment_2:
		boolean = False
	return boolean

domains = dict.fromkeys(variables, processes)

network = CSP(variables, domains, neighbors, different_values_constraint)
#----------------------------------------------------------
#Calculate critical path
def critical_path(result):
	global result_states
	result_states = result
	global t_states
	t_states = {}
	t_sum = 0
	for i in range(n_processes+2):
		if (i == 0):
			t_states[i] = [t_sum,t_sum+time[number_process.index(i)]]
		t_sum = t_states[i][1]
		for state in neighbors[i]:	
			if (int(state) > i): 
				t_result = t_sum+time[number_process.index(state)]
				try:
					if(t_sum > t_states[state][0]):
						t_states[state] = [t_sum,t_result]
						break;
				except:
					t_states[state] = [t_sum,t_result]

	size = len(t_states)
	for i in range(size):
		y = i+1
		if (i == 0):
			t_states[size-y] = [t_states[size-y][0],t_states[size-y][1],t_sum,t_sum-time[number_process.index(size-y)],(t_sum-time[number_process.index(size-y)]-t_states[size-y][0])]
		t_sum = t_states[size-y][3]
		for state in neighbors[size-y]:	
			if (int(state) < size-y): 
				t_result = t_sum-time[number_process.index(state)]
				try:
					if(t_sum < t_states[state][2]):
						t_states[state] = [t_states[state][0],t_states[state][1],t_sum,t_result,(t_result-t_states[state][0])]
						break;
				except:
					t_states[state] = [t_states[state][0],t_states[state][1],t_sum,t_result,(t_result-t_states[state][0])]
	print("--------------------------------------------------------------------------------")
	print("If the slack is different than 0, the process can take those hours more (slack) to be done")
	print("Process | Slack")
	for state in t_states:
		print("  ",name_processes[number_process.index(state)]," -> ",t_states[state][4])
	final_path = ["start"]
	global result_path
	result_path = [0]
	for i in range(len(t_states)):
		try:
			for number in neighbors[result_path[i]]:
				if((number > result_path[i])and(t_states[number][4]) == 0):
					result_path.append(number)
					final_path.append(name_processes[number_process.index(number)])
					break;
		except:
			break;
	print(" ")
	print("The critical path is:")
	print(final_path)
	print("--------------------------------------------------------------------------------")

#----------------------------------------------------------
# Main program
def main(argv):
	try:
		opts,args = getopt.getopt(argv, "v:o:i:", ["variableSelection=","orderValues=","inference="]) 
	except getopt.GetoptError:
		print('python3 csp.py')
		print('python3 csp.py -v mrv -o lrv -i mac')
		print('python3 csp.py --variableSelection mrv --orderValues lrv --inference mac')
		sys.exit(2)
	if opts == []:
		result = backtracking_search(network)
		critical_path(result)
	else:
		variableSelection = first_unassigned_variable
		orderValues = unordered_domain_values
		infer = no_inference
		for opt,arg in opts:
			if opt in ("-v","--variableSelection"):
				if arg == 'mrv':
					variableSelection = mrv					
				else:
					print('Method not recognized')
					sys.exit(2)
			if opt in ("-o","--orderValues"):
				if arg == 'lcv':
					orderValues = lcv
				else:
					print('Method not recognized')
					sys.exit(2)
			if opt in ("-i","--inference"):
				if arg == 'mac':
					infer=mac
				else:
					print('Method not recognized')
					sys.exit(2)
		result = backtracking_search(network, 
			        select_unassigned_variable=variableSelection,
                    order_domain_values=orderValues,
                    inference=infer)   

if __name__ == "__main__":
	main(sys.argv[1:])
#----------------------------------------------------------
# Pygame, show results
def write(msg):
    myfont = pygame.font.SysFont("None",40)
    mytext = myfont.render(msg, True, (0,0,0))
    mytext = mytext.convert_alpha()
    return mytext

assigned = [[0]]
array2 = []
array3 = []		
for i in range(len(neighbors)):
	t = 0
	array2 = []
	try:
		array = assigned[i]
	except:
		break;
	for j in range(len(array)):
		for number in neighbors[array[j]]:
			if(number > array[j])and(number not in array3):
				t = t+1
				array2.append(number)
			array3.append(number)
	if(array2 != []):
		assigned.append(array2)

branches = []
for i in range(len(assigned)):
	array = assigned[i]
	branches.append(len(array))
		
columns = len(branches)
rows = max(branches)

diameter_circle = 30
radius_circle = diameter_circle*2
circle_space = radius_circle*2

width_matrix = circle_space*columns
height_matrix = circle_space*rows

width = width_matrix+300
height = height_matrix
if (40*len(neighbors) > height):
	height = 40*len(neighbors)

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Critical Path")
screen.fill((255,255,255))

range_pos = circle_space/2
pos_states = []
for i in range(columns):
	x = int(range_pos+(circle_space*i))
	for j in range(branches[i]):
		y = int(range_pos+(circle_space*j))
		if((x,y)not in pos_states):
			pos_states.append((x,y))
			
colors = []
for i in range(len(neighbors)):
	if(i in result_path):
		colors.append((135,206,250))
	else:
		colors.append((173,255,47))

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	for i in range(len(neighbors)):
		for j in neighbors[i]:
			pygame.draw.line(screen, (0,0,0), pos_states[i], pos_states[j],4)
	for i in range(len(neighbors)):
		pygame.draw.circle(screen, (0,0,0), pos_states[i], diameter_circle+3)
		pygame.draw.circle(screen, colors[i], pos_states[i], diameter_circle)
	for i in range(len(neighbors)):
		textsurface = write(result_states[i])
		x,y =  pos_states[i]
		screen.blit(textsurface, ((x-10),(y-10)))
	for i in range(len(neighbors)):	
		text = "S="+str(t_states[i][4])
		textsurface = write(text)
		x,y =  pos_states[i]
		screen.blit(textsurface, ((x-diameter_circle),(y-radius_circle)))
	for i in range(len(neighbors)):	
		text = str(processes[i]+" -> "+name_processes[i])
		textsurface = write(text)
		x = width_matrix+50
		y = 30*(i+1)
		screen.blit(textsurface, (x,y))
	pygame.display.flip()	
