import sys
from resource import *
import time
import psutil

def input(iPath):
    # Helper for generating strings
    def generate_str(lines):
        S = lines[0]
        for i in range(1, len(lines)):
            p = int(lines[i])
            S = S[: p + 1] + S + S[p + 1: ]
        return S
    # Read & Generate Strings
    with open(iPath, "r") as f:
        lines = [x.strip() for x in f.readlines()]
        mid = 1
        for i in range(1, len(lines)):
            if lines[i][0] in ['T', 'A', 'C', 'G']:
                mid = i
                break
        return generate_str(lines[: mid]), generate_str(lines[mid: ])
    return "", ""

def alpha(c1, c2):
    rev = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    alpha = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0],]
    return alpha[rev[c1]][rev[c2]]

def solve(S, T):
    theta = 30
    n, m = len(S), len(T)
    inf = (n + m + 5) * theta
    
    dp = [[inf for _ in range(m + 1)] for _ in range(n + 1)]
    ms = [[("", "") for _ in range(m + 1)] for _ in range(n + 1)]
    dp[0][0] = 0
    
    for i in range(n + 1):
        for j in range(m + 1):
            s, t = S[i - 1], T[j - 1]
            if i > 0 and dp[i][j] > dp[i - 1][j] + theta:
                dp[i][j] = dp[i - 1][j] + theta
                ms[i][j] = (ms[i - 1][j][0] + s, ms[i - 1][j][1] + '_')
            if j > 0 and dp[i][j] > dp[i][j - 1] + theta:
                dp[i][j] = dp[i][j - 1] + theta
                ms[i][j] = (ms[i][j - 1][0] + '_', ms[i][j - 1][1] + t)
            if i > 0 and j > 0 and dp[i][j] > dp[i - 1][j - 1] + alpha(s, t):
                dp[i][j] = dp[i - 1][j - 1] + alpha(s, t)
                ms[i][j] = (ms[i - 1][j - 1][0] + s, ms[i - 1][j - 1][1] + t)
        
    return dp[n][m], ms[n][m][0], ms[n][m][1]

def main(iPath):
    S, T = input(iPath)
    return solve(S, T)
    

if __name__ == "__main__": 
    process = psutil.Process()
    start_time = time.time()
    
    # Call algorithm 
    v, S, T = main(sys.argv[1])
    
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    memory_info = process.memory_info()
    memory_consumed = memory_info.rss / 1024
    
    # Output answer
    with open(sys.argv[2], "w") as f:
        f.write(str(v) + "\n")
        f.write(S + "\n")
        f.write(T + "\n")
        f.write(str(time_taken) + "\n")
        f.write(str(memory_consumed) + "\n")