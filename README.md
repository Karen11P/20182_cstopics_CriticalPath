# 20182_cstopics_CriticalPath

The main idea of the project is to make an intelligent critical path using a search algorithm
in this case CSP (Constraint Satisfaction Problems). 

Constraint Satisfaction Problems:
A CSP consist of three components: 1. A set of variables, 2. A set of domains and
3. A set of constraints. Each variable in the tree will be set following a domain, it
has to satisfy the constraints given previously.

Critical path:
A critical path is a sequence of activities that show the time each one can take to be 
done. In the case that one activity that can't take longer than the set time it will be part of 
the critical path, in other words, It’s a sequence of activities where you figure out what the
least amount of time is necessary to complete a task with the least amount of slack.
So, the critical path is really the longest length of time it will take to complete the project tasks.
It has three components: 
  * A list of activities
  * The duration that each activity will take to complete
  * The dependencies between the activities.
  
There will be an example with screenshots in the 'example' folder.

To execute the program:
1. Open the terminal
2. Use cd to access the folder "20182_cstopics_CriticalPath"
3. Write "python3 criticalPath.py" in the terminal and press ENTER

Instructions
Example:

![example](https://user-images.githubusercontent.com/45362728/49258528-be532780-f403-11e8-842d-8b468954ef23.JPG)

1. Enter the total number of processes then ENTER.
2. The program will ask you the names of each process.

![step 1](https://user-images.githubusercontent.com/45362728/49258534-c317db80-f403-11e8-9819-2bfc5c725b7a.JPG)

3. Enter the predecessor (assigned letter) of each process.

![step 2](https://user-images.githubusercontent.com/45362728/49258539-c8752600-f403-11e8-906c-c60bd98b6fd0.JPG)

4. Specify the time of each process.

![step 3](https://user-images.githubusercontent.com/45362728/49258544-cdd27080-f403-11e8-9c4b-6ba44cb8eb6d.JPG)

5. The critical path will be shown in blue.

![terminal result 1](https://user-images.githubusercontent.com/45362728/49258553-d3c85180-f403-11e8-8964-5839838dbd48.JPG)
![terminal result 2](https://user-images.githubusercontent.com/45362728/49258557-d88d0580-f403-11e8-9af0-12862029d8b5.JPG)

Flow diagram of the program:
![captura](https://user-images.githubusercontent.com/45362728/49238072-a95ba180-f3cd-11e8-8e03-3d7653ccd873.JPG)


Link of the video:
https://youtu.be/FDXqOAf8Aek
