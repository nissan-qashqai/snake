from tkinter import *
import random
import time

#control center
#----------------------------
spaceWidth = 20
snakeColor = "green"
snakeDefaultParts = 3
foodColor = "red"
backgroundColor = "#608bbc"
screenWidth = 500
screenHeight= 500
speed = 1
#----------------------------

direction = "right"
score = 0
restart = False
gmlb = []

class snake:
    def __init__(self, color, parts):
        self.color = color
        self.parts_num = parts
        self.reborn()

    def reborn(self):
        self.parts = []
        self.cordinates = []
        for i in range(self.parts_num):
            x = i
            y = 0
            part = c.create_rectangle(x*spaceWidth +2, y*spaceWidth + 2, (x+1)*spaceWidth -2, (y+1)*spaceWidth -2 , fill=self.color)
            self.parts.insert(0, part)
            self.cordinates.insert(0,[y,x])


    def snake_ate(self,food):
        global score
        if food.cordinate == self.cordinates[0]:
            score += 1
            label_scor.config(text="Score : " + str(score) )
            self.add_part()
            _food.reborn()
            
               

    def move(self):
        self.add_part()
        self.snake_ate(_food)
        c.delete(self.parts[-1])
        del self.parts[-1]
        del self.cordinates[-1]
    
    def add_part(self):
        global direction
        y, x = self.cordinates[0]
        if direction == "right":
            x += 1
        elif direction == "left":
            x -= 1
        elif direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        
        part = c.create_rectangle(x*spaceWidth + 2, y*spaceWidth+ 2, (x+1)*spaceWidth -2, (y+1)*spaceWidth -2 , fill=self.color)
        self.cordinates.insert(0,[y,x])        
        self.parts.insert(0,part)

    def delete(self):

        for p in self.parts:
            c.delete(p)


    def gameOver(self):
        y,x = self.cordinates[0]
        permission = y == screenHeight/spaceWidth or y == -1 or x == screenWidth/spaceWidth \
            or x == -1 or [y,x] in self.cordinates[1:]
        if permission:
            return True
        return False

class food:
    def __init__(self, color):
        self.color = color       
        self.food_list = [] 
        self.create()
    def reborn(self):
        self.create()
        c.delete(self.food_list[-1])
        del self.food_list[-1]

    def create(self):
        self.x = random.randint(snakeDefaultParts+ 5,  screenWidth/ spaceWidth-1)
        self.y = random.randint(2,  screenHeight/ spaceWidth-1)
        if not ([self.y,self.x] in _snake.cordinates):
            food = c.create_rectangle(self.x*spaceWidth + 2, self.y*spaceWidth + 2, (self.x+1)*spaceWidth -2, (self.y+1)*spaceWidth -2 , fill=self.color)
            self.food_list.insert(0,food)
            self.cordinate = [self.y,self.x]
        else:
            self.create()

    def delete(self):

        for f in self.food_list:
            c.delete(f)

def change_direction(_direction):
    global direction
    permission = (_direction == "up" and direction != "down") or (_direction == "down" and direction != "up") or \
        (_direction == "left" and direction != "right") or (_direction == "right" and direction != "left")
    if permission:
        direction = _direction

def change_restart(bl):
    global restart, _snake, _food, score, direction
    restart = bl
    direction = "right"

    for g in gmlb:
        c.delete(g)  
    _snake.reborn()
    _food.reborn()
    new_turn()

def new_turn():

    global _snake, _food, score, restart
    score = 0
    label_scor['text'] = "Score : 0"
    
    while True:
        if not _snake.gameOver():

            _snake.move()     
            time.sleep(float( str( "0." + str( speed ) ) ) )
        
            w.update()
        else: 
            _snake.delete()
            _food.delete()
            break
    gameOverLabel = c.create_text(screenWidth/2, screenHeight/2,text=""*10+"game over\n please click anywhere to restart",font=("comic sans",15,"bold"))
    gmlb.append(gameOverLabel)
    w.bind("<Button-1>", lambda event: change_restart(True))

w = Tk()
photo = PhotoImage(file='icon.png')
w.iconphoto(True,photo)
w.resizable(False,False)
w.title("Snake Game")
w.bind("<Up>",lambda event : change_direction("up"))
w.bind("<Down>",lambda event : change_direction("down"))
w.bind("<Left>",lambda event : change_direction("left"))
w.bind("<Right>",lambda event : change_direction("right"))


label_scor = Label(w, text="Score :", font=("comic sans",20,"bold"))
label_scor.pack(side=TOP)

c = Canvas(w,bg=backgroundColor,width=screenWidth,height=screenHeight)
c.pack()

_snake = snake(snakeColor,snakeDefaultParts)
_food = food(foodColor)

new_turn()


w.mainloop()
#made by nissan-qashqai