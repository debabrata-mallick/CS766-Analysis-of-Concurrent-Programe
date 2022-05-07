import sys
import itertools

def inputProgram():
    """

    :return:
    statements:- This is a list of lists where each list has the instructions of a program, hence consist all the programs
    including the initialisation of the global variable as the default program.

    assert_cond_stat:- This is the string having assert condition only.
    """
    print("Provide number of processes:")
    n = int(input())
    if(n<1 or n>10):
        print("Value of n should be between 1 and 10 inclusive.")
        sys.exit()
    programs = [None] * (n + 1)
    programs[0] = "x=0;y=0;z=0;"

    for i in range(1, n + 1):
        print("Type the program " + "P" + str(i))
        programs[i] = input()

    print("Is there any assertion statement, if yes type 1 else 0")

    assert_cond_stat = None
    if (int(input()) == 1):
        print("Type assertion conditional statement:")
        assert_cond_stat = input()
        assert_cond_stat = assert_cond_stat.replace("assert","")

    else:
        assert_cond_stat = None

    statements = []
    for program in programs:
        temp = program.split(';')
        temp = temp[:-1]
        if(len(temp) > 4):
            print("Maximum number of instructions in the program cannot be more than four.")
            sys.exit()
        statements.append(temp)

    return statements, assert_cond_stat

def modifyInput(statements):
    """

    :param statements: This is a list of lists where each list has the instructions of a program.

    :return:
    statements:- This is a list of lists where each list has the instructions of a program but the simple instruction is
    modified in a manner which is easy for the program to identify read and write operations.

    all_variables_dict:- This is a dictionary having all the variables(global and local) and the value initialised to 0.

    """
    all_variables_dict = {}
    for i in range(len(statements)):
        statement = statements[i]
        for j in range(len(statement)):
            expression = statement[j]
            temp = expression.split("=")
            left = temp[0]
            right = temp[-1]

            if left not in all_variables_dict:
                all_variables_dict[left] = 0

            if(left == 'x' or left == 'y' or left == 'z'):
                statements[i][j] = str(i)+' ' + 'w' + ' ' +left+' '+right
            else:
                statements[i][j] = str(i) +' '+ 'r' +' '+ right+' '+left
    return statements,all_variables_dict


def combine(lst1,lst2):
    """

    :param lst1: A list having instructions of a program in the same order as provided in input.
    :param lst2: Another list having instructions of a program in the same order as provided in input.

    :return:
    comb_results:- This is a list of lists having all the inter-mixing possible of the instructions of programs which are
    in the two lists, keeping the order of instructions of both program maintained.
    """
    comb_results = []
    for locations in itertools.combinations(range(len(lst1) + len(lst2)), len(lst2)):
        result = lst1[:]
        for location, element in zip(locations, lst2):
            result.insert(location, element)
        comb_results.append(result)
    return comb_results



def permStatements(statements):
    """

    :param statements: This is a list of lists where each list has the instructions of a program.

    :return:
    perm_of_statements:- This is a list of list having all the inter-mixing of instructions of 'n' programs, keeping the
    order of instructions of a single program maintained.
    """
    if (len(statements) == 1):
        perm_of_statements = statements
    else:
        lst1 = statements[0]
        lst2 = statements[1]
        temp1 = combine(lst1, lst2)

        for i in range(2, len(statements)):
            temp2 = []
            for t in temp1:
                for x in combine(t, statements[i]):
                    temp2.append(x)

            temp1 = temp2.copy()

        perm_of_statements = temp1

    return perm_of_statements



def convertExpressionToOrg(expression):
    """

    :param expression: This is a string having instruction in modified form.

    :return:
    final_expression:- Instruction in normal form as provided by the user.
    """
    temp = expression.split(" ")
    process_no = temp[0]
    op = temp[1]
    variable = temp[2]
    value = temp[3]

    final_expression  = ""
    if(op == 'w'):
        final_expression = final_expression + variable+" = "+value
    if(op == 'r'):
        final_expression = final_expression + value + " = "+ variable

    return final_expression


def get_index(op,variable,perm_of_statement):
    """

    :param op: character referring to operation, 'w' means write and 'r' means read.
    :param variable: variable in consideration, such as 'x', 'y' , 'z'.
    :param perm_of_statement: This is a list, having one possible interleaving of instructions of the programs.

    :return:
    indices(list):- indices of all the instruction which are performing the operation as provided in parameter "op"
    to the variable provided in the parameter "variable".
    """
    indices = []
    for i in range(len(perm_of_statement)):
        temp = perm_of_statement[i].split(" ")
        if(temp[1]==op and temp[2]==variable):
            indices.append(i)
    return indices

def getRF(perm_of_statement):
    """

    :param perm_of_statement:This is a list, having one possible interleaving of instructions of the programs.

    :return:
    rf:- This is a list of list containing all the read-from realtions
    between a write instruction and a read instruction on the same variable.
    """
    rf = []
    for var in ['x','y','z']:
        w_var_indices  = get_index('w',var, perm_of_statement)
        r_var_indices = get_index('r', var, perm_of_statement)

        for r_var_index in r_var_indices:
            w_var_index = None
            for i in range(len(w_var_indices)-1,-1,-1):
                if(w_var_indices[i]<r_var_index):
                    w_var_index = w_var_indices[i]
                    break
            if(w_var_index != None):
                rf.append([convertExpressionToOrg(perm_of_statement[w_var_index]),convertExpressionToOrg(perm_of_statement[r_var_index])])
            else:
                rf.append([var+' = '+'0', convertExpressionToOrg(perm_of_statement[r_var_index])])

    return rf




def getWS(perm_of_statement):
    """

    :param perm_of_statement: This is a list, having one possible interleaving of instructions of the programs.

    :return:
    ws:- This is a list of list containing all the write serialization between two write instruction on the same variable.
    """
    ws = []

    for var in ['x','y','z']:
        w_var_indices = get_index('w',var, perm_of_statement)
        if(len(w_var_indices) <= 1):
            continue
        for i in range(len(w_var_indices)-1):
            ws.append([convertExpressionToOrg(perm_of_statement[w_var_indices[i]]),convertExpressionToOrg(perm_of_statement[w_var_indices[i+1]])])

    return ws

def getTrace(perm_of_statement):
    """

    :param perm_of_statement: This is a list, having one possible interleaving of instructions of the programs.

    :return:
    trace:- This is a list of instructions in an order, which is considered as a possible trace.
    """
    trace = []
    for expression in perm_of_statement:
        trace.append(convertExpressionToOrg(expression))
    return trace

def output(traces, rfs, wss):
    """
     This is to print final valid traces.

    :param traces: This is a list of instructions in an order, which is considered as a possible trace.
    :param rfs: List of lists containing all the read from relations.
    :param wss: List of lists containing all write serializations.
    """
    num_of_traces = len(traces)
    print("No. of traces = "+str(num_of_traces))
    for i in range(num_of_traces):
        print("{}-: Trace: {}, rf relation: {}, co relation: {}".format(i+1,traces[i],rfs[i],wss[i]))

def assertViolateOutput(trace,rf,ws):
    """
    This is to print Violating Trace.

    :param traces: This is a list of instructions in an order, which is considered as a possible trace.
    :param rfs: List of lists containing all the read from relations.
    :param wss: List of lists containing all write serializations.
    """
    print("Error: Assertion Violation")
    print("Violating Trace: {}, rf relation: {}, co relation: {}".format(trace, rf, ws))

def checkAssert(perm_of_statement,all_variables_dict,assert_cond_stat):
    """

    :param perm_of_statement: This is a list, having one possible interleaving of instructions of the programs.
    :param all_variables_dict: This is a dictionary having all the variables(global and local) and the value initialised to 0.
    :param assert_cond_stat: This is the string having assert condition only.

    :return:
    flag:- Boolean variable represent whether the assertion condition holds or not on the 'perm of statement'.
    """
    for expression in perm_of_statement:
        temp = expression.split(" ")
        op = temp[1]
        variable = temp[2]
        value = temp[3]
        if(op == 'w'):
            all_variables_dict[variable] = int(value)
        if(op=='r'):
            all_variables_dict[value] = all_variables_dict[variable]

    variables = all_variables_dict.keys()
    for variable in variables:
        newvariable = "all_variables_dict['{}']".format(str(variable))
        assert_cond_stat = assert_cond_stat.replace(variable, newvariable)

    flag = eval(assert_cond_stat)

    return flag

def main():
    """
     Main function, execution starts from here.
    """
    statements, assert_cond_stat = inputProgram()
    statements, all_variables_dict = modifyInput(statements)
    initial_stat = statements[0]
    statements = statements[1:]
    perm_of_statements = permStatements(statements)

    traces = []
    rfs = []
    wss = []
    rfs_wss = []

    for perm_of_statement in perm_of_statements:
        trace = None
        rf = None
        ws = None
        trace = getTrace(perm_of_statement)
        rf = getRF(perm_of_statement)
        rf.sort()
        ws = getWS(perm_of_statement)

        if(assert_cond_stat != None):
            flag  = checkAssert(perm_of_statement,all_variables_dict,assert_cond_stat)
            if(not flag):
                assertViolateOutput(trace,rf,ws)
                sys.exit()

        temp = rf+ws
        if(temp in rfs_wss):
            continue

        traces.append(trace)
        rfs.append(rf)
        wss.append(ws)
        rfs_wss.append(temp)

    output(traces,rfs,wss)


if __name__ == '__main__':
    main()
