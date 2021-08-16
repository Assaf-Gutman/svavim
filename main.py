from functions import *
import sys
from pathlib import Path
from tkinter import filedialog as fd
import os



__author__ = "Assaf Gutman"
__copyright__ =  "SuprNation LTD"
__version__ = "1.0.1"
__maintainer__ = "Assaf Gutman"
__email__ = "assaf@suprnation.com"
__status__ = "Production"



if __name__ == '__main__':
    # checking if a file path was given as a parameter
    if len(sys.argv) != 2:
        filename = fd.askopenfilename()
    else:
        filename = sys.argv[1]
    #check if the file is an excel file
    if filename == '' or not Path(filename).exists() or not filename.lower().endswith(('.xlsx', '.xlsm', '.xls' , '.csv')):
        print('Wrong File path')
        exit(1)

    # reading excel file and transform the data do 3 sets: names, cost ,and size of groups
    # filename = "
    cost_matrix , group_size , leader_names = create_data(filename ,os.path.splitext(filename)[1])
    # we randomly choosing the order of entries from the excel file, that in case of more then one optimal solution, the solution will be choosen randomly
    cost_matrix , group_size , leader_names ,shaffle_indexes= raffle(cost_matrix , group_size , leader_names)
    # create the nex cost matrix: Formula for current cost matrix -> x[i][j] = x[i][j] ^2 * group size[i]
    cost_matrix_after_mannipulation, num_groups, num_options = transform_cost(cost_matrix , group_size )
    # generae the solver object with the right constainers
    solver, x = generate_solver(cost_matrix_after_mannipulation,group_size ,num_groups, num_options)
    # solve the linear equaition and print resaults
    final_result = print_resaults(solver, x, leader_names, cost_matrix_after_mannipulation, num_groups, num_options, group_size , shaffle_indexes)
    # create csv file with the resault
    generate_file(final_result)


