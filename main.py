import pygame as pg
import random
import sys
import asyncio


# Blocks
class Block:
    def __init__(self, id):
        self.id = id
        self.cells = {}
        self.cell_size= 30
        self.row_offset=0
        self.column_offset= 0        
        self.rotation_state= 0
        self.colors = Colors.get_cell_colors()
        
    def move(self, rows, columns):
        self.row_offset += rows
        self.column_offset += columns 
        
    def get_cell_positions(self):
        tiles = self.cells[self.rotation_state]
        moved_tiles = []
        for position in tiles:
            position = Position(position.row + self.row_offset, position.column + self.column_offset)
            moved_tiles.append(position)
        return moved_tiles
    
    def rotate(self):
        self.rotation_state += 1
        if self.rotation_state ==  len(self.cells):
            self.rotation_state = 0
    
    def undo_rotation(self):
        self.rotation_state -= 1
        if self.rotation_state == 0:
            self.rotation_state = len(self.cells) - 1
    
    def draw(self, screen, offset_x, offset_y):
        tiles = self.get_cell_positions()
        for tile in tiles:
            tile_rect = pg.Rect(offset_x + tile.column * self.cell_size , offset_y + tile.row * self.cell_size , self.cell_size -1, self.cell_size -1)
            pg.draw.rect(screen, self.colors[self.id], tile_rect)

class Lblock(Block):
    def __init__(self):
        super().__init__(id =1) 
        self.cells= {
            0: [Position(0,2), Position(1,0), Position(1,1),Position(1,2)],
            1: [Position(0,1), Position(1,1), Position(2,1),Position(2,2)],
            2: [Position(1,0), Position(1,1), Position(1,2),Position(2,0)],
            3: [Position(0,0), Position(0,1), Position(1,1),Position(2,1)]
        }
        
class Jblock(Block):
    def __init__(self):
        super().__init__(id =2) 
        self.cells= {
            0: [Position(0,0), Position(1,0), Position(1,1),Position(1,2)],
            1: [Position(0,1), Position(0,2), Position(1,1),Position(2,1)],
            2: [Position(1,0), Position(1,1), Position(1,2),Position(2,2)],
            3: [Position(0,1), Position(1,1), Position(2,0),Position(2,1)]
        }
        self.move(0,3)
class Iblock(Block):
    def __init__(self):
        super().__init__(id =3) 
        self.cells= {
            0: [Position(1,0), Position(1,1), Position(1,2),Position(1,3)],
            1: [Position(0,2), Position(1,2), Position(2,2),Position(3,2)],
            2: [Position(2,0), Position(2,1), Position(2,2),Position(2,3)],
            3: [Position(0,1), Position(1,1), Position(2,1),Position(3,1)]
        }
        self.move(-1,3)
class Oblock(Block):
    def __init__(self):
        super().__init__(id =4) 
        self.cells= {
            0: [Position(0,0), Position(0,1), Position(1,0),Position(1,1)],   
        }
        self.move(0,4)
class Sblock(Block):
    def __init__(self):
        super().__init__(id =5) 
        self.cells= {
            0: [Position(0,1), Position(0,2), Position(1,0),Position(1,1)],
            1: [Position(0,1), Position(1,1), Position(1,2),Position(2,2)],
            2: [Position(1,1), Position(1,2), Position(2,0),Position(2,1)],
            3: [Position(0,0), Position(1,0), Position(1,1),Position(2,1)]
        }
        self.move(0,3)
class Tblock(Block):
    def __init__(self):
        super().__init__(id =6) 
        self.cells= {
            0: [Position(0,1), Position(1,0), Position(1,1),Position(1,2)],
            1: [Position(0,1), Position(1,1), Position(1,2),Position(2,1)],
            2: [Position(1,0), Position(1,1), Position(1,2),Position(2,1)],
            3: [Position(0,1), Position(1,0), Position(1,1),Position(2,1)]
        }
        self.move(0,3)
class Zblock(Block):
    def __init__(self):
        super().__init__(id =7) 
        self.cells= {
            0: [Position(0,0), Position(0,1), Position(1,1),Position(1,2)],
            1: [Position(0,2), Position(1,1), Position(1,2),Position(2,1)],
            2: [Position(1,0), Position(1,1), Position(2,1),Position(2,2)],
            3: [Position(0,1), Position(1,0), Position(1,1),Position(2,0)]
        }
        self.move(0,3)

#Colors
class Colors:    
    dark_grey = (0,0,0)
    Cor1 = (119, 9, 230)
    Cor2 = (9, 230, 82)
    Cor3 = (255,255,255)
    Cor4 = (22, 31, 234)
    Cor5 = (243, 255, 11)
    Cor6 = (254, 92, 254)
    Cor7 = (230, 141, 10)
    white= (255,255,255)
    dark_blue = (44,44,127)
    light_blue = (59,85,162)
    black = (0,0,0)
    
    @classmethod
    def get_cell_colors(cls):
        return(cls.dark_grey, cls.Cor1, cls.Cor2, cls.Cor3, cls.Cor4, cls.Cor5, cls.Cor6, cls.Cor7)
    
#GAME

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [Iblock(), Jblock(), Lblock(), Oblock(), Sblock(), Tblock(), Zblock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over= False
        self.score= 0
       
        self.clear_sound = pg.mixer.Sound("Sounds/tetrisline.ogg")
        
        pg.mixer.music.load("Sounds/tetrisoriginal.ogg")
        volume = 0.3 
        pg.mixer.music.set_volume(volume)
        
        pg.mixer.music.play(-1)
    
        
        
        
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared ==1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score +=500
        elif lines_cleared == 4:
            self.score +=600
        elif lines_cleared == 5:
            self.score +=700
        elif lines_cleared == 6:
            self.score +=800
        elif lines_cleared == 7:
            self.score +=900
        elif lines_cleared == 8:
            self.score +=1000
        self.score += move_down_points
            
        
    def get_random_block(self):
        if len(self.blocks) ==0:
            self.blocks = [Iblock(), Jblock(), Lblock(), Oblock(), Sblock(), Tblock(), Zblock()]
        
        block  = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)
        
    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)
    
    def move_down(self):
        self.current_block.move(1,0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
            
    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared,0)
        if self.block_fits() == False:
            self.game_over = True
            
    def reset(self):
        self.grid.reset()
        self.blocks = [Iblock(), Jblock(), Lblock(), Oblock(), Sblock(), Tblock(), Zblock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0
            
        
    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column)== False:
                return False
        return True  
        
    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        # else: 
        #     self.rotate_sound.play() 
        
    def block_inside(self):
        tiles = self.current_block.get_cell_positions()    
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True
    
 
    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen,11,11)
        
        if self.next_block.id == 3:
            self.next_block.draw(screen,255,290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen,255,280)
        elif self.next_block.id == 1:
            self.next_block.draw(screen, 350,280)       
        else:
            self.next_block.draw(screen, 270,270)
            
#GRID
class Grid:
    def __init__(self):
        self.num_rows = 20
        self.num_cols = 10
        self.cell_size = 30
        self.grid = [[0 for j in range(self.num_cols)] for i in range(self.num_rows)]
        self.colors = Colors.get_cell_colors() 
        
    def print_grid(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end= " ")
            print()
            
            
    def is_inside(self,row,column):
        if row >= 0 and row < self.num_rows and column >= 0 and  column < self.num_cols:
            return True   
        return False
    
    def is_empty(self,row,column):
        if self.grid[row][column] == 0:
            return True
        return False
    
    def is_row_full(self,row):
        for column in range(self.num_cols):
            if self.grid[row][column] == 0:
                return False
        return True
    
    def clear_row(self,row):
        for column in range(self.num_cols):
            self.grid[row][column] = 0
            
    def move_row_down(self,row, num_rows):
        for column in range(self.num_cols):
            self.grid[row+num_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0
            
    def clear_full_rows(self):
        completed = 0
        for row in range(self.num_rows-1,0,-1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed >0:
                self.move_row_down(row,completed)
        return completed
    
    def reset(self):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                self.grid[row][column] = 0
            
            
    def draw(self,screen):
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                cell_value = self.grid[row][column]
                cell_rect = pg.Rect(column*self.cell_size +11 ,row*self.cell_size + 11,self.cell_size -1,self.cell_size -1)
                pg.draw.rect(screen, self.colors[cell_value], cell_rect)
                
#POSITIONS
class Position:
    def __init__(self,row,column):
        self.row = row
        self.column = column

pg.init()

title_font = pg.font.Font(None, 40)
score_surface= title_font.render("Pontos", True, Colors.white)
next_surface = title_font.render("Proximo",True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)


score_rect = pg.Rect(320,55,170,60)
next_rect = pg.Rect(320,215,170,180)


screen = pg.display.set_mode((500,620))
pg.display.set_caption("Python Tetris")

clock = pg.time.Clock()

game = Game()

async def main():
    
    GAME_UPDATE = pg.USEREVENT
    pg.time.set_timer(GAME_UPDATE, 200)
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
       
                sys.exit()
            if event.type == pg.KEYDOWN:
                if game.game_over == True:
                    game.game_over = False
                    game.reset()
                if event.key == pg.K_LEFT and game.game_over == False:
                    game.move_left()
                if event.key == pg.K_RIGHT and game.game_over == False:
                    game.move_right()
                if event.key == pg.K_DOWN and game.game_over == False:
                    game.move_down() 
                    game.update_score(0,1)   
                if event.key == pg.K_UP and game.game_over == False:
                    game.rotate()  
            if event.type ==  GAME_UPDATE and game.game_over == False:
                game.move_down()  
        
        #Drawing    
        
        score_value_surface = title_font.render(str(game.score),True, Colors.white)
            
        screen.fill(Colors.dark_blue)
        screen.blit(score_surface,(365,20,50,50))
        screen.blit(next_surface, (355,180,50,50))
        
        
        if game.game_over == True:
            screen.blit(game_over_surface, (320,450,50,50))
            
        pg.draw.rect(screen, Colors.black, score_rect, 0, 10)
        screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
        pg.draw.rect(screen, Colors.black, next_rect,0,10)
        game.draw(screen)
    
        
        pg.display.update()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())
