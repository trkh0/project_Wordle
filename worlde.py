from random import randint
import time
import pygame

clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('bahnschrift', 40)
PLAY_FONT = pygame.font.SysFont('bahnschrift', 20)

BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREY = (128,128,128)
DARKGREY = (90, 90, 90)
GREEN = (128, 128, 0)
YELLOW = (255, 255, 120)

#game states
RUNNING  = 1
MAIN_MENU = 2
LOST = 3
WIN = 4

FPS = 60

WIDTH = 800
HEIGHT = 600
TILE_WIDTH = 50
TILE_HEIGHT = 50
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))

class Tile:
    def __init__(self, rect, color = BLACK, status = 0):
        self.rect = rect
        self.color = color
        self.status = status
        self.surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        self.surface.fill(self.color)
        self.text = ''
        self.found = 0



def defTiles(tiles):
    tiles = [[],[],[],[],[],[]]
    for j in range(6):
        for i in range(5):
            tileRect = pygame.Rect(WIDTH//2 - 3 * TILE_WIDTH + 5 + i * 60, HEIGHT//2 - 3 * TILE_HEIGHT + 30 + j * 60 , TILE_WIDTH, TILE_HEIGHT)
            tiles[j].append(Tile(tileRect, GREY))
    tiles[0][0].status = 1
    activeTile = 0
    return tiles
        

def update(tiles, sub):
    WINDOW.fill(WHITE)
    timer = FONT.render(str(sub), 1, BLACK)
    WINDOW.blit(timer, (WIDTH//2 - timer.get_width()//2, 80))
    for tileLine in tiles:
        for tile in tileLine:
            if tile.status == 1:
                tile.surface.fill(BLACK)
            elif tile.status == 0:
                tile.surface.fill(GREY)
            elif tile.status == 2:
                tile.surface.fill(DARKGREY)
            elif tile.status == 3:
                tile.surface.fill(GREEN)
            elif tile.status == 4:
                tile.surface.fill(YELLOW)
            content = FONT.render(tile.text, 1, WHITE)
            tile.surface.blit(content, (TILE_WIDTH // 2 - content.get_width()//2, TILE_HEIGHT//2 - content.get_height()//2))
            WINDOW.blit(tile.surface, tile.rect)
    pygame.display.update()

def update_main(playButton):
    WINDOW.fill(WHITE)
    title = FONT.render("WORDLE", 1, BLACK)
    WINDOW.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    playButton_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
    playButton_surface.fill(RED)
    play_text = PLAY_FONT.render("PLAY!", 1, WHITE)
    playButton_surface.blit(play_text, (BUTTON_WIDTH//2 - play_text.get_width()//2, BUTTON_HEIGHT//2 - play_text.get_height()//2))
    WINDOW.blit(playButton_surface, playButton)
    pygame.display.update()

def update_lost(menuButton, solution):
    WINDOW.fill(WHITE)
    title = FONT.render("YOU LOST!", 1, BLACK)
    word = FONT.render("SOLUTION WAS: " + str(solution), 1, BLACK)
    WINDOW.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    WINDOW.blit(word, (WIDTH//2 - word.get_width()//2, 150))
    menuButton_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
    menuButton_surface.fill(RED)
    menu_text = PLAY_FONT.render("MENU", 1, WHITE)
    menuButton_surface.blit(menu_text, (BUTTON_WIDTH//2 - menu_text.get_width()//2, BUTTON_HEIGHT//2 - menu_text.get_height()//2))
    WINDOW.blit(menuButton_surface, menuButton)
    pygame.display.update()

def update_win(menuButton, solution):
    WINDOW.fill(WHITE)
    title = FONT.render("YOU WON!", 1, BLACK)
    word = FONT.render("SOLUTION WAS: " + str(solution), 1, BLACK)
    WINDOW.blit(title, (WIDTH//2 - title.get_width()//2, 80))
    WINDOW.blit(word, (WIDTH//2 - word.get_width()//2, 150))
    menuButton_surface = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT))
    menuButton_surface.fill(RED)
    menu_text = PLAY_FONT.render("MENU", 1, WHITE)
    menuButton_surface.blit(menu_text, (BUTTON_WIDTH//2 - menu_text.get_width()//2, BUTTON_HEIGHT//2 - menu_text.get_height()//2))
    WINDOW.blit(menuButton_surface, menuButton)
    pygame.display.update()

def checkLetters(word, solution, activeRow, tiles):
    # i = 0
    # for tile in tiles[activeRow]:
    #     pos = solution.find(tile.text)
    #     if pos == i:
    #         tile.status = 3 #status 3 : letter in right position
    #         tiles[activeRow][pos].found = 1
    #     i += 1

    # for tile in tiles[activeRow]:
    #     pos = solution.find(tile.text)
    #     # if pos == -1:
    #     #     tile.status = 2 #status 2 : letter not found in word
    #     while tiles[activeRow][pos].found == 1 and solution.find(tile.text, pos + 1, 4) != -1:
    #         pos =  solution.find(tile.text, pos + 1, 4)
    #     if tiles[activeRow][pos].found != 1 and pos != -1:
    #         tile.status = 4 #status 4 : not right position, but it can be found
    #         tiles[activeRow][pos].found = 1
        
    #     print(pos)

        # for letter in solution:
        #     map(letter, lambda x: x + 1)
    tempSolution = list(solution)
    for i in range(5):
        if tiles[activeRow][i].text == tempSolution[i]:
            tempSolution[i] = "."
            tiles[activeRow][i].status = 3 #status 3 : letter in right position
            tiles[activeRow][i].found = 1
    for i in range(5):
        if tiles[activeRow][i].found != 1:
            for j in range(5):
                if tempSolution[j] == tiles[activeRow][i].text:
                    tempSolution[j] = "."
                    tiles[activeRow][i].status = 4
                    tiles[activeRow][i].found = 1
                    break
    for tile in tiles[activeRow]:
        if not tile.found:
            tile.status = 2


def check(word, activeRow, tiles, solution):
    if word == solution:
        print("OK! WIN!")
        return True
    else:
        checkLetters(word, solution, activeRow, tiles)
        print("NOT OK")
        return False

def reset(tiles, activeRow, activeTile, solution):
    tiles = [[],[],[],[],[],[]]
    activeRow = 0
    activeTile = 0
    tiles = defTiles(tiles)
    solution = getRandWord()
    return tiles, activeRow, activeTile, solution

def getRandWord():
    file = open("words.txt","r", encoding = "utf8")
    line = file.readline()
    line = line.split()
    rand = randint(0, len(line))
    print(line[rand])
    return line[rand]
    
    

def main():
    run = True
    tiles = [[],[],[],[],[],[]]
    activeRow = 0
    activeTile = 0
    solution = getRandWord()
    tiles = defTiles(tiles)
    state = MAIN_MENU
    playButton = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT - 150, BUTTON_WIDTH, BUTTON_HEIGHT)
    menuButton = pygame.Rect(WIDTH//2 - BUTTON_WIDTH//2, HEIGHT - 150, BUTTON_WIDTH, BUTTON_HEIGHT)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.collidepoint(event.pos) and state == MAIN_MENU:
                    state = RUNNING
                    start = time.time()
                if menuButton.collidepoint(event.pos) and (state == LOST or state == WIN):
                    tiles, activeRow, activeTile, solution = reset(tiles, activeRow, activeTile, solution)
                    state = MAIN_MENU
            if event.type == pygame.KEYDOWN and state == RUNNING:
                if event.key == pygame.K_BACKSPACE:
                    if activeTile < 5:
                        tiles[activeRow][activeTile].text = ''
                    if activeTile != 0:
                        if activeTile < 5:
                            tiles[activeRow][activeTile].status = 0
                        activeTile -= 1
                        tiles[activeRow][activeTile].text = ''
                        tiles[activeRow][activeTile].status = 1
                elif activeTile < 5:
                    letter = event.unicode.upper()
                    if tiles[activeRow][activeTile].text == '' and letter.isalpha():
                        tiles[activeRow][activeTile].text = letter
                        if activeTile != 5:
                            tiles[activeRow][activeTile].status = 0
                            activeTile += 1
                            if activeTile < 5:
                                tiles[activeRow][activeTile].status = 1
                if event.key == pygame.K_RETURN and activeTile == 5:
                    word = ''
                    for tile in tiles[activeRow]:
                        word += tile.text
                    if check(word, activeRow, tiles, solution):
                        state = WIN
                    elif activeRow < 5:
                        activeRow += 1
                        activeTile = 0
                        tiles[activeRow][0].status = 1
                    else:
                        print("LOST!")
                        state = LOST

        if state == RUNNING:
            current = time.time()
            sub = int(current - start)
            update(tiles, sub)
            
        
        if state == MAIN_MENU:
            update_main(playButton)

        if state == LOST:
            update_lost(menuButton, solution)

        if state == WIN:
            update_win(menuButton, solution)

    clock.tick(FPS)

if __name__ == "__main__":
    main()


