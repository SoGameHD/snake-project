import tkinter as tk
import random

WIDTH = 300
HEIGHT = 300
SNAKE_BLOCK = 10

class Snake:
    def __init__(self):
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        self.init_game()

    def init_game(self):
        self.snake_pos = [(150, 150)]
        self.snake_segments = []
        self.direction = "d"
        self.last_direction = "d"
        self.food_pos = [self.create_food()]
        self.score = 0
        self.lose = False
        self.reverse_control = False
        self.update_speed = 1
        self.bonus_time = 0
        self.malus_time = 0
        self.bonus_type = 0
        self.malus_type = 0
        self.bonus_pos = self.create_bonus()
        self.malus_pos = self.create_malus()
        self.canvas.bind_all("<Key>", self.on_key_press)
        self.move()

    def create_food(self):
        x = random.randint(0, (WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        y = random.randint(0, (HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="red")
        return (x, y)
    
    def create_malus(self):
        x = random.randint(0, (WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        y = random.randint(0, (HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        if self.update_speed == 0.5:
            self.update_speed = 1
        self.reverse_control = False

        random_range = random.randint(1, 100)        
        if random_range <= 50:
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="blue")
            self.malus_type = 1
        elif random_range <= 90:
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="peru")
            self.malus_type = 2
        elif random_range <= 100: 
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="orchid")
            self.malus_type = 3
        return (x, y)
        
    def create_bonus(self):
        x = random.randint(0, (WIDTH - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        y = random.randint(0, (HEIGHT - SNAKE_BLOCK) // SNAKE_BLOCK) * SNAKE_BLOCK
        if self.update_speed == 1.5:
            self.update_speed = 1

        random_range = random.randint(1, 100)
        if random_range <= 50: 
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="green")
            self.bonus_type = 1
        elif random_range <= 90:
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="white")
            self.bonus_type = 2
        elif random_range <= 100:
            self.canvas.create_rectangle(x, y, x + SNAKE_BLOCK, y + SNAKE_BLOCK, fill="orange")
            self.bonus_type = 3

        return (x, y)
    
    def on_key_press(self, event):
        if event.keysym == "z" and self.last_direction != "s":
            if self.reverse_control:
                self.direction = "d"
            else:
                self.direction = "z"
        elif event.keysym == "s" and self.last_direction != "z":
            if self.reverse_control:
                self.direction = "q"
            else:
                self.direction = "s"
        elif event.keysym == "q" and self.last_direction != "d":
            if self.reverse_control:
                self.direction = "z"
            else:
                self.direction = "q"
        elif event.keysym == "d" and self.last_direction != "q":
            if self.reverse_control:
                self.direction = "s"
            else:
                self.direction = "d"
        if self.lose:
            if event.keysym == "space":
                self.init_game()

    def move(self):
        self.canvas.delete("all")
        if self.direction == "z":
            if self.snake_pos[0][1] - SNAKE_BLOCK < 0:
                self.game_over()
                return
            new_pos = (self.snake_pos[0][0], self.snake_pos[0][1] - SNAKE_BLOCK)
        elif self.direction == "s":
            if self.snake_pos[0][1] + SNAKE_BLOCK > HEIGHT:
                self.game_over()
                return
            new_pos = (self.snake_pos[0][0], self.snake_pos[0][1] + SNAKE_BLOCK)
        elif self.direction == "q":
            if self.snake_pos[0][0] - SNAKE_BLOCK < 0:
                self.game_over()
                return
            new_pos = (self.snake_pos[0][0] - SNAKE_BLOCK, self.snake_pos[0][1])
        elif self.direction == "d":
            if self.snake_pos[0][0] + SNAKE_BLOCK > WIDTH:
                self.game_over()
                return
            new_pos = (self.snake_pos[0][0] + SNAKE_BLOCK, self.snake_pos[0][1])
        self.snake_pos.insert(0, new_pos)
        self.last_direction = self.direction
        
        i = 0
        is_food_eaten = False
        for pos in self.food_pos:
            if new_pos == pos:
                self.food_pos[i] = self.create_food()
                self.score += 1
                is_food_eaten = True
            else:
                self.canvas.create_rectangle(pos[0], pos[1], pos[0] + SNAKE_BLOCK, pos[1] + SNAKE_BLOCK, fill="red")
            i += 1
        if not is_food_eaten:
            self.snake_pos.pop()

        if self.bonus_type != 0:
            if new_pos == self.bonus_pos:
                if self.bonus_type == 1:
                    if self.update_speed == 0.5:
                        self.malus_time = 0
                        self.malus_pos = self.create_malus()
                    self.update_speed = 1.5
                    self.bonus_time = 10000
                elif self.bonus_type == 2:
                    self.food_pos.append(self.create_food())
                    self.bonus_pos = self.create_bonus()
                self.bonus_type = 0
            else:
                if self.bonus_type == 1:
                    self.canvas.create_rectangle(self.bonus_pos[0], self.bonus_pos[1], self.bonus_pos[0] + SNAKE_BLOCK, self.bonus_pos[1] + SNAKE_BLOCK, fill="green")
                elif self.bonus_type == 2:
                    self.canvas.create_rectangle(self.bonus_pos[0], self.bonus_pos[1], self.bonus_pos[0] + SNAKE_BLOCK, self.bonus_pos[1] + SNAKE_BLOCK, fill="orange")

        if self.malus_type != 0:
            if new_pos == self.malus_pos:
                if self.malus_type == 1:
                    if self.update_speed == 1.5:
                        self.bonus_time = 0
                        self.bonus_pos = self.create_bonus()
                    self.update_speed = 0.5
                    self.malus_time = 10000
                elif self.malus_type == 2:
                    self.reverse_control = True
                    self.malus_time = 10000
                self.malus_type = 0
            else:
                if self.malus_type == 1:
                    self.canvas.create_rectangle(self.malus_pos[0], self.malus_pos[1], self.malus_pos[0] + SNAKE_BLOCK, self.malus_pos[1] + SNAKE_BLOCK, fill="blue")
                elif self.malus_type == 2:
                    self.canvas.create_rectangle(self.malus_pos[0], self.malus_pos[1], self.malus_pos[0] + SNAKE_BLOCK, self.malus_pos[1] + SNAKE_BLOCK, fill="orchid")

        for pos in self.snake_pos:
            self.canvas.create_rectangle(pos[0], pos[1], pos[0] + SNAKE_BLOCK, pos[1] + SNAKE_BLOCK, fill="green")

        if self.snake_pos[0][0] < 0 or self.snake_pos[0][0] >= WIDTH or self.snake_pos[0][1] < 0 or self.snake_pos[0][1] >= HEIGHT:
            self.game_over()
            return
            
        if len(self.snake_pos) != len(set(self.snake_pos)):
            self.game_over()
            return
            
        timetowait = (100 - self.score) * self.update_speed

        if self.bonus_time > 0:
            self.bonus_time -= timetowait
            if self.bonus_time <= 0:
                self.bonus_time = 0
                self.bonus_pos = self.create_bonus()
        if self.malus_time > 0:
            self.malus_time -= timetowait
            if self.malus_time <= 0:
                self.malus_time = 0
                self.malus_pos = self.create_malus()

        if timetowait < 10:
            timetowait = 10
            
        root.after(int(timetowait), self.move)
        
        self.canvas.create_text(WIDTH/2, 20, text=str(self.score), font=("Arial", 12, "bold"))


    def game_over(self):
        self.canvas.create_text(WIDTH/2, HEIGHT/2, text="Partie perdue", font=("Arial", 12, "bold"))
        self.canvas.create_text(WIDTH/2, 20, text=str(self.score), font=("Arial", 12, "bold"))
        self.canvas.create_text(WIDTH/2, HEIGHT/2 + HEIGHT/4, text="Barre espace pour recommencer", font=("Arial", 15))
        self.snake_pos = []
        self.lose = True

root = tk.Tk()
root.title("Snake")
snake = Snake()
root.mainloop()