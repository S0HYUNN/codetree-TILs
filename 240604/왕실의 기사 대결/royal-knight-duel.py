di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

N, M, Q = map(int, input().split())
arr = [[2] * (N+2)] + [[2] + list(map(int, input().split())) + [2] for _ in range(N)] + [[2] * (N+2)]
units = {}
init_k = [0] * (M+1)
for m in range(1, M+1):
    si, sj, h, w, k = map(int, input().split())
    units[m] = [si, sj, h, w, k]
    init_k[m] = k

def push_unit(start, dr):
    q = []
    pset = set()
    damage = [0] * (M+1)

    q.append(start)
    pset.add(start)

    while q:
        cur = q.pop(0)
        ci, cj, h, w, k = units[cur]
        ni, nj = ci + di[dr], cj + dj[dr]
        for i in range(ni, ni+h):
            for j in range(nj, nj+w):
                if arr[i][j] == 2:
                    return
                if arr[i][j] == 1:
                    damage[cur] += 1

        for idx in units:
            if idx in pset:
                continue

            ti, tj, th, tw, tk = units[idx]

            if ni <= ti+th-1 and ni+h-1 >= ti and tj <= nj+w-1 and nj <= tj+w-1:
                q.append(idx)
                pset.add(idx)

    damage[start] = 0

    for idx in pset:
        si, sj, h, w, k = units[idx]

        if k <= damage[idx]:
            units.pop(idx)
        else:
            ni, nj = si + di[dr], sj + dj[dr]
            units[idx] = [ni, nj, h, w, k-damage[idx]]

for _ in range(Q):
    idx, dr = map(int, input().split())
    if idx in units:
        push_unit(idx, dr)

ans = 0
for idx in units:
    ans += init_k[idx] - units[idx][4]
print(ans)