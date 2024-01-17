def solve8Queen():
    col = set()
    posDiag = set()
    negDiag = set()

    res = []
    board = [["."]*8 for _ in range(8)]

    def backtrack(r):
        if r == 8:
            copy = ["".join(row) for row in board]
            res.append(copy)
            return

        for c in range(8):
            if c in col or (r+c) in posDiag or (r-c) in negDiag:
                continue

            col.add(c)
            posDiag.add(r+c)
            negDiag.add(r-c)
            board[r][c] = "Q"

            backtrack(r+1)

            col.remove(c)
            posDiag.remove(r+c)
            negDiag.remove(r-c)
            board[r][c] = "."

    backtrack(0)
    return res