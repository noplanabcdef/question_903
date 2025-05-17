import itertools
import math

def rank_permutation(perm):
    rank = 0
    n = len(perm)
    available = list(range(1, n + 1))
    for i in range(n):
        pos = available.index(perm[i])
        rank += pos * math.factorial(n - 1 - i)
        available.pop(pos)
    return rank + 1

def permutation_power(perm, power):
    n = len(perm)
    result = [0] * n
    for i in range(n):
        pos = i
        for _ in range(power):
            pos = perm[pos] - 1
        result[i] = pos + 1
    return tuple(result)

def compute_Q(n, mod=None):
    permutations = list(itertools.permutations(range(1, n + 1)))
    rank_map = {perm: rank_permutation(perm) for perm in permutations}
    total = 0
    for perm in permutations:
        seen = {}
        current = perm
        cycle_length = 0
        cycle_ranks = []
        while current not in seen:
            seen[current] = cycle_length
            cycle_ranks.append(rank_map[current])
            current = permutation_power(perm, len(seen))
            cycle_length += 1
        k = len(seen)
        sum_ranks = sum(cycle_ranks)
        contribution = (math.factorial(n) // k) * sum_ranks
        if mod is not None:
            contribution %= mod
        total += contribution
        if mod is not None:
            total %= mod
    return total

print(compute_Q(2))
print(compute_Q(3))
print(compute_Q(6, 10**9 + 7))
