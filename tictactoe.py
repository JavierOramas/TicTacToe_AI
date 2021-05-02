import pygame
import math
# Initializing Pygame
pygame.init()

# Screen
WIDTH = 500
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("TicTacToe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("Images/x.png"), (150, 150))
O_IMAGE = pygame.transform.scale(pygame.image.load("Images/o.png"), (150, 150))

# Fonts
END_FONT = pygame.font.SysFont('courier', 40)


def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)


def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y, "", True)

    return game_array


def click(game_array):
    global x_turn, o_turn, images

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                # if x_turn:  # If it's X's turn
                images.append((x, y, X_IMAGE))
                game_array[i][j] = (x, y, 'x', False)
                return True
    return False                
    

def evaluate(game_array):
    for row in range(3):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            if game_array[row][0][2] == 'o':
                return 10
            elif game_array[row][0][2] == 'x':
                return -10
        
    for row in range(3):
        if (game_array[0][row][2] == game_array[1][row][2] == game_array[2][row][2]) and game_array[0][row][2] != "":
            if game_array[0][row][2] == 'o':
                return 10
            elif game_array[0][row][2] == 'x':
                return -10
        
        if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
            if game_array[0][0][2] == 'o':
                return 10
            elif game_array[0][0][2] == 'x':
                return -10

        if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
            if game_array[0][2][2] == 'o':
                return 10
            elif game_array[0][2][2] == 'x':
                return -10

    return 0

def Moves_Left(game_array):
    for i in range(3):
        for j in range(3):
            if game_array[i][j][2] == '':
                return True
    return False

def minimax(game_array, depth, is_max):
    score = evaluate(game_array)
    
    if score == 10 or score == -10:
        return score
    
    if not Moves_Left(game_array):
        return 0
    
    if is_max:
        best = 1000
        
        for i in range(3):
            for j in range(3):
                temp_tuple = game_array[i][j]
                if game_array[i][j][2] == '':
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'o', game_array[i][j][3])
                    
                    best = min(best, minimax(game_array, depth + 1, not is_max))
                    
                game_array[i][j] = temp_tuple
        
        return best
  
    else:    
        best = -1000
        
        for i in range(3):
            for j in range(3):
                temp_tuple = game_array[i][j]
                if game_array[i][j][2] == '':
                    game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'x', game_array[i][j][3])
                    
                    best = max(best, minimax(game_array, depth + 1, not is_max))
                    
                game_array[i][j] = temp_tuple
                
        return best

def play_ai(game_array):
    best_val = -1000
    best_move = (-1,-1)
    
    for i in range(3):
        for j in range(3):
            temp_tuple = game_array[i][j]
            if game_array[i][j][2] == '':
                game_array[i][j] = (game_array[i][j][0], game_array[i][j][1], 'o', game_array[i][j][3])
            
                move_val = minimax(game_array, 0, False)
            
                game_array[i][j] = temp_tuple
                
                if move_val > best_val:
                    best_move = (i,j)
                    best_val = move_val
        
    return best_move


# Checking if someone has won
def has_won(game_array):
    # print(game_array)
    # Checking rows
    for row in range(3):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            display_message(str(game_array[row][0][2]) + " has won!")
            return True
        if (game_array[0][row][2] == game_array[1][row][2] == game_array[2][row][2]) and game_array[0][row][2] != "":
            display_message(str(game_array[0][row][2]) + " has won!")
            return True
    
    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won!")
        return True

    # Checking reverse diagonal
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        display_message(game_array[0][2][2].upper() + " has won!")
        return True

    return False

def has_drawn(game_array):
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True


def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()


def main():
    global x_turn, o_turn, images, draw

    images = []
    draw = False

    run = True

    x_turn = True
    o_turn = False

    game_array = initialize_grid()
    
    render()
    
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if click(game_array):
                    
                    if has_won(game_array) or has_drawn(game_array):
                        run = False
                        continue
                        
                    if  Moves_Left(game_array):                 
                        ai_move = play_ai(game_array)
                        images.append((game_array[ai_move[0]][ai_move[1]][0], game_array[ai_move[0]][ai_move[1]][1], O_IMAGE))
                        game_array[ai_move[0]][ai_move[1]] = (game_array[ai_move[0]][ai_move[1]][0], game_array[ai_move[0]][ai_move[1]][1], 'o', False)

                    render()

                    if has_won(game_array) or has_drawn(game_array):
                        run = False
                        continue 

while True:
    if __name__ == '__main__':
        main()