from collections import deque

R, C, K = map(int, input().split())
arr = [[0 for _ in range(C)] for __ in range(R+3)]

di, dj = [-1, 0, 1, 0], [0, 1, 0, -1]

def set_position(n, board, col):
    q = deque()
    q.append([1, col])
    l_c, r_c = 0, 0

    while q:
        ci, cj = q.popleft()

        # 아래로 내려갈 수 있음
        if 0 <= ci + 2 < R + 3 and 0 <= cj < C and board[ci + 2][cj] == 0 and board[ci + 1][cj + 1] == 0 and board[ci + 1][cj - 1] == 0:
            q.append([ci + 1, cj])
        else:
            # 왼쪽으로 내려갈 수 있음
            if 0 <= ci + 2 < R + 3 and 0 <= cj - 2 < C and board[ci][cj - 2] == 0 and board[ci - 1][cj - 1] == 0 and board[ci + 1][cj - 1] == 0 and board[ci + 1][cj - 2] == 0 and board[ci + 2][cj - 1] == 0:
                q.append([ci + 1, cj - 1])
                l_c += 1
            # 오른쪽으로 내려갈 수 있음
            elif 0 <= ci + 2 < R + 3 and 0 <= cj + 2 < C and board[ci][cj + 2] == 0 and board[ci - 1][cj + 1] == 0 and board[ci + 1][cj + 1] == 0 and board[ci + 1][cj + 2] == 0 and board[ci + 2][cj + 1] == 0:
                q.append([ci + 1, cj + 1])
                r_c += 1
            else:
                return [ci, cj], l_c, r_c

def bfs(board, x, y):
    q = deque()
    v = [[0] * len(board[0]) for _ in range(len(board))]
    v[x][y] = 1
    q.append([x, y])
    max_row = x

    while q:
        ci, cj = q.popleft()
        max_row = max(ci, max_row)

        for d in range(4):
            ni, nj = ci + di[d], cj + dj[d]
            if 0 <= ni < R + 3 and 0 <= nj < C and abs(board[ci][cj]) == abs(board[ni][nj]) and v[ni][nj] == 0 and board[ni][nj] != 0:
                q.append([ni, nj])
                v[ni][nj] = 1
            elif board[ci][cj] < 0 and 0 <= ni < R + 3 and 0 <= nj < C and v[ni][nj] == 0 and board[ni][nj] != 0:
                q.append([ni, nj])
                v[ni][nj] = 1

    return max_row

total = 0
for i in range(1, K+1):
    c, d = map(int, input().split())
    c, l, r = set_position(i, arr, c-1)
    rot = (d + (r-l))%4
    x, y = c[0], c[1]

    if x <= 3:
        arr = [[0 for _ in range(C)] for __ in range(R+3)]
    else:
        arr[x][y] = i
        arr[x + 1][y] = i
        arr[x - 1][y] = i
        arr[x][y + 1] = i
        arr[x][y - 1] = i
        arr[x + di[rot]][y + dj[rot]] = -i

        score = bfs(arr, x, y) - 2
        total += score

print(total)