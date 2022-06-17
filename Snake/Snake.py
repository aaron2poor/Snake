
from replit import db
import os
import time, os, random
from copy import deepcopy
import tkinter as tk

window = tk.Tk()
window.attributes('-fullscreen', True)
window.configure(background='#708862') 

def grid(width, height):
    row = []
    grid = []
    for l in range(height):
        for i in range(width):
            if i == 0:
                row = [' ']
            else:
                row.append(' ')
        grid.append(row[:])
    i = 0
    for y in range(height):
        for x in range(width):
            grid[y][x] = random.choice(['#a1c38c','#90af7e','#809c70'])
    return grid

width = 15
height = 15
grid = grid(width, height)
master = deepcopy(grid)
delay = .2
sf = 20
window_width = int(window.winfo_screenwidth())
window_height = int(window.winfo_screenheight())
apple_location = (random.randint(0,width),random.randint(0,height))
frame = tk.Frame(width=sf*width+(sf*2),height=sf*width+(sf*2),bg='#264e15')
frame.place(relx=.5,rely=.5,anchor='center')
screen = tk.Canvas(frame, bg='black', width=sf*width,height=sf*height)
screen.place(x=sf,y=sf)



class Snake:
  def __init__(self):
    self.head_direction = None
    self.length = 2
    self.head_location = [6,6]
    self.locations = []
    self.locations.append(deepcopy(self.head_location))
    self.body_locations = []

  def getDirection(self, event):
    if event.keysym in ['Up','Down','Left','Right']:
      if (self.head_direction == 'Up' and event.keysym == 'Down') or (self.head_direction == 'Down' and event.keysym == 'Up') or (self.head_direction == 'Right' and event.keysym == 'Left') or (self.head_direction == 'Left' and event.keysym == 'Right'):
        pass
      else:
        self.head_direction = event.keysym
    else:
      pass
    
  def move(self, dirn):
    if dirn == 'Up':
      self.head_location[1] -= 1
      self.locations.insert(0,deepcopy(self.head_location))
    elif dirn == 'Down':
      self.head_location[1] += 1
      self.locations.insert(0,deepcopy(self.head_location))
    elif dirn == 'Right':
      self.head_location[0] += 1
      self.locations.insert(0,deepcopy(self.head_location))
    elif dirn == 'Left':
      self.head_location[0] -= 1
      self.locations.insert(0,deepcopy(self.head_location))
    else:
      pass

  def grow(self):
    self.length += 1

snake = Snake()
screen.bind('<Key>',snake.getDirection)
screen.focus_set()

'''start_screen = tk.Frame(width=sf*width+(sf*2),height=sf*width+(sf*2),bg='#264e15')'''
while True:
  
  if (snake.locations[0][0] >= width) or (snake.locations[0][0] < 0):
    break
  if (snake.locations[0][1] >= height) or (snake.locations[0][1] < 0):
    break

  try:
    grid[apple_location[1]][apple_location[0]] = 2
  except:
    while True:
      try:
        while True:
          apple_location = (random.randint(0,len(grid)),random.randint(0,len(grid[0])))
          if apple_location not in snake.locations:
            break
        break
      except:
        print(apple_location)
        continue

  snake.body_locations = []
  for i,v in enumerate(snake.locations):
    if i <= snake.length:
      snake.body_locations.append(v)
      grid[snake.locations[i][1]][snake.locations[i][0]] = 1
    else:
      break
  snake.body_locations.pop(0)

  for y in range(len(grid)):
    for x in range(len(grid[0])):
      if grid[y][x] == 0:
        pass
      elif grid[y][x] == 1:
        screen.create_rectangle(x*sf,y*sf,(x*sf)+sf,(y*sf)+sf,fill='green')
      elif grid[y][x] == 2:
        screen.create_rectangle(x*sf,y*sf,(x*sf)+sf,(y*sf)+sf,fill='red')
      else:
        screen.create_rectangle(x*sf,y*sf,(x*sf)+sf,(y*sf)+sf,fill=grid[y][x])
  
  if snake.locations[0] == [apple_location[0],apple_location[1]]:
    while True:
      try:
        apple_location = (random.randint(0,len(grid)),random.randint(0,len(grid[0])))
        break
      except:
        print(apple_location)
        continue
    snake.grow()
    if snake.length % 2 == 0:
      delay -= .01
  
  if snake.locations[0] in snake.body_locations:
    break
  window.update()
  time.sleep(delay)
  window.update()
  snake.move(snake.head_direction)
  window.update()
  screen.delete('all')
  grid = deepcopy(master)

score = snake.length

player_username = os.environ['REPL_OWNER']
if db.keys() == set():
  db[f'Highscores'] = [['---', 0], ['---', 0], ['---', 0], ['---', 0], ['---', 0]]
scores = list(db[f'Highscores'])
score+= 1
achived_highscore = False
def get_value(value):
  return value[1]
for i, v in enumerate(scores):
  if v[1] < score:
    achived_highscore = True
    scores.insert(i, [player_username, score])
    scores.sort(key=get_value, reverse=True)
    if len(scores) > 5:
        del scores[5]
        break
db[f'Highscores'] = scores

width = screen.winfo_width()
height = screen.winfo_height()
screen.delete('all')
temp = (f'''
1: {scores[0][0]} - {scores[0][1]}
2: {scores[1][0]} - {scores[1][1]}
3: {scores[2][0]} - {scores[2][1]}
4: {scores[3][0]} - {scores[3][1]}
5: {scores[4][0]} - {scores[4][1]}
''')
screen.create_text(int(width/2),int(height/2),fill="white",font="Times 14",text=temp)
if achived_highscore:
  screen.create_text(int(width/2),int(height/2)-100,fill="white",font="Times 14",text=f'You got a Highscore! \nFinal Score was {score}.')
else:
  screen.create_text(int(width/2),int(height/2)-100,fill="white",font="Times 14",text=f'You died! Final Score was {score}.')

while True:
  window.update()
