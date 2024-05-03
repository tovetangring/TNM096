import random

class Clause:

    def __init__(self, list1, list2 = None):
        if list2 == None:
            self.n = []
            self.p = []
            for i in list1:
                if i > 0 and i not in self.p:
                    self.p.append(i)
                elif i < 0 and -i not in self.n:
                    self.n.append(-i)
        else:
            self.n = list1
            self.p = list2
    
    def __bool__(self):
        for i in self.n:
            if i in self.p:
                return True
        return False
    
    def remove_duplicates(self):
        self.n = list(set(self.n))
        self.p = list(set(self.p))

    # Operator &, used for union
    def __and__(self, other):
        return Clause(self.n + other.n, self.p + other.p)

    # Operator -=
    def __isub__(self, other):
        if -other in self.n and other < 0:
            self.n.remove(-other)
        if other in self.p and other > 0:
            self.p.remove(other)
        return self
    
    # Operator <=
    def __le__(self, other):
        for i in self.n:
            if i not in other.n:
                return False
        for i in self.p:
            if i not in other.p:
                return False
        return True
    
    # Operator >=
    def __ge__(self, other):
        for i in other.n:
            if i not in self.n:
                return False
        for i in other.p:
            if i not in self.p:
                return False
        return True
    
    # Operator <
    def __lt__(self, other):
        return self <= other and self != other
    
    # Operator >
    def __gt__(self, other):
        return self >= other and self != other
        
    # Operator ==
    def __eq__(self, other):
        # Create sorted copies of the lists
        n1 = sorted(self.n)
        p1 = sorted(self.p)
        p2 = sorted(other.p)
        n2 = sorted(other.n)
        # Check if the lists are the same
        return n1 == n2 and p1 == p2
    
    def is_empty(self):
        return not self.n and not self.p
    
    def __str__(self):
        return f"{self.n}, {self.p}"
    
    def print_converter(self):
        def get_word(n):
            switcher = {
                1: "sun",
                2: "money",
                3: "ice",
                4: "movie",
                5: "cry"
            }
            return switcher.get(n, "Invalid number")

        output = ""
        for i in self.n:
            output += f"-{get_word(i)} "
        for i in self.p:
            output += f"{get_word(i)} "
        # Remove last space
        output = output[:-1]
        # Add ∨ between each word
        output = output.replace(" ", " ∨ ")
        print(output)
    

def intersect(a, b):
    return [i for i in a if i in b]

# TASK A.1: Given two clauses, returns their resolvent.
def resolution(A: Clause, B : Clause):
    # region A.p ∩ B.n = {} and A.n ∩ B.p = {}
    ApBn = intersect(A.p, B.n)
    AnBp = intersect(A.n, B.p)
         
    if not ApBn and not AnBp:
        return False
    # endregion

    # region (A.p ∩ B.n) ̸= {}
    if ApBn:
        a = random.choice(ApBn)
        A -= a
        B -= -a
    elif AnBp:
        a = random.choice(AnBp)
        A -= -a
        B -= a
    # endregion
        
    #C.p ← A.p ∪ B.p
    #C.n ← A.n ∪ B.n
    C = A & B

    # Check if C is a tautology
    if C:
        print("Tautology found")
        return False

    C.remove_duplicates()
    
    return C

def incorporate(S, kb):
    for A in S:
        kb = incorporate_clause(A, kb)
    return kb

def incorporate_clause(A, kb):
    for B in kb:
        if A <= B:
            return kb
    for B in kb:
        if A <= B:
            kb.remove(B)
    kb.append(A)
    return kb

def find_resolvents(kb):
    resolvents = []
    for A in kb:
        for B in kb:
            C = resolution(A, B)
            if C:
                resolvents.append(C)
    return resolvents

# TASK A.2: Given a knowledge base, returns a new knowledge base after applying the resolution rule.
def solver(kb):
    print("New iteration")
    kb = incorporate(kb, []) 
    while True:
        s = []
        kb_deriv = kb.copy()
        s = find_resolvents(kb)

        if not s:
            print("not S")
            return kb
        
        kb = incorporate(s, kb)

        if kb == kb_deriv:
            print("No new clauses were added")
            break



# Test
def test1():
    # Test for task 1:
    A, B, C, D, G, T, Z, F = 1, 3, 4, 7, 9, 16, 25, 29
    # Resolution
    print("Resolution")
    # Ex 1
    c1 = Clause([A, B, -C])
    c2 = Clause([C, B])
    print(resolution(c1,c2))

    # Ex 2
    c1 = Clause([A, B, -C])
    c2 = Clause([D, B, -G])
    print(resolution(c1,c2))

    # Ex 3
    c1 = Clause([-B, C, T])
    c2 = Clause([-C, Z, B])
    print(resolution(c1,c2))

    # Subsumption
    print("Subsumption")
    print(Clause([A, C]) < Clause([A, B, C]))
    print(Clause([B, -C]) < Clause([A, B, -C]))
    print(Clause([B, -F, -C]) < Clause([A, B, -C]))
    print(Clause([B]) < Clause([A, B, -C]))
    print(Clause([B, -C, A]) < Clause([A, B, -C]))

def test2():
    SUN, MONEY, ICE, MOVIE, CRY = 1, 2, 3, 4, 5

    # 1 & 2. Define the clauses for Bob
    # region Clauses
    # ¬sun ∨ ¬money ∨ ice
    # ¬money ∨ ice ∨ movie
    # ¬movie ∨ money
    # ¬movie ∨ ¬ice
    # sun ∨ money ∨ cry
    # endregion
    clauses = [
        Clause([-SUN, -MONEY, ICE]),
        Clause([-MONEY, ICE, MOVIE]),
        Clause([-MOVIE, MONEY]),
        Clause([-MOVIE, -ICE]),
        Clause([SUN, MONEY, CRY])
    ]

    for clause in clauses:
        clause.print_converter()
    print("===================")

    # 3. Run the solver
    KB = solver(clauses)

    for clause in KB:
        clause.print_converter()

# test1()
test2()
