N, M = map(int, input().split())
arr = [[1] * (N+2)] + [[1] + list(map(int, input().split())) + [1] for _ in range(N)] + [[1] * (N+2)]

basecamp = set()
for i in range(1, N+1):
    for j in range(1, N+1):
        if arr[i][j] == 1:
            basecamp.add((i, j))
            arr[i][j] = 0

store = {}
for m in range(1, M+1):
    i, j = map(int, input().split())
    store[m] = (i, j)

from collections import deque
def find(si, sj, dsets):
    q = deque()
    v = [[0] * (N+2) for _ in range(N+2)]
    tlst = []
    
    q.append((si, sj))
    v[si][sj] = 1
    
    while q:
        nq = deque()
        for ci, cj in q:
            if (ci, cj) in dsets:
                tlst.append((ci, cj))
            else:
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = ci+di, cj+dj
                    if v[ni][nj] == 0 and arr[ni][nj] == 0:
                        nq.append((ni, nj))
                        v[ni][nj] = v[ci][cj] + 1
                        
        if len(tlst) > 0:
            tlst.sort()
            return tlst[0]
        q = nq
        
    return -1

def solve():
    q = deque()
    time = 1
    arrived = [0]*(M+1)
    
    while q or time == 1:
        nq = deque()
        alst = []
        # [1] 모두 편의점 방향 최단거리 이동 (이번 time만, 같은 반경)
        for ci, cj, m in q:
            if arrived[m] == 0:
                ni, nj = find(store[m][0], store[m][1], set(((ci-1, cj), (ci+1,cj),(ci,cj-1),(ci,cj+1))))
                if (ni, nj) == store[m]:
                    arrived[m] = time
                    alst.append((ni, nj))
                else:
                    nq.append((ni, nj, m))
        q = nq

        # [2] 편의점 도착 거리 => arr[][] = 1 (이동 불가 처리)
        if len(alst) > 0:
            for ai, aj in alst:
                arr[ai][aj] = 1

        # [3] 시간 번호의 멤버가 베이스캠프로 순간 이동
        if time <= M:
            si, sj = store[time]
            ei, ej = find(si, sj, basecamp)
            basecamp.remove((ei, ej))
            arr[ei][ej] = 1
            q.append((ei, ej, time))
            
        time += 1
    return max(arrived)

ans = solve()
print(ans)