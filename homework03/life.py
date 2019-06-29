import pygame 
from pygame.locals import * 
import random 


class GameOfLife: 
    
    def __init__(self, width=640, height=480, cell_size=10, speed=10): 
        self.width = width 
        self.height = height 
        self.cell_size = cell_size 
        # Устанавливаем размер окна 
        self.screen_size = width, height 
        # Создание нового окна 
        self.screen = pygame.display.set_mode(self.screen_size) 
        # Вычисляем количество ячеек по вертикали и горизонтали 
        self.cell_width = self.width // self.cell_size 
        self.cell_height = self.height // self.cell_size 
        # Скорость протекания игры 
        self.speed = speed 
 
    def draw_grid(self): 
        """ Отрисовать сетку """ 
        for x in range(0, self.width, self.cell_size): 
            pygame.draw.line(self.screen, pygame.Color('black'), 
                (x, 0), (x, self.height)) 
        for y in range(0, self.height, self.cell_size): 
            pygame.draw.line(self.screen, pygame.Color('black'), 
                    (0, y), (self.width, y)) 

    def run(self): 
        """ Запустить игру """ 
        pygame.init() 
        clock = pygame.time.Clock() 
        pygame.display.set_caption('Game of Life') 
        self.screen.fill(pygame.Color('white')) 
 
        # Создание списка клеток
        self.cell_list(randomize=True)
        running = True
        while running: 
            for event in pygame.event.get(): #возврат списка всех объектов event из очереди  
                if event.type == QUIT:       
                    running = False
            # Отрисовка списка клеток 
            # Выполнение одного шага игры (обновление состояния ячеек)
                self.draw_cell_list(self.clist)
                self.update_cell_list(self.clist)
                self.draw_grid()
            pygame.display.flip() 
            clock.tick(self.speed) 
        pygame.quit() 
 
 
    def cell_list(self, randomize=True): 
        """ Создание списка клеток.
        :param randomize: Если True, то создается список клеток, где 
        каждая клетка равновероятно может быть живой (1) или мертвой (0). 
        :return: Список клеток, представленный в виде матрицы 
        """ 
        if randomize:
            self.clist = [[random.randint(0,1) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        else:
            self.clist = [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        return self.clist 
 
    def draw_cell_list(self, clist): 
        """ Отображение списка клеток 
  
        :param rects: Список клеток для отрисовки, представленный в виде матрицы 
        """
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if clist[row][col]:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size))


    def get_neighbours(self, cell): 
        """ Вернуть список соседей для указанной ячейки 
  
        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col) 
        :return: Одномерный список ячеек, смежных к ячейке cell 
        """ 
        neighbours = []
        row,col = cell
        positions = [[-1, -1], [-1, 0], [-1, 1], [1, -1], [1, 0], [1, 1], [0, -1], [0, 1]]
        for neighbour in positions:
            if (0 <= neighbour[0] + row < self.cell_height) and (0 <= neighbour[1] + col < self.cell_width):
                neighbours.append(self.clist[neighbour[0] + row][neighbour[1] + col])
        return neighbours 
 
 
    def update_cell_list(self, cell_list): 
        """ Выполнить один шаг игры. 
  
        Обновление всех ячеек происходит одновременно. Функция возвращает 
        новое игровое поле. 
  
        :param cell_list: Игровое поле, представленное в виде матрицы 
        :return: Обновленное игровое поле 
        """ 
        newclist = [[0 for _ in range(self.cell_width)] for _ in range(self.height)]
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                if cell_list[row][col]:
                    if 2 <=  self.get_neighbours((row,col)).count(1) <= 3:
                        newclist[row][col] = 1
                    else:
                        newclist[row][col] = 0
                else:
                    if (self.get_neighbours((row, col)).count(1)) == 3:
                        newclist[row][col] = 1
        self.clist = newclist
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 10, 5)
    game.run() 
