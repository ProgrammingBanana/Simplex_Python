import numpy as np

np.set_printoptions(suppress=True,
                    formatter={'float_kind': '{:0.2f}'.format})

# num_variables = int(input("Enter the amount of variables in the equation: "))
# num_equations = int(input("Enter the amount of innequalities: "))

# rows = num_equations+1
# cols = num_variables+rows+1


def form_max_matrix(rows, cols):
    num_equations = rows-1
    num_variables = cols-rows-1
    matrix = np.zeros((rows, cols))

    equation_coeff = list(map(float, input(
        "Enter the coefficients of the equation: ").split(" ")))

    for i in range(num_variables+1):
        if i == 0:
            matrix[(rows-1), i] = 1
        else:
            matrix[(rows-1), i] = (-1)*equation_coeff[(i-1)]

    for i in range(rows-1):
        inequeality_coeff = list(
            map(float, input("Enter the coefficients of the inequeality (if a variable is not present write 0): ").split(" ")))
        for j in range(len(inequeality_coeff)):
            matrix[i, j+1] = inequeality_coeff[(j)]

    slack_row = 0
    slack_col = num_variables+1

    for i in range(rows-1):
        matrix[slack_row, slack_col] = 1
        slack_row += 1
        slack_col += 1

    for i in range(rows-1):
        matrix[i, -1] = float(input("Input the inequality constants: "))

    return matrix


# matrix = form_max_matrix(rows, cols)
# test = matrix


def first_non_negative(rows):
    for i in range(len(rows)):
        if rows[i] >= 0:
            return i


def smallest_non_negative(rows):
    smallest_indx = first_non_negative(rows)
    smallest = rows[smallest_indx]

    for i in range(len(rows)):
        if smallest > rows[i] and rows[i] >= 0:
            smallest = rows[i]
            smallest_indx = i

    return smallest_indx


def find_most_negative(matrix):
    arr = matrix[len(matrix)-1]
    min = 0
    min_indx = -1
    for col in range(len(arr)):
        if arr[col] < min and col != len(arr)-1:
            min = arr[col]
            min_indx = col
    return min_indx


def find_pivot_row(matrix, indx):
    rows = []
    for i in range(len(matrix)-1):
        rows.append(matrix[i, -1]/matrix[i, indx])

    return smallest_non_negative(rows)


def solve_max(matrix):
    pivot_col = find_most_negative(matrix)
    while(pivot_col != -1):
        pivot_row = find_pivot_row(matrix, pivot_col)

        matrix[pivot_row] = np.true_divide(
            matrix[pivot_row], matrix[pivot_row, pivot_col])

        for i in range(len(matrix)):
            if i != pivot_row:
                matrix[i] = matrix[i] - \
                    (matrix[i, pivot_col]*matrix[pivot_row])

        pivot_col = find_most_negative(matrix)

    return matrix

# print(matrix)

##################################################################
##                        Minimization                          ##
##################################################################


def form_min_matrix():
    num_variables = int(
        input("Enter the amount of variables in the equation: "))
    num_equations = int(input("Enter the amount of innequalities: "))

    rows = num_equations+1
    cols = num_variables+1

    matrix = np.zeros((rows, cols))

    equation_coeff = list(map(float, input(
        "Enter the coefficients of the equation: ").split(" ")))

    for i in range(num_variables):
        matrix[(rows-1), i] = equation_coeff[i]

    for i in range(rows-1):
        inequeality_coeff = list(
            map(float, input("Enter the coefficients of the inequeality (if a variable is not present write 0): ").split(" ")))
        inequeality_coeff.append(
            float(input("Input the inequality constants: ")))
        matrix[i] = np.array([inequeality_coeff])

    matrix = matrix.transpose()
    rows, cols = matrix.shape

    t_matrix_rows = rows
    t_matrix_cols = cols+rows

    t_matrix = np.zeros((t_matrix_rows, t_matrix_cols))

    for i in range(t_matrix_rows):
        for j in range(cols):
            if j == cols-1:
                t_matrix[i, -1] = matrix[i, j]
            else:
                if i == t_matrix_rows-1:
                    t_matrix[i, j+1] = (-1)*matrix[i, j]
                else:
                    t_matrix[i, j+1] = matrix[i, j]

    t_matrix[-1, 0] = 1

    slack_row = 0
    slack_col = cols

    for i in range(t_matrix_rows-1):
        t_matrix[slack_row, slack_col] = 1
        slack_row += 1
        slack_col += 1

    return t_matrix


def solve_min(matrix):
    pivot_col = find_most_negative(matrix)
    while(pivot_col != -1):
        pivot_row = find_pivot_row(matrix, pivot_col)

        matrix[pivot_row] = np.true_divide(
            matrix[pivot_row], matrix[pivot_row, pivot_col])

        for i in range(len(matrix)):
            if i != pivot_row:
                matrix[i] = matrix[i] - \
                    (matrix[i, pivot_col]*matrix[pivot_row])

        pivot_col = find_most_negative(matrix)
    return matrix


def minimization():
    matrix = form_min_matrix()
    matrix = solve_min(matrix)
    print(matrix)


minimization()

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


def find_pivot_row_phase_1(matrix):
    min_row = -1
    min = 0

    for i in range(np.size(matrix, 0)-1):
        if matrix[i, -1] < min:
            min = matrix[i, -1]
            min_row = i
    return min_row


def find_pivot_col_phase_1(matrix, row):
    col = -1
    greatest_ratio = 0.0

    denominator = matrix[row, -1]

    for i in range(np.size(matrix, 1)-1):
        numerator = matrix[row, i]
        if numerator < 0:
            ratio = numerator/denominator
            if ratio > greatest_ratio:
                greatest_ratio = ratio
                col = i
    return col


"""
    You want to have an if that verifies if find_pivot_row_phase_1 returns -1
        - this means you go to phase 2
    You also want to have an if that verifies if find_pivot_col_phase_1 returns -1
        - this means there is no solution
"""


def phase_1(matrix):
    pivot_row = find_pivot_row_phase_1(matrix)
    while (pivot_row != -1):
        pivot_col = find_pivot_col_phase_1(matrix, pivot_row)

        if pivot_col == -1:
            print("THERE IS NO SOLUTION!")
            exit()

        matrix[pivot_row] = np.true_divide(
            matrix[pivot_row], matrix[pivot_row, pivot_col])+0

        for i in range(len(matrix)):
            if i != pivot_row:
                matrix[i] = matrix[i] - \
                    (matrix[i, pivot_col]*matrix[pivot_row])+0

        pivot_row = find_pivot_row_phase_1(matrix)

    return matrix


matrix = np.array([[0, -1, -1, 1, 0, 0, -7], [0, 9, 5, 0, 1, 0, 45],
                  [0, -2, -1, 0, 0, 1, -8], [1, -20, -15, 0, 0, 0, 0]]).astype(float)


# TODO create this functions

"""
    Funciono para:

        Z = 20x1 + 15x2

        x1 + x2 >= 7
        9x1 + 5x2 <= 45
        2x1 + x2 >= 8
        
        [[0.00 -1.00 -1.00 1.00 0.00 0.00 -7.00]
        [0.00 9.00 5.00 0.00 1.00 0.00 45.00]
        [0.00 -2.00 -1.00 0.00 0.00 1.00 -8.00]
        [1.00 -20.00 -15.00 0.00 0.00 0.00 0.00]]

"""


def form_max_mix_matrix():
    """
        Get user input and form matrix with all slack variables.
    """
    num_variables = int(
        input("Enter the amount of variables in the equation: "))
    num_equations = int(
        input("Enter the amount of innequalities: "))

    sign_list = []

    rows = num_equations+1
    cols = num_variables+rows+1

    matrix = np.zeros((rows, cols))

    equation_coeff = list(
        map(float, input("Enter the coefficients of the equation: ").split(" ")))

    for i in range(num_variables+1):
        if i == 0:
            matrix[(rows-1), i] = 1
        else:
            matrix[(rows-1), i] = (-1)*equation_coeff[(i-1)]

    for i in range(rows-1):
        inequeality_coeff = list(
            map(float, input("Enter the coefficients of the inequeality (if a variable is not present write 0): ").split(" ")))

        sign = input("Enter if it's greater than or lesser than: ")
        if sign == ">":
            sign_list.append(True)
        else:
            sign_list.append(False)

        for j in range(len(inequeality_coeff)):
            if sign_list[i]:
                matrix[i, j+1] = (-1)*inequeality_coeff[(j)]
            else:
                matrix[i, j+1] = inequeality_coeff[(j)]

    slack_row = 0
    slack_col = num_variables+1

    for i in range(rows-1):
        matrix[slack_row, slack_col] = 1
        slack_row += 1
        slack_col += 1

    for i in range(rows-1):
        if sign_list[i]:
            #  The \ just means the thing goes on the next line.
            matrix[i, -1] = (-1) * \
                float(input("Input the inequality constants: "))
        else:
            matrix[i, -1] = float(input("Input the inequality constants: "))

    return matrix


def max_mix():
    """
        Runs all necessary functions
    """
    matrix = form_max_mix_matrix()
    matrix = phase_1(matrix)
    matrix = solve_max(matrix)
    print(matrix)


# matrix = phase_1(matrix)
# matrix = solve_max(matrix)
# print(matrix)
##################################################################
##                        MIN MIXED CONST.                      ##
##################################################################
"""
    1. Multiply objective function for minimization by -1
    2. Apply Simplex method for Maximization with mixed constraints
    3. Result of the objective function MUST be multiplied by -1 at the end of the process
"""

# TODO create these functions

"""
    Funciono para:

        Z = 20x1 + 15x2

        x1 + x2 >= 7
        9x1 + 5x2 <= 45
        2x1 + x2 >= 8
        
        [[0.00 -1.00 -1.00 1.00 0.00 0.00 -7.00]
        [0.00 9.00 5.00 0.00 1.00 0.00 45.00]
        [0.00 -2.00 -1.00 0.00 0.00 1.00 -8.00]
        [1.00 20.00 15.00 0.00 0.00 0.00 0.00]]

"""


def form_min_mix_matrix():
    """
        Get user input and form matrix with all slack variables.
    """
    num_variables = int(
        input("Enter the amount of variables in the equation: "))
    num_equations = int(
        input("Enter the amount of innequalities: "))

    sign_list = []

    rows = num_equations+1
    cols = num_variables+rows+1

    matrix = np.zeros((rows, cols))

    equation_coeff = list(
        map(float, input("Enter the coefficients of the equation: ").split(" ")))

    for i in range(num_variables+1):
        if i == 0:
            matrix[(rows-1), i] = 1
        else:
            """
                Cuando uno mueve los coeficientes para la izq de la ecuacion,
                se multiplican por -1.  Como en este caso se supone que se multiplique por -1,
                por ser minimizacion mixta,se cancelan el -1 original y el -1 por el cual se multiplicaria.
                Esto deja los coeficientes iguales a como los entraron.  Para evitar confusion y condicionales
                adicionales, no invertimos el primer coeficiente.
            """
            matrix[(rows-1), i] = equation_coeff[(i-1)]

    for i in range(rows-1):
        inequeality_coeff = list(
            map(float, input("Enter the coefficients of the inequeality (if a variable is not present write 0): ").split(" ")))

        sign = input("Enter if it's greater than or lesser than: ")
        if sign == ">":
            sign_list.append(True)
        else:
            sign_list.append(False)

        for j in range(len(inequeality_coeff)):
            if sign_list[i]:
                matrix[i, j+1] = (-1)*inequeality_coeff[(j)]
            else:
                matrix[i, j+1] = inequeality_coeff[(j)]

    slack_row = 0
    slack_col = num_variables+1

    for i in range(rows-1):
        matrix[slack_row, slack_col] = 1
        slack_row += 1
        slack_col += 1

    for i in range(rows-1):
        if sign_list[i]:
            #  The \ just means the thing goes on the next line.
            matrix[i, -1] = (-1) * float(input("Input the inequality constants: "))
        else:
            matrix[i, -1] = float(input("Input the inequality constants: "))

    return matrix


def min_mix():
    """
        Runs all necessary functions 
    """

    matrix = form_min_mix_matrix()
    matrix = phase_1(matrix)
    matrix = solve_max(matrix)
    print(matrix)


# max_mix()
