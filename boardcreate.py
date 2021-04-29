from PIL import Image, ImageDraw, ImageFont

def update(board):
    height = 575
    width = 575
    font = ImageFont.truetype("Comic Sans MS.ttf", 200)


    img = Image.new('RGBA', (width, height), (255, 0, 0, 0))

    draw = ImageDraw.Draw(img)

    cell_width =  width // 3
    cell_height = height // 3

    draw.line([(0,0), (width,0)], fill=(255,255,255,255), width = 10)
    draw.line([(0,0), (0,height)], fill=(255,255,255,255), width = 10)
    draw.line([(0,height-1), (width-1,height-1)], fill=(255,255,255,255), width = 10)
    draw.line([(width-1,0), (width-1,height-1)], fill=(255,255,255,255), width = 10)

    draw.line([(cell_width,0 + 10), (cell_width,height - 10)], width = 10, fill=(255,255,0,255))
    draw.line([(cell_width * 2,0 + 10), (cell_width * 2,height - 10)], width = 10, fill=(255,255,0,255))

    draw.line([(0 + 10, cell_height), (width - 10, cell_height)], width = 10, fill=(255,255,0,255))
    draw.line([(0 + 10 , cell_height * 2), (width - 10, cell_height * 2)], width = 10, fill=(255,255,0,255))

    for i in range(3):
        for j in range(3):
            if board[i][j] is not None:
                draw.text(((j * cell_width + cell_width // 2) , (i * cell_height + cell_height // 2)), board[i][j], fill=(255,140,0), anchor="mm", font=font)
    img.show()


def winner(i, board):
    height = 575
    width = 575
    font = ImageFont.truetype("Comic Sans MS.ttf", 200)

    img = Image.new('RGBA', (width, height), (255, 0, 0, 0))

    draw = ImageDraw.Draw(img)

    cell_width =  width // 3
    cell_height = height // 3

    draw.line([(0,0), (width,0)], fill=(255,255,255,255), width = 10)
    draw.line([(0,0), (0,height)], fill=(255,255,255,255), width = 10)
    draw.line([(0,height-1), (width-1,height-1)], fill=(255,255,255,255), width = 10)
    draw.line([(width-1,0), (width-1,height-1)], fill=(255,255,255,255), width = 10)

    draw.line([(cell_width,0 + 10), (cell_width,height - 10)], width = 10, fill=(255,255,0,255))
    draw.line([(cell_width * 2,0 + 10), (cell_width * 2,height - 10)], width = 10, fill=(255,255,0,255))

    draw.line([(0 + 10, cell_height), (width - 10, cell_height)], width = 10, fill=(255,255,0,255))
    draw.line([(0 + 10 , cell_height * 2), (width - 10, cell_height * 2)], width = 10, fill=(255,255,0,255))

    # for i in range(3):
    #     for j in range(3):
    #         if board[i][j] is not None:
    #             draw.text(((j * cell_width + cell_width // 2) , (i * cell_height + cell_height // 2)), board[i][j], fill=(255,140,0), anchor="mm", font=font)

    if i == 1:
       draw.multiline_text(((width//2) , (height // 2)), "X wins", fill=(255,140,0), anchor="mm", font=font) 
    if i == -1:
        draw.text(((width//2) , (height // 2)), "O wins", fill=(255,140,0), anchor="mm", font=font) 
    if i == 0:
        draw.text(((width//2) , (height // 2)), "Draw", fill=(255,140,0), anchor="mm", font=font) 
    
    img.show()