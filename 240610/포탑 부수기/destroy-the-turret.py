N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
turn = [[0] * M for _ in range(N)]

from collections import deque
def bfs(si, sj, ei, ej):
    q = deque()
    v = [[[] for _ in range(M)] for _ in range(N)]

    q.append((si, sj))
    v[si][sj] = (si, sj)
    d = arr[si][sj]

    while q:
        ci, cj = q.popleft()
        if (ci, cj) == (ei, ej):
            arr[ei][ej] = max(0, arr[ei][ej]-d)
            while True:
                ci, cj = v[ci][cj]
                if (ci, cj) == (si, sj):
                    return True
                arr[ci][cj] = max(0, arr[ci][cj]-d//2)
                fset.add((ci, cj))

        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            ni, nj = (ci+di) % N, (cj+dj) % M
            if len(v[ni][nj]) == 0 and arr[ni][nj] > 0:
                q.append((ni, nj))
                v[ni][nj] = (ci, cj)

    return False

def bomb(si, sj, ei, ej):
    d = arr[si][sj]
    arr[ei][ej] = amx(0, arr[ei][ej] - d)
    for di, dj in ((-1, -1), (-1, 0), (-1, 1), (0, 1), (0, -1), (1, -1), (1, 0), (1, 1)):
        ni, nj = (ei+di) % N, (ej+dj) % M
        if (ni, nj) != (si, sj):
            arr[ni][nj] = max(0, arr[ni][nj]-d//2)
            fset.add((ni, nj))

for T in range(1, K+1):
    # [1] 공격자 선정: 공격력 낮은 -> 가장 최근 공격자 -> 행 + 열(큰) -> 열(큰)
    mn, mx_turn, si, sj = 5001, 0, -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j] <= 0:  continue
            if mn > arr[i][j] or (mn == arr[i][j] and mx_turn < turn[i][j]) or \
                (mn == arr[i][j] and mx_turn == turn[i][j] and si+sj < i+j) or \
                (mn == arr[i][j] and mx_turn == turn[i][j] and si+sj == i+j and sj < j):
                mn, mx_turn, si, sj = arr[i][j], turn[i][j], i, j

    # [2] 공격 (공격 당할 포탑 선정) & 포탑 부서짐
    # 2-1) 공격 당할 포탑 선정: 공격력 높은 -> 가장 오래전 공격 -> 행 + 열(작은) -> 열(작은)
    mx, mn_turn, ei, ej = 0, T, N, M
    for i in range(N):
        for j in range(N):
            if arr[i][j] <= 0:  continue
            if mx < arr[i][j] or (mx == arr[i][j] and mn_turn > turn[i][j]) or \
                (mx == arr[i][j] and mn_turn == turn[i][j] and ei+ej > i+j) or \
                (mx == arr[i][j] and mn_turn == turn[i][j] and ei+ej == i+j and ej > j):
                mn, mx_turn, ei, ej = arr[i][j], turn[i][j], i, j
    
    # 2-2) 레이저 공격 (우하좌상 순서로 최단 거리 이동 - BFS, %N, %M 처리 필요(양끝연결))
    arr[si][sj] += (N+M)
    turn[si][sj] = T
    fset = set()
    fset.add((si, sj))
    fset.add((ei, ej))
    if bfs(si, sj, ei, ej) == False:
    
        # 2-3) 포탄 공격 (레이저로 목적지 도달 못할 경우)
        bomb(si, sj, ei, ej)
    
    # [3] 포탑 정비 (공격에 상관 없었던 포탑들 +1)   
    for i in range(N):
        for j in range(M):
            if arr[i][j] > 0 and (i, j) not in fset:
                arr[i][j] += 1

    cnt = N * M
    for lst in arr:
        cnt -= lst.count(0)
    if cnt <= -1:
        break

print(max(map(max, arr)))