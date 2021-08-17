from ortools.linear_solver import pywraplp
import random
import math
import pandas as pd
import numpy as np
import sys



def create_data(filename , file_extension):
    '''
    this function get a file path and return three data types:
    1. a cost matrix, this cost matrix represnet how student rank an specific option,
    it look for the location of the option within the student's vector and convert it to score.
    2. size vector - how many students in each group
    3. name list- better be in english
    :param filename: the path to the excel file that we reading the data from
    :return: cost matrix , group size vectoer, name list
    '''
    # incase that we are reding an csv file
    if file_extension == '.csv':
        df = pd.read_csv(filename)
    else:
    # read excel file
        df = pd.read_excel(filename)
    # check if the file in the right format
    names =list(zip(df.iloc[:, 1].tolist(), df.iloc[:,2].fillna('').tolist(), df.iloc[:, 3].fillna('').tolist()))
    all_members = []
    for name in names:
        all_members.append(filter_empty(name))

    size = df.iloc[:, 0].tolist()
    raw = []
    # get columns data
    for i in range(8):
        raw.append(  list( map(extract_string, df.iloc[:, i + 4].tolist())))
    array = np.array(raw)
    transpose = array.T
    transpose_list = transpose.tolist()
    cost = []
# convert to score matrix
    for j in range(len(transpose_list)):
        new = []
        for i in range(8):
            new.append((transpose_list[j].index(i+1))+1)
        cost.append(new)
    return cost , size , all_members


def transform_cost(cost_matrix ,group_size):
    '''
    this function get a cost matrix and group size vector and return three data types:
    1. a manipulated cost matrix, this cost matrix will be generted by the lambda expression.
    2. number of groups
    3. number of taske
    :param cost_matrix: an original cost matrix before manipulation
    :param group_size - a vectoer with how manny students in each group
    :return: new cost matrix , num_groups, name list , num_options
    '''
    num_groups = len(cost_matrix)
    num_options = len(cost_matrix[0])

    new_cost_matrix = []
    # to create the model punish worth high rank we powering the rate, and also multiplying in the amount of the team members, so group of 3 will be treated diffrently then one
    for i in range (len(cost_matrix)):
        new_cost_matrix.append(list(map(lambda x: x*x, cost_matrix[i])))
    return new_cost_matrix , num_groups , num_options


def generate_solver(cost_matrix,group_size ,num_groups, num_options):
    '''
    this function create the solver object with the right constrains, and x dictionary that rpresnt a binary reprentaion to the matrix
    :param cost_matrix:cost matrix after manipulation
    :param group_size - a vectoer with how manny students in each group
    :param num_groups - int how many existing groups
    :param num_options- int how many options to split
    :return: solver object, dictinary
    '''
    solver = pywraplp.Solver.CreateSolver('SCIP')
    x = {}
    for i in range(num_groups):
        for j in range(num_options):
            x[i, j] = solver.IntVar(0, 1, '')

    # Each student need to be in exac one group
    for i in range(num_groups):
        solver.Add(solver.Sum([x[i, j] for j in range(num_options)]) == 1)

    # Each task is assigned not more then 8 people.
    for j in range(num_options):
        solver.Add(solver.Sum([group_size[i] * x[i, j] for i in range(num_groups)]) <= 8)

    # group number 1 (represnt as 0) will contain 7 people
    solver.Add(solver.Sum([group_size[i] * x[i, 4] for i in range(num_groups)]) == 7)

    objective_terms = []
    for i in range(num_groups):
        for j in range(num_options):
            objective_terms.append(cost_matrix[i][j] * x[i, j])

    solver.Minimize(solver.Sum(objective_terms))
    return solver, x


def print_resaults(solver, x, names, result, num_workers, num_tasks, size, new_index):
    final = []
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Total cost = ', solver.Objective().Value() / sum(size), '\n')
        for i in range(num_workers):
            for j in range(num_tasks):
                # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                if x[i, j].solution_value() > 0.5:
                    final.append([new_index[i] + 1, ", ".join(names[i]), j + 1, math.sqrt(result[i][j] ), size[i]])
                    print('Group %d, Group members : %s  ,Group size = %d, Maslul = %d, prefence = %d' %
                          (new_index[i] + 1, ", ".join(names[i]), size[i], j + 1, math.sqrt(result[i][j])))

    return final


def generate_file(results):
    '''
    generate a file out a the solver results
    :param results
    :return: df ['index', 'leader name', 'option' , 'the rank' ,'group size']
    '''
    df_to_save = pd.DataFrame(results, columns = ['index', 'name', 'unit' , 'prefernce' ,'size'])
    df_to_save.sort_values(by= ['index'], inplace = True)
    df_to_save.to_csv('assigments.csv',index=False  ,encoding='utf-8')
    return df_to_save

def raffle(cost_matrix , group_size , names):
    '''
    shaffle the entries to generate random resault in case of more then one optimaloption
    :param results
    :return: df ['index', 'leader name', 'option' , 'the rank' ,'group size']
    '''
    new_cost = []
    new_size = []
    new_names = []
    new_indesx = random.sample(range(0,len(group_size)), len(group_size))
    for item in new_indesx:
        new_cost.append(cost_matrix[item])
        new_size.append(group_size[item])
        new_names.append(names[item])
    return new_cost, new_size , new_names,  new_indesx

def extract_string(a_string):
    numbers = []
    for word in a_string.split():
        if word.isdigit():
            numbers.append(int(word))

    return numbers[0]

def filter_empty(tup):
    new_list  =  list(filter(lambda x: x != '', tup))
    return list(map(lambda x: str(x) ,new_list ))