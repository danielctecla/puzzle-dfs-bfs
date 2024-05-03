import pygame
import random
import time
from sprite import *
from settings import *
from state import *
from collections import deque

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.shuffle_time = 0
        self.start_shuffle = False
        self.previous_choice = ""
        self.start_game = False
        self.start_timer = False
        self.elapsed_time = 0
        self.image = self.load_image()   
        self.maxDepth = 100000

    def create_game(self):
        grid = [[x + y * GAME_SIZE for x in range(1, GAME_SIZE + 1)] for y in range(GAME_SIZE)]
        grid[-1][-1] = 0
        return grid
    
    def load_image(self):
        image = pygame.image.load(IMAGE_PATH)
        image = pygame.transform.scale(image, (TILESIZE * GAME_SIZE, TILESIZE * GAME_SIZE))
        return image

    def create_imagematrix(self):
        matrix = [[(row, col) for col in range(GAME_SIZE)] for row in range(GAME_SIZE)]
        return matrix

    def move(self, row, col, move):
        if move == "u":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]
            self.tiles_img_coords[row][col], self.tiles_img_coords[row - 1][col] = self.tiles_img_coords[row - 1][col], self.tiles_img_coords[row][col]
        elif move == "d":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]
            self.tiles_img_coords[row][col], self.tiles_img_coords[row + 1][col] = self.tiles_img_coords[row + 1][col], self.tiles_img_coords[row][col]
        elif move == "l":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]
            self.tiles_img_coords[row][col], self.tiles_img_coords[row][col - 1] = self.tiles_img_coords[row][col - 1], self.tiles_img_coords[row][col]
        elif move == "r":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]
            self.tiles_img_coords[row][col], self.tiles_img_coords[row][col + 1] = self.tiles_img_coords[row][col + 1], self.tiles_img_coords[row][col]

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("r")
                    if tile.left():
                        possible_moves.append("l")
                    if tile.up():
                        possible_moves.append("u")
                    if tile.down():
                        possible_moves.append("d")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "r":
            possible_moves.remove("l") if "l" in possible_moves else possible_moves
        elif self.previous_choice == "l":
            possible_moves.remove("r") if "r" in possible_moves else possible_moves
        elif self.previous_choice == "u":
            possible_moves.remove("d") if "d" in possible_moves else possible_moves
        elif self.previous_choice == "d":
            possible_moves.remove("u") if "u" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        self.move(row, col, choice)

    def moveSolve(self, move):
        for i in range(4):
            for j in range(4):
                if self.tiles_grid[i][j] == 0:
                    row = i
                    col = j
                    break
        self.move(row, col, move)
        self.draw_tiles()

    def repeet(self, state, list):
        for i in list:
            if i.isEquals(state):
                return True
        return False

    def solve(self):
        success = False; deadend = 0; totalNodes = 0; listInt = []
        for i in range(4):
            for j in range(4):
                listInt.append(self.tiles_grid[i][j])
        
        startState = State(listInt); goalState = State([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0])
        queue = deque(); first = []; path = None

        first.append(startState); queue.append(first)

        deepCon = False; dr = 0; m = 0

        while queue and not success and not deepCon:
            m += 1; validStates = 0; l = list(queue)[0]; last = l[len(l) - 1]
            next = last.nextStates(); totalNodes += len(next)
            queue.popleft()

            for ns in next:
                if not self.repeet(ns, l):
                    validStates += 1; nl = list(l)
                    if ns.goalFunction(goalState):
                        success = True; path = nl
                    nl.append(ns)

                    if len(nl) - 1> dr:
                        dr = len(nl) - 1
                    if dr > self.maxDepth:
                        deepCon = True

                    if self.dept:
                        queue.append(nl)
                    else:
                        queue.appendleft(nl)
            if validStates == 0:
                deadend += 1
        
        if success:
            if self.dept:
                print("Depth First Search")
            else:
                print("Breadth First Search")
            print("Succes!, Path: ", len(path), " nodes: ", totalNodes, " dead ends: ", deadend, " max depth: ", dr)

            self.thePath = ""; self.total_nodes = totalNodes; self.deadEnds = deadend; self.loops = m; self.dr = dr
            n = 0; i = startState.getI(); j = startState.getJ()
            for st in path:
                st.show()
                if n > 0:
                    self.thePath = self.thePath + st.getMovement() 
                n += 1
        else:
            print("No solution found")
        self.sthePath = len(path)
        print("Path: ", self.thePath)
                
            

    def draw_tiles(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                row_ , col_ = self.tiles_img_coords[row][col]
                if tile != 0:
                    subimage = self.image.subsurface((col_ * TILESIZE, row_ * TILESIZE, TILESIZE, TILESIZE))
                    self.tiles[row].append(Tile(self, col, row, subimage, (row_, col_)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty", (row_, col_)))

    def new(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.create_game()
        self.tiles_grid_completed = self.create_game()
        self.tiles_img_coords = self.create_imagematrix()
        self.elapsed_time = 0
        self.start_timer = False
        self.start_game = False
        self.buttons_list = []
        self.dept = False

        self.selected_option = 0
        self.total_moves = 0
        self.showShuffle = True
        self.showTestCases = True
        self.showRestart = False
        self.showMethods = False
        self.showSolve = False
        self.showData = False
        self.useMethod = False
        self.thePath = ""
        self.total_nodes = 0
        self.deadEnds = 0
        self.loops = 0
        self.dr = 0
        self.buttons_list.append(Button(850, 75, 200, 50, 'Shuffle', WHITE, BLACK))
        self.buttons_list.append(Button(850, 175, 200, 50, 'DFS', WHITE, BLACK))
        self.buttons_list.append(Button(850, 250, 200, 50, 'BFS', WHITE, BLACK))
        self.buttons_list.append(Button(850, 325, 200, 50, 'Solve', WHITE, BLACK))
        self.buttons_list.append(Button(850, 450, 200, 50, 'Test Case', WHITE, BLACK))
        self.buttons_list.append(Button(850, 525, 200, 50, 'Reset', WHITE, BLACK))
        self.draw_tiles()

    def run(self):
        self.playing = True
        while self.playing:
            if self.thePath == "":
                self.clock.tick(FPS)
            else:
                self.clock.tick(2)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.thePath == "":
            if self.start_game:
                if self.tiles_grid == self.tiles_grid_completed:
                    self.start_game = False
                if self.start_timer:
                    self.timer = time.time()
                    self.start_timer = False
                self.elapsed_time = time.time() - self.timer

            if (self.dept and self.selected_option == 1) or (self.selected_option == 2 and not self.dept):
                if self.start_timer:
                    self.timer = time.time()
                    self.start_timer = False
                self.solve()
                self.selected_option = -1
                self.showShuffle = True
                self.showMethods = False
                self.showTestCases = True
                self.elapsed_time = time.time() - self.timer
                

            if self.start_shuffle:
                self.shuffle()
                self.draw_tiles()
                self.shuffle_time += 1
                if self.shuffle_time > 120:
                    self.start_shuffle = False
        else:
            move = self.thePath[0]
            self.thePath = self.thePath[1:]
            self.moveSolve(move)
        self.all_sprites.update()

    def draw_grid(self):
        for row in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (row + TILESIZE/8, TILESIZE/2), (row + TILESIZE/8, GAME_SIZE * TILESIZE + TILESIZE/2))
        for col in range(-1, GAME_SIZE * TILESIZE, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (TILESIZE/8, col + TILESIZE/2), (GAME_SIZE * TILESIZE +TILESIZE/8, col + TILESIZE/2))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        for button in self.buttons_list:
            if button.text == "Shuffle" and self.showShuffle:
                button.draw(self.screen)
            if button.text == "DFS" and self.showMethods:
                button.draw(self.screen)
            if button.text == "BFS" and self.showMethods:
                button.draw(self.screen)
            if button.text == "Solve" and self.showSolve:
                button.draw(self.screen)
            if button.text == "Test Case" and self.showTestCases:
                button.draw(self.screen)
            if button.text == "Reset" and self.showRestart:
                button.draw(self.screen)
        
        UIElement(550, 25, "Selected Mode:").draw(self.screen)
        if self.start_game:
            UIElement(550, 75, "Normal").draw(self.screen)
        elif self.selected_option == 0:
            UIElement(550, 75, "None").draw(self.screen)
        elif self.dept:
            UIElement(550, 75, "DFS").draw(self.screen)
        else:
            UIElement(550, 75, "BFS").draw(self.screen)

        if self.start_game:
            UIElement(550, 150, "Total Moves:").draw(self.screen)
            UIElement(550, 200, str(self.total_moves)).draw(self.screen)
            UIElement(550, 500, "Time:").draw(self.screen)
            UIElement(550, 555, "%.3f" % self.elapsed_time).draw(self.screen)
        elif self.showData:
            UIElement(550, 150, f"Path with: {self.sthePath} nodes").draw(self.screen)
            UIElement(550, 300, f"Generated nodes: {self.total_nodes}").draw(self.screen)
            UIElement(550, 350, f"Dead ends: {self.deadEnds}").draw(self.screen)
            UIElement(550, 400, f"Loops: {self.loops}").draw(self.screen)
            UIElement(550, 555, f"Time: {round(self.elapsed_time,4)} seg").draw(self.screen)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if self.thePath == "":
                            if tile.click(mouse_x, mouse_y):
                                if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                    self.move(row, col, "r")
                                    if self.start_game:
                                        self.total_moves += 1
                                if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                    self.move(row, col, "l")
                                    if self.start_game:
                                        self.total_moves += 1
                                if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                    self.move(row, col, "u")
                                    if self.start_game:
                                        self.total_moves += 1
                                if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                    self.move(row, col, "d")
                                    if self.start_game:
                                        self.total_moves += 1
                                self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle" and self.showShuffle:
                            self.selected_option = 0
                            self.showData = False
                            self.shuffle_time = 0
                            self.start_shuffle = True
                            self.showSolve = True
                            self.showTestCases = False
                            self.showRestart = True
                            self.thePath = ""
                        if button.text == "DFS" and self.showMethods:
                            self.selected_option = 1
                            self.dept = True
                            self.showData = True
                            self.start_timer = True
                            self.showRestart = True
                        if button.text == "BFS" and self.showMethods:
                            self.dept = False
                            self.selected_option = 2
                            self.showData = True
                            self.start_timer = True
                            self.showRestart = True
                        if button.text == "Reset":
                            self.new()
                        if button.text == "Solve":
                            self.start_game = True
                            self.showShuffle = False
                            self.start_timer = True
                            self.showSolve = False
                        if button.text == "Test Case" and self.showTestCases:
                            self.selected_option = 0
                            self.thePath = ""
                            self.showData = False
                            self.showMethods = True
                            self.showShuffle = False
                            self.showSolve = False
                            self.showTestCases = False
                            
                            #if want to use DFS or BFS without defined test case
                            #just comment the three lines below
                            #consider that doing this, the program could crash
                            # self.tiles_grid = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[0,13,14,15]]
                            # self.tiles_img_coords = [[(0,0),(0,1),(0,2),(0,3)],[(1,0),(1,1),(1,2),(1,3)],[(2,0),(2,1),(2,2),(2,3)],[(3,3),(3,0),(3,1),(3,2)]]
                            # self.draw_tiles()


game = Game()
if __name__ == "__main__":
    game.new()
    game.run()
