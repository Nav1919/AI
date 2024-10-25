import sys


all_blocks = {
    "I" : [((1,1,1,1), (0,0,0,0)), ((4,),(0,))],
    "O" : [((2,2), (0,0))],
    "T" : [((1,2,1), (0,0,0)), ((3,1), (0,-1)), ((1,2,1), (-1,0,-1)), ((1,3), (-1,0))],
    "S" : [((1,2,1), (0,0,-1)), ((2,2), (-1,0))],
    "Z" : [((1,2,1),(-1,0,0)), ((2,2),(0,-1))],
    "J" : [((2,1,1),(0,0,0)), ((3,1),(0,-2)), ((1,1,2),(-1,-1,0)), ((1,3),(0,0))],
    "L" : [((1,1,2),(0,0,0)), ((3,1),(0,0)), ((2,1,1),(0,-1,-1)), ((1,3),(-2,0))],
}

def drop_block( block, board, column ):
    block_width = len(block[0])
    col_distribution = [0 for i in range(block_width)]
    for i in range(column, column + block_width):
        col_height = 0
        while col_height < 20:
            if board[col_height][i] == "#":
                col_distribution[i-column] = 20 - col_height
                break
            else:
                col_height += 1

    for i in range(len(col_distribution)):
        col_distribution[i] += block[1][i]
    
    bottom_row = 20 - max(col_distribution) - 1
    
    for col in range(column, column + block_width):
        for vert_increment in range(0, block[0][col-column]):
            place = bottom_row - vert_increment + block[1][col-column]
            if place < 0:
                return "GAME OVER"
            board[place] = board[place][:col] + "#" + board[place][col+1:]
    
    return
            
def completed_rows( board ):
    countFilledRows = 0
    i = 19
    while i >= 0:
        if board[i].count("#") == 10:
            board.pop(i)
            board.insert(0, " "*10)
            countFilledRows += 1
        else:
            i -= 1
    if countFilledRows == 1:
        return 40
    elif countFilledRows == 2:
        return 100
    elif countFilledRows == 3:
        return 300
    elif countFilledRows == 4:
        return 1200
    return 0


input = sys.argv[1]

with open("tetrisout.txt", "a") as f:
    for block in all_blocks:
        for orientation in all_blocks[block]:
            for column in range(0, 10 - len(orientation[0]) + 1):
                board = [input[i*10:i*10+10] for i in range(0,20)]
                result = drop_block( orientation, board, column )
                if result == "GAME OVER":
                    f.write("GAME OVER\n")
                else:
                    score = completed_rows(board)
                    f.write(''.join(board) + "\n")       
    
    f.close()       