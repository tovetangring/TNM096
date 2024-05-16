import copy
import random

class Clauses:
    def __init__(self, p=None, n=None):
        self.p = p if p else set()
        self.n = n if n else set()

    def __eq__(self, other):
        return self.p == other.p and self.n == other.n

    def __hash__(self):
        p_hashable = frozenset(self.p) if isinstance(self.p, (set, list, tuple)) else self.p
        n_hashable = frozenset(self.n) if isinstance(self.n, (set, list, tuple)) else self.n
        return hash((p_hashable, n_hashable))

    def __str__(self):
        return f"[{self.p}, {self.n}]"

    def __repr__(self):
        listed = []
        for item in self.p:
            listed.append(item)
        for item in self.n:
            listed.append(-item)

        return f"{listed}"

    def __contains__(self, item):
        return item in self.p or item in self.n


                    


def Resolution(A_copy, B_copy):
    A = copy.deepcopy(A_copy)
    B = copy.deepcopy(B_copy)

    print('First A:', A)
    print('First B:', B)

    Ap_i_Bn = A.p.intersection(B.n)
    An_i_Bp = A.n.intersection(B.p)

    if not Ap_i_Bn and not An_i_Bp:
        return False
    
    if Ap_i_Bn:
        a = random.choice(list(Ap_i_Bn))
        A.p.remove(a)
        B.n.remove(a)
    else:
        a = random.choice(list(An_i_Bp))
        A.n.remove(a)
        B.p.remove(a)

    print('A:', A)
    print('B:', B)
    
    C = Clauses(B.p.union(A.p),A.n.union(B.n))

    if C.p.intersection(C.n):
        return False
 
    return C

def Incorporate(S, KB):
    for clause in copy.deepcopy(S):
        KB = Incorporate_Clause(clause, KB)
        #KB.add(tuple(clause))
    return KB

def Incorporate_Clause(A, KB):
    
    
    for B in copy.deepcopy(KB):
        if B.p.issubset(A.p) and B.n.issubset(A.n):
            return KB
    for B in copy.deepcopy(KB):
        if A.p.issubset(B.p) and A.n.issubset(B.n):
            KB.discard(B)

    
    KB = KB.union({A})
    return KB

def Solver(KB):
    K = set()
    KB = Incorporate(KB, K)
    k = 0
    while True:
        k +=1
        S = set()
        KB_list = list(KB)
        KB_old = copy.deepcopy(KB)
        for i in range(len(KB_list)-1):
            for j in range(i + 1, len(KB_list)):
                C = Resolution(KB_list[i], KB_list[j])
                if C :
                    S = S.union({C})
                    print(S)
        if not S:
            return KB
        KB = Incorporate(S, KB)
        if KB_old == KB:
            break
    return KB


# sun = 1
# money = 2
# ice = 3
# cry = 4
# movie = 5
task1 = set()
task1.add(Clauses({3},set((1,2))))
task1.add(Clauses({5,3},{2}))
task1.add(Clauses({2},{5}))
task1.add(Clauses({},set((5,3))))
task1.add(Clauses({5}, {}))
task1.add(Clauses({1,5,4}, {}))

task2 = set()
task2.add(Clauses({1,2,3}, {}))
task2.add(Clauses({1}, {3}))
task2.add(Clauses({1}, {2}))


# A -C
# A B C
# -B A


print('Start Set:', task1)
result = Solver(task1)
print('Final Knowledge Base:', result)


