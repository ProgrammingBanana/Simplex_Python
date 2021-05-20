import numpy as np

# Asegura que el print de floats tenga dos espacios decimales
np.set_printoptions(suppress=True, formatter={'float_kind': '{:0.2f}'.format})

# np.set_printoptions(sign=' ')

##################################################################
##                      MAXIMIZE CONST.                         ##
##################################################################

class Simplex:
    def __init__(self, variable_name = "X"):
        self.variable_name = variable_name
        print()
        self.get_basic_problem_info()
        print()
        self.get_equation_coeff()
        print()
        self.get_inequality_coeffs()
        print()
        self.get_inequality_constants()
        print()
        self.build_matrix()
        print()
        self.solve_matrix()
        self.print_results()


    def get_basic_problem_info(self):
        self.num_variables = int(input("Enter the amount of variables in the equation: "))
        self.num_equations = int(input("Enter the amount of innequalities: "))

        self.rows = self.num_equations+1
        self.cols = self.num_variables+self.rows+1


    def get_equation_coeff(self):
        self.equation_coeff = []
        for i in range(self.num_variables):
                while True:
                    try:
                        coeff = float(input("Enter value for X{} in the EQUATION (if not present, please write 0): ".format(i+1)))
                        if type(coeff) == float:
                            self.equation_coeff.append(coeff) 
                            break
                    except:
                        print("INPUT MUST BE A NUMBER")


    def get_inequality_coeffs(self):
        self.inequalities_coeffs = []
        for i in range(self.rows-1):
            print()
            coeff_list = []
            for j in range(self.num_variables):
                while True:
                    try:
                        coeff = float(input("Enter value for X{} in the INEQUALITY {} (if not present, please write 0): ".format(j+1, i+1)))
                        if type(coeff) == float: 
                            break
                    except:
                        print("INPUT MUST BE A NUMBER")
                    
                        
                coeff_list.append(coeff)

            self.inequalities_coeffs.append(coeff_list)
    

    def get_inequality_constants(self):
        self.constants_list = []
        for i in range(self.rows-1):
            while True:
                try:
                    constant = float(input("Enter value of the constant for INEQUALITY {}: ".format(i+1)))
                    if type(constant) == float:
                        self.constants_list.append(constant) 
                        break
                except:
                    print("INPUT MUST BE A NUMBER")


    def add_equation_coeff_to_matrix(self):
        for i in range(self.num_variables+1):
            if i == 0:
                self.matrix[(self.rows-1), i] = 1
            else:
                self.matrix[(self.rows-1), i] = (-1)*self.equation_coeff[(i-1)]


    def add_slack_variables(self):
        slack_row = 0
        slack_col = self.num_variables+1

        for i in range(self.rows-1):
            self.matrix[slack_row, slack_col] = 1
            slack_row += 1
            slack_col += 1
    

    def add_constants(self):
        for i in range(self.rows-1):
            self.matrix[i, -1] = self.constants_list[i]


    def add_inequality_coeff_to_matrix(self):
        for i in range(self.num_equations):
            for j in range(self.num_variables):
                self.matrix[i, j+1] = self.inequalities_coeffs[i][j]


    def build_matrix(self):
        self.matrix = np.zeros((self.rows, self.cols))

        self.add_equation_coeff_to_matrix()
        self.add_slack_variables()
        self.add_constants()
        self.add_inequality_coeff_to_matrix()
        
        self.print_matrix()
                

    def find_pivot_col(self):
        # arr = matrix[len(matrix)-1]
        minimum = 0
        min_indx = -1
        for col in range(1, self.cols-1):
            if self.matrix[-1, col] < minimum and col != self.cols-1:
                minimum = self.matrix[-1, col]
                min_indx = col

        self.pivot_col =  min_indx

    def find_pivot_row(self):
        # possible_rows = []
        minimum = np.inf
        min_indx = -1
        
        for i in range(self.rows-1):
            row_constant = self.matrix[i, -1]
            row_coeff = self.matrix[i, self.pivot_col]
            division = row_constant/row_coeff
            if row_constant >= 0 and row_coeff >= 0 and division < minimum:
                minimum = division
                min_indx = i

        self.pivot_row =  min_indx


    def solve_matrix(self):
        self.find_pivot_col()
        while(self.pivot_col != -1):
            self.find_pivot_row()

            self.matrix[self.pivot_row] = np.true_divide(self.matrix[self.pivot_row], self.matrix[self.pivot_row, self.pivot_col])

            for i in range(self.rows):
                if i != self.pivot_row:
                    self.matrix[i] = self.matrix[i] - (self.matrix[i, self.pivot_col] * self.matrix[self.pivot_row])

            self.find_pivot_col()

    def print_matrix(self):
        for i in range(self.cols):
            if i == 0:
                print("   P", end ="    ")
            elif i <= self.num_variables:
                print("{}{}".format(self.variable_name, i), end ="   ")
            elif i != self.cols-1:
                print("S{}".format(i-i+1), end ="    ")
            else:
                print("C")

        print(self.matrix)


    def print_results(self):
        print("###############################################")
        print("###               RESULTS                   ###")
        print("###############################################")
        self.print_matrix()
        print()
        print("Optimal Solution: ")
        solution = self.find_optimal_solution_values()
        for i in range(len(solution)):
            if i == 0:
                print("P = {}".format(solution[i]), end=", ")
            elif i != len(solution)-1:
                print("X{} = {}".format(i, solution[i]), end=", ")
            else:
                print("X{} = {}".format(i, solution[i]))

    def find_optimal_solution_values(self):
        optimal_values = []
        optimal_values.append(self.matrix[-1,-1])


        for col in range(1, self.num_variables+1):
            row = self.is_unit(col)
            if row != -1:
                optimal_values.append(self.matrix[row, -1])
            else:
                optimal_values.append(0)

        return optimal_values

    def is_unit(self, col):
        """ Verifies if the column is a unit column and if it is, it returns the row
            of the result. If it isnt it returns -1

        Args:
            col ([type]): [description]

        Returns:
            [type]: [description]
        """
        one_count = 0
        row = 0

        for i in range(self.rows):
            if self.matrix[i, col] == 1:
                one_count += 1
                row = i
        
        return row if one_count == 1 else -1


##################################################################
##                      MINIMIZE CONST.                         ##
##################################################################

class Min_Simplex(Simplex):
    
    def __init__(self):
        super().__init__("Y")


    def build_initial_matrix(self):
        initial_matrix = np.zeros((self.num_equations+1, self.num_variables+1))
        for i in range(self.num_equations+1):
            for j in range(self.num_variables+1):
                if i != self.num_equations:
                    if j != self.num_variables:
                        initial_matrix[i,j] = self.inequalities_coeffs[i][j]
                    else:
                        initial_matrix[i,j] = self.constants_list[i]
                else:
                    if j != self.num_variables:
                        initial_matrix[i,j] = self.equation_coeff[j]
                    else:
                        initial_matrix[i,j] = 0
        
        return initial_matrix

    def build_matrix(self):
        initial_matrix = self.build_initial_matrix()
        print("The Initial Matrix: ")
        print(initial_matrix)
        print()

        initial_matrix = initial_matrix.transpose()
        print("The Matrix After Transposing Value: ")
        print(initial_matrix)
        print()

        self.rows, self.cols = initial_matrix.shape
        self.num_variables = self.cols-1
        self.num_equations = self.rows-1

        # Taking into account the Z column and the slack variables
        self.cols += self.rows

        transposed_matrix = np.zeros((self.rows, self.cols))

        self.matrix = self.transfer_values(initial_matrix, transposed_matrix)
        self.add_slack_variables()
        
        print("Prepared Matrix: ")
        self.print_matrix()


    def transfer_values(self, initial_matrix, transposed_matrix):
        i_rows, i_cols = initial_matrix.shape
        for i in range(self.rows):
            for j in range(i_cols+1):
                if j == 0:
                    if i != self.rows-1:
                        transposed_matrix[i,0] = 0
                    else:
                        transposed_matrix[i,0] = 1
                elif j == i_cols:
                    transposed_matrix[i,-1] = initial_matrix[i,j-1]
                else:
                    if i == self.rows-1:
                        transposed_matrix[i,j] = (-1) * initial_matrix[i,j-1]
                    else:
                        transposed_matrix[i,j] = initial_matrix[i,j-1]

        return transposed_matrix


    def find_optimal_solution_values(self):
        optimal_values = []
        optimal_values.append(self.matrix[-1,-1])


        for col in range(self.num_variables+1, self.cols-1):
            optimal_values.append(self.matrix[-1, col])

        return optimal_values


##################################################################
##                        MIXED CONST.                          ##
##################################################################
"""
    1. When asking for inputs we, also ask if the inequality is in the form < or >
        - The standard form is <
    2. We append, the innequality number to a list, in order to know which inequalities to change the values of when creating the matrix
    3. Multiply all coefficients of that inequality by -1 (changing the sign)
    4. Make the tableu (matrix)
    5. Determine phase 1 or phase 2 (loop phase 1 until there are no negative values in the constants row)
        5_a) Phase 1:
            - Pivot row is the most negative row.
                + If the row has no negative values, the problem has no solution
            - For each column with a negative in the pivot row, find the ratio with the constant as the denominator, the largest value
                will determine the pivot column
            - apply the matrix operations to change the pivot row and all other rows (like the standard problems)
            - Once all constants (excluding the objective function) are non-negative apply, phase 2
        5_b) Phase 2:
            - If all constants in the constant rows are positive (except the objective function which doesnt matter)
                use simplex method for maximization
"""

class Mix_Simplex(Simplex):
    def __init__(self):
        super().__init__("X")


    def get_inequality_coeffs(self):
        """ Gets user input for inequality coefficients inequality signs
        """

        self.inequalities_coeffs = []
        self.sign_list = []

        for i in range(self.rows-1):
            print()
            coeff_list = []
            for j in range(self.num_variables):
                while True:
                    try:
                        coeff = float(input("Enter value for X{} in the INEQUALITY {} (if not present, please write 0): ".format(j+1, i+1)))
                        if type(coeff) == float: 
                            break
                    except:
                        print("INPUT MUST BE A NUMBER")
                coeff_list.append(coeff)

            self.inequalities_coeffs.append(coeff_list)

            while True:
                sign = input("Enter if inequality {} uses greater than or lesser than: ".format(i+1))
                if sign == ">":
                    self.sign_list.append(True)
                    break
                elif sign == "<":
                    self.sign_list.append(False)
                    break
                else:
                    print("INPUT MUST BE < OR >")

    def add_inequality_coeff_to_matrix(self):
        for i in range(self.num_equations):
            for j in range(self.num_variables):
                if self.sign_list[i]:
                    self.matrix[i, j+1] = (-1) * self.inequalities_coeffs[i][j]
                else:
                    self.matrix[i, j+1] = self.inequalities_coeffs[i][j]

    def add_constants(self):
        for i in range(self.rows-1):
            if self.sign_list[i]:
                self.matrix[i, -1] = (-1) * self.constants_list[i]
            else:
                self.matrix[i, -1] = self.constants_list[i]


    def find_pivot_row_phase_1(self):
        self.pivot_row = -1
        minimum = 0

        for i in range(self.rows-1):
            if self.matrix[i, -1] < minimum:
                minimum = self.matrix[i, -1]
                self.pivot_row = i



    def find_pivot_col_phase_1(self):
        self.pivot_col = -1
        greatest_ratio = 0.0

        denominator = self.matrix[self.pivot_row, -1]

        for i in range(self.cols-1):
            
            numerator = self.matrix[self.pivot_row, i]
            if numerator < 0.0:
                print(denominator)
                ratio = numerator/denominator
                if ratio > greatest_ratio:
                    greatest_ratio = ratio
                    self.pivot_col = i



    """
        You want to have an if that verifies if find_pivot_row_phase_1 returns -1
            - this means you go to phase 2
        You also want to have an if that verifies if find_pivot_col_phase_1 returns -1
            - this means there is no solution
    """


    def phase_1(self):
        self.find_pivot_row_phase_1()
        counter = 0
        while (self.pivot_row != -1 and counter <= 1):
            self.find_pivot_col_phase_1()

            if self.pivot_col == -1:
                print("THERE IS NO SOLUTION!")
                exit()

            self.matrix[self.pivot_row] = np.true_divide(self.matrix[self.pivot_row], self.matrix[self.pivot_row, self.pivot_col])+0

            for i in range(self.rows):
                if i != self.pivot_row:
                    self.matrix[i] = self.matrix[i] - (self.matrix[i, self.pivot_col]*self.matrix[self.pivot_row])+0

            self.find_pivot_row_phase_1()
            print(self.matrix)
            counter += 1

    
    def solve_matrix(self):
        self.phase_1()
        super().solve_matrix()


##################################################################
##                      MIN MIXED CONST.                        ##
##################################################################

class Min_Mix_Simplex(Mix_Simplex):
    def __init__(self):
        super().__init__()

    def get_equation_coeff(self):
        self.equation_coeff = []
        for i in range(self.num_variables):
                while True:
                    try:
                        coeff = float(input("Enter value for X{} in the EQUATION (if not present, please write 0): ".format(i+1)))
                        if type(coeff) == float:
                            self.equation_coeff.append((-1)*coeff) 
                            break
                    except:
                        print("INPUT MUST BE A NUMBER")


    def print_results(self):
        print("###############################################")
        print("###               RESULTS                   ###")
        print("###############################################")
        self.print_matrix()
        print()
        print("Optimal Solution: ")
        solution = self.find_optimal_solution_values()
        for i in range(len(solution)):
            if i == 0:
                print("P = {}".format((-1)*solution[i]), end=", ")
            elif i != len(solution)-1:
                print("X{} = {}".format(i, solution[i]), end=", ")
            else:
                print("X{} = {}".format(i, solution[i]))


def main():
    while True:
        print("SIMPLEX MENU:")
        print("1. Maximization Simplex")
        print("2. Minimization Simplex")
        print("3. Mixed Maximization Simplex")
        print("4. Mixed Minimization Simplex")
        print("5. EXIT")
        user_input = input("What simplex method do you wish to use?: ")
        if user_input == "1":
            simplex = Simplex()
        if user_input == "2":
            simplex = Min_Simplex()
        if user_input == "3":
            simplex = Mix_Simplex()
        if user_input == "4":
            simplex = Min_Mix_Simplex()
        if user_input == "5":
            print("Thank you for using this app")
            break

if __name__ == "__main__":
    main()



"""  
PROGRAM TESTED WITH THIS CALCULATOR:
https://cbom.atozmath.com/CBOM/Simplex.aspx?q=sm&q1=3%602%60MIN%60Z%60x1%2cx2%2cx3%60-2%2c4%2c-1%603%2c-6%2c4%3b2%2c-8%2c10%60%3c%3d%2c%3e%3d%6030%2c18%60%60D%60false%60true%60false%60true%60false%60false%60true&do=1#PrevPart
"""