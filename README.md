# 20182_cstopics_CriticalPath

The main idea of the project is to make an intelligent critical path using a search algorithm
in this case CSP (Constraint Satisfaction Problems). 

Constraint Satisfaction Problems:
A CSP consist of three components: 1. A set of variables, 2. A set of domains and
3. A set of constraints. Each variable in the tree will be set following a domain, it
has to satisfy the constraints given previously.

Critical path:
A critical path is a sequence of activities that show the time each one can take to be 
done. In the case that one activity can't take longer than the set time it will be part of 
the critical path. It has three components: 
  * A list of activities
  * The duration that each activity will take to complete
  * The dependencies between the activities.
  
There will be an example with screenshots in the 'example' folder.

To execute the program:
1. Open the terminal
2. Use cd to access the folder "20182_cstopics_CriticalPath"
3. Write "python3 criticalPath.py" in the terminal and press ENTER

Instructions
1. Enter the total number of processes then ENTER.
2. The program will ask you the names of each process.
3. Enter the predecessor (assigned letter) of each process.
4. Specify the time of each process.
5. The critical path will be shown in blue.

Link of the video:
https://youtu.be/FDXqOAf8Aek
