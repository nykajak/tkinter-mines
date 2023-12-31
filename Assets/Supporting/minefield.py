from tkinter import Canvas

class MineField(Canvas):
    def __init__(self, root, minefield_info):
        width = minefield_info.num_cols * 50
        height = minefield_info.num_rows * 50

        super().__init__(root, width = width * 50, height = height)

        self.root = root
        self.minefield_info = minefield_info
        self.root.geometry(f"{width}x{height}")
        self.flags = set()
        self.revealed = 0
        self.non_bombs = minefield_info.num_cols * minefield_info.num_rows - minefield_info.num_bombs

        self.ids = [[0 for i in range(minefield_info.num_cols)] for j in range(minefield_info.num_rows)]

        # for row in minefield_info.layout:
        #     print(row)

        for i in range(minefield_info.num_rows):
            for j in range(minefield_info.num_cols):
                num = minefield_info.layout[i][j]
                if 0 < num < 9:
                    self.draw_numbered(i,j,"white",num)

                elif num == 0:
                    self.draw_box(i,j,"white")

                elif num == 9:
                    self.draw_box(i,j,"red")

                self.ids[i][j] = self.draw_box(i,j,"gray75")

        self.bind("<Button 1>", self.select_box)
        self.bind("<Button 3>", self.flag_box)

    def check_flags(self,flags = None):
        correct_count = 0
        for flag in flags:
            if self.minefield_info.layout[flag[0]][flag[1]] == 9:
                correct_count += 1

        if correct_count == self.minefield_info.num_bombs:
            return True
        
        return False

    def get_coords(self, event):
        return event.y // 50, event.x // 50
    
    def flag_box(self,event):
        row,col = self.get_coords(event)
        if self.ids[row][col] == 0:
            return

        if (row,col) in self.flags:
            self.flags.remove((row,col))
            self.delete(self.ids[row][col])
            self.ids[row][col] = self.draw_box(row,col, "gray75")
            
        else:
            if len(self.flags) == self.minefield_info.num_bombs:
                return

            self.delete(self.ids[row][col])
            self.ids[row][col] = self.draw_box(row,col, "orange")
            self.flags.add((row,col))

        if len(self.flags) == self.minefield_info.num_bombs:
            if self.revealed == self.non_bombs:
                if self.check_flags(self.flags):
                    self.root.end(True)
    
    def generate_cells(self,row,col):
        self.delete(self.ids[row][col])
        self.ids[row][col] = 0
        self.revealed += 1

        for x,y in self.minefield_info.get_neighbours(row,col):
            if self.ids[x][y] == 0:
                continue

            if (x,y) in self.flags:
                self.flags.remove((x,y))
                self.delete(self.ids[x][y])

            if self.minefield_info.layout[x][y] == 0:
                self.generate_cells(x,y)

            else:
                self.delete(self.ids[x][y])
                self.ids[x][y] = 0
                self.revealed += 1
    
    def reveal_tiles(self,row,col):
        num = self.minefield_info.layout[row][col]

        if num == 9:
            for i in range(self.minefield_info.num_rows):
                for j in range(self.minefield_info.num_cols):
                    self.delete(self.ids[i][j])
                    self.ids[i][j] = 0

            self.root.end(False)
        
        elif num == 0:
            self.generate_cells(row,col)

        else:
            self.delete(self.ids[row][col])
            self.ids[row][col] = 0
            self.revealed += 1
        
    def select_box(self,event):
        row,col = self.get_coords(event)
        if self.ids[row][col] == 0:
            return
        
        self.reveal_tiles(row,col)

        if self.revealed == self.non_bombs:
            if self.check_flags(self.flags):
                    self.root.end(True)

    def draw_box(self, row, col, color):
        return self.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill = color)

    def draw_numbered(self,row, col, color, number):
        self.draw_box(row, col, color)
        self.create_text(col * 50 + 25, row * 50 + 25, text = str(number))

