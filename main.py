import pygame
import random
pygame.init()
# Setting up the Game window
font=pygame.font.SysFont(None,30)
width,height=600,400
cell_size=20
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake: Drawing Test")
green=(0,255,0)
black=(0,0,0)
clock=pygame.time.Clock()
running=True
dx,dy=1,0
x=y=5
snake=[(5,5),(4,5),(3,5),(2,5),(1,5)]
def random_food(snake):
    pos=(random.randint(0,(width//cell_size)-1),random.randint(0,(height//cell_size)-1))
    if pos not in snake:
        return pos 
food=random_food(snake)
score=0
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False      
        elif event.type==pygame.KEYDOWN :
            if (event.key==pygame.K_LEFT or event.key==pygame.K_a)  and dx!=1:
                dx,dy=-1,0
            elif (event.key==pygame.K_RIGHT or event.key==pygame.K_d) and dx!=-1:
                dx,dy=1,0      
            elif (event.key==pygame.K_UP or event.key==pygame.K_w) and dy!=1:
                dx,dy=0,-1 
            elif (event.key==pygame.K_DOWN or event.key==pygame.K_s) and dy!=-1:
                dx,dy=0,1            
    x+=dx;y+=dy;
    snake.insert(0,(x,y))
    if(x<0 or x>=width//cell_size or y<0 or y>=height//cell_size):
        running=False
        break
    if(x,y) in snake[1:]:
        running=False
        break
    if(snake[0]==food):
        food=random_food(snake)
        score+=1
    else:    
     snake.pop()
    screen.fill(black)
    for segment in snake:
       rect=pygame.Rect(cell_size*segment[0],cell_size*segment[1],cell_size,cell_size)
       rect_food=pygame.Rect(cell_size*food[0],cell_size*food[1],cell_size,cell_size)
       pygame.draw.rect(screen,(255,0,0),rect_food)
       pygame.draw.rect(screen,green,rect)
       score_text=font.render(f"Score: {score}",True,(255,255,255))
       screen.blit(score_text,(10,10))

    pygame.display.flip()
    clock.tick(8)
pygame.quit()    
