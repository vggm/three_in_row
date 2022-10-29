import pygame as pg

# padding
PADDING = 120

# rows/cols
ROWS = COLS = 3

# screen size
SCREEN_HEIGHT = 720 + PADDING
SCREEN_WIDTH  = 720
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

# board size
BOARD_HEIGHT = 720
BOARD_WIDTH  = 720
BOARD_SIZE   = BOARD_WIDTH, BOARD_HEIGHT

# cell size
CELL_HEIGHT = BOARD_HEIGHT//ROWS
CELL_WIDTH  = BOARD_WIDTH//COLS
CELL_SIZE   = CELL_WIDTH, CELL_HEIGHT


def getImage(ruta):
  img = pg.image.load(ruta)
  return pg.transform.smoothscale(img, CELL_SIZE)
  
  
def winner_state():
  
  stack = set()
  # check rows
  for i in range(ROWS):
    for j in range(COLS):
      stack.add(board[i][j])
    
    if len(stack) == 1 and stack.pop() != -1:
      return True

    stack = set()  
  
  stack = set()
  # check col
  for i in range(COLS):
    for j in range(ROWS):
      stack.add(board[j][i])

    if len(stack) == 1 and stack.pop() != -1:
      return True

    stack = set()
    
  stack = set()
  # check diag
  for i in range(ROWS):
    stack.add(board[i][i])
    
  if len(stack) == 1 and stack.pop() != -1:
    return True
  
  stack = set()
  for i in range(ROWS):
    stack.add(board[i][COLS-i-1])
    
  if len(stack) == 1 and stack.pop() != -1:
    return True

  return False
    
  
  
SPRITES = {0: getImage('src/O.png'),
           1: getImage('src/X.png')}


# 0 <= x,y <= 3
def coordToReal(x,y):
  return (BOARD_WIDTH/COLS)*x, PADDING+(BOARD_WIDTH/ROWS)*y

# 0 <= x,y <= SCREEN_WIDTH,SCREEN_HEIGHT
def realToCoord(x,y):
  return int(x//CELL_HEIGHT), int((y-PADDING)//CELL_WIDTH)
    

if __name__ == '__main__':
  pg.init()
  pg.display.set_caption('ThreeInRow')
  
  clock = pg.time.Clock()
  window = pg.display.set_mode(SIZE, vsync=1)
  
  board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
  # print(board)
  
  # background image
  bg = pg.image.load('src/board2.png')
  bg = pg.transform.scale(bg, BOARD_SIZE)
  
  bigFont = pg.font.Font('src/jetbrains.ttf', 100)
  
  end = False
  quit_game = False
  turno = 1
  while not quit_game:
    for event in pg.event.get():
      match event.type:
        case pg.QUIT:
          quit_game
        case pg.KEYDOWN:
          if event.key == pg.K_ESCAPE:
            quit_game = True
          elif event.key == pg.K_r:
            board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
            end = False
            
            turno = 1 if turno == 0 else 0
            
        case pg.MOUSEBUTTONUP:
          mouseX, mouseY = pg.mouse.get_pos()
          if mouseY < PADDING:
            break
          
          coord = realToCoord(mouseX, mouseY)
          if board[coord[1]][coord[0]] != -1 or end:
            break
          
          board[coord[1]][coord[0]] = turno 
          # for row in board:
          #   print(row)
          turno = 1 if turno == 0 else 0
        
    window.fill(0x000000)
    window.blit(bg, (0,PADDING)) 
    
    for y in range(ROWS):
      for x in range(COLS):
        if board[y][x] == -1:
          continue
      
        window.blit(SPRITES[board[y][x]], coordToReal(x,y))
    
    
    if winner_state():
      winner = 'player1' if turno == 0 else 'player2'
      msg = bigFont.render(f'{winner} winss!!',True,0xFF0000)
      window.blit(msg, (0,0))
      end = True
    
    pg.display.flip()
    clock.tick(60)
  