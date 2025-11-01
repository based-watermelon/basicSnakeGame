import pygame
pygame.init()
# Setting up the Game window
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

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False      
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_LEFT and dx!=1:
                dx,dy=-1,0
            elif event.key==pygame.K_RIGHT and dx!=-1:
                dx,dy=1,0      
            elif event.key==pygame.K_UP and dy!=1:
                dx,dy=0,-1 
            elif event.key==pygame.K_DOWN and dy!=-1:
                dx,dy=0,1            
    x+=dx;y+=dy;
    snake.insert(0,(x,y))
    snake.pop()
    screen.fill(black)
    for segment in snake:
       rect=pygame.Rect(cell_size*segment[0],cell_size*segment[1],cell_size,cell_size)
       pygame.draw.rect(screen,green,rect)
    # pygame.draw.rect(screen,black,rect_tail)
    pygame.display.flip()
    clock.tick(5)
pygame.quit()    
