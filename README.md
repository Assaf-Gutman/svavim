# svavim
find an optimal solutin to divide students to groups by the student's preference

# General


##### The problem that we are trying to solve is to assign 63 studens to eight groups with some limitations
##### This script uses Google OR to solve optimization problems
##### Google OR tool is an open source software for opimazitoing problems using linear programing
##### You can read more about the tool in https://developers.google.com/optimization/introduction/overview
##### The script is based on the assigment problem that is presented with simple examples at 
##### https://developers.google.com/optimization/assignment/overview and were modified to our needs.

## Installation

To install the script go into the folder of the script and run

```
python -m venv venv
```

This will create the virtual environment.


Activate the virtual environment

```
source venv/bin/activate
```

then run the next commant to install all dependencies that require to run the script


```
pip3 install -r requirements.txt
```

if u like to run the script from terminal run the next command, where path is the path to the excel file


```
python3 main.py <path> (see below)
```
# Input
when runing the script from IDE, a folder picker will be open to choose your excel file, u can also run the script from the terminal 
by speficy the excel file path

# Output

the output will be an CSV file name: assign.csv 
the file will be store in the same folder as the script
with what group assign to what option
notice that it might be issue with hebrew, so better write names in english

# Excel Format 
1. how many members in the group
2. first member's name 
3. second member's name 
4. third member's name
5. to 12 the options that u pick, when line column 3 is the most desire option and column 10 is the less desire 



