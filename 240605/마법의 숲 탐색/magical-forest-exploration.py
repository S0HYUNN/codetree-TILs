import sys
from collections import deque

sys.setrecursionlimit(10000)

def init_map():
    global m
    m = [[-1] * C for _ in range(R)]

def drop(idx, ci, cj, e):
    global score, rMax

    while True:
        if ci == R - 2:
            break  # exit at bottom

        # go down
        if (ci == -2 and m[ci + 2][cj] == -1) or (m[ci + 2][cj] == -1 and m[ci + 1][cj - 1] == -1 and m[ci + 1][cj + 1] == -1):
            ci += 1
            continue

        # go left
        if cj >= 2:
            if (ci == -2 and m[ci + 2][cj - 1] == -1) or ((ci == -1) and m[ci + 2][cj - 1] == -1 and m[ci + 1][cj - 1] == -1 and m[ci + 1][cj - 2] == -1) or (m[ci + 2][cj - 1] == -1 and m[ci + 1][cj - 1] == -1 and m[ci + 1][cj - 2] == -1 and m[ci][cj - 2] == -1):
                ci += 1
                cj -= 1
                e = (e + 3) % 4
                continue

        # go right
        if cj < C - 2:
            if (ci == -2 and m[ci + 2][cj + 1] == -1) or ((ci == -1) and m[ci + 2][cj + 1] == -1 and m[ci + 1][cj + 1] == -1 and m[ci + 1][cj + 2] == -1) or (m[ci + 2][cj + 1] == -1 and m[ci + 1][cj + 1] == -1 and m[ci + 1][cj + 2] == -1 and m[ci][cj + 2] == -1):
                ci += 1
                cj += 1
                e = (e + 1) % 4
                continue

        # exit when cannot go anymore
        break

    # reset if golem located outside of the map
    if ci <= 0:
        init_map()
        return

    # mark golem on map
    m[ci][cj] = m[ci - 1][cj] = m[ci][cj + 1] = m[ci + 1][cj] = m[ci][cj - 1] = idx
    gArr[idx] = (ci, cj, e)

    move_golem(idx)
    score += rMax

def move_golem(idx):
    global rMax
    v[idx] = True  # visited

    # update rMax with the bottom of current golem
    ri = gArr[idx][0] + 2
    rMax = max(ri, rMax)

    # exit coord of current golem
    e = gArr[idx][2]
    ri = gArr[idx][0] + di[e]
    rj = gArr[idx][1] + dj[e]

    # find next golem close to current colem's exit
    for d in range(4):
        ni = ri + di[d]
        nj = rj + dj[d]

        if ni < 0 or ni >= R or nj < 0 or nj >= C:
            continue
        if m[ni][nj] == -1 or v[m[ni][nj]]:
            continue

        move_golem(m[ni][nj])

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    idx = 0
    
    R = int(data[idx])
    idx += 1
    C = int(data[idx])
    idx += 1
    K = int(data[idx])
    idx += 1
    
    score = 0
    init_map()
    gArr = [None] * K
    
    di = [-1, 0, 1, 0]
    dj = [0, 1, 0, -1]
    
    for k in range(K):
        c = int(data[idx]) - 1
        idx += 1
        e = int(data[idx])
        idx += 1
        
        # init every try
        rMax = 0
        v = [False] * K
        drop(k, -2, c, e)
    
    print(score)