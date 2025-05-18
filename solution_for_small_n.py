from functools import cache

MOD = 10**9 + 7
N = 10**6

primes = [1] * (N+1)
mobius = [1] * (N+1)

for i in range(2, N+1):
    if primes[i]:
        for j in range(i**2, N+1, i):
            primes[j] = 0
        for j in range(i, N+1, i):
            mobius[j] *= -1
        for j in range(i**2, N+1, i**2):
            mobius[j] = 0

invs = [None]
for i in range(1, N+1):
    invs.append(pow(i, -1, MOD))

H = [0] * (N+1) # sum of 1/i
for i in range(1, N+1):
    H[i] = (H[i-1] + invs[i]) % MOD

# sum of 1/ab for a+b <= n
@cache
def sab(n, H=H, mod=MOD, invs=invs):
    ret = 0
    for a in range(1, n):
        ret += invs[a] * H[n-a]
        ret %= mod
    return ret

# sum of 1/ab for a+b <=n, gcd(a, b) == 1
@cache
def copab(n, mod=MOD, mobius=mobius, invs=invs):
    ret = 0
    for g in range(1, n+1):
        ret += sab(n // g) * invs[g]**2 * mobius[g]
        ret %= mod
    return ret

# sum of 1/lcm(a, b) for a, b <= n
@cache
def pab(n, mod=MOD, invs=invs):
    ret = 0
    for g in range(1, n+1):
        ret += copab(n // g) * invs[g]
        ret %= mod
    return ret


# x, y <-> y, x
# 1, x <-> x, 0
def samecycle(n, mod=MOD, invs=invs):
    res = 0
    for clen in range(2, n+1):
        p = (clen-1) * pow(n*(n-1), -1, mod)
        p10 = pow(clen*(clen-1), -1, mod) if not clen % 2 else 0
        pp = p10 - invs[clen]
        res += p * pp
        res %= mod
    return (invs[2] + res) * invs[2], (invs[2] - res) * invs[2]

def diffcycle(n, mod=MOD, invs=invs, H=H):
    res = n*(n-1) * invs[4]
    v = pab(n) * invs[2]
    return (res - v) * invs[n]*invs[n-1], (res + v + n*(1 - H[n])) * invs[n]*invs[n-1]

def ends(n, mod=MOD):
    same = samecycle(n)
    diff = diffcycle(n)
    start = (same[0] + diff[0])
    start %= mod
    end = (same[1] + diff[1])
    end %= mod
    return start, end

def solve(n, mod=MOD):
    start, end = ends(n)
    diff = pow(n-2, -1, mod)*(end-start)
    ret = 0
    s = 0
    fact = 1
    for i in range(1, n):
        s += start + (i-1)*diff
        s %= mod
        fact = fact * i % mod
        ret += s * fact
        ret %= mod
    fact *= n
    ret += 1
    ret *= fact ** 2
    return ret % mod

print(solve(N))
