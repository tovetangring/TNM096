# TASK A.1: Given two clauses, returns their resolvent.
def task1(c1, c2):
    resolvent = []

    for literal in c1:
        if literal not in c2 and -literal not in c2:
            resolvent.append(literal)

    for literal in c2:
        if literal not in c1 and -literal not in c1:
            resolvent.append(literal)

    return resolvent

# TASK A.2: Applies resolution mechanism to a given set of clauses.
def task2(clauses):
    new_clauses = list(clauses)

    while True:
        new_resolvents = []

        for i in range(len(new_clauses)):
            for j in range(i+1, len(new_clauses)):
                resolvent = task1(new_clauses[i], new_clauses[j])
                if not resolvent:
                    return True  # Empty clause found, contradiction
                if resolvent not in new_clauses and resolvent not in new_resolvents:
                    new_resolvents.append(resolvent)

        if not new_resolvents:
            return False  # No new resolvent can be derived

        new_clauses += new_resolvents


# Test
if __name__ == "__main__":
    # Test for task 1:
    c1 = [1, 4, 8]
    c2 = [1, 5, 6, 8]

    print(task1(c1,c2))

    # Test för task 2:
    clauses = [[1, 2, -3], [-1, 3], [-2, 3], [-3]]

    if task2(clauses):
        print("The formula is unsatisfiable because a contradiction was found.")
    else:
        print("The formula is satisfiable because no contradiction was found.")
