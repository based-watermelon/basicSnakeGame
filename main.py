import pygame
import random

pygame.init()
# Setting up the Game window
font=pygame.font.SysFont(None,30)
big_font=pygame.font.SysFont(None,64)
width,height=600,400
cell_size=20

screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Snake.io")
#Initializing required variables
green=(0,255,0)
black=(0,0,0)
white=(255,255,255)
clock=pygame.time.Clock()
running=True
#Function for randomized food generation
def random_food(snake):
   while True: 
    pos=(random.randint(0,(width//cell_size)-1),random.randint(0,(height//cell_size)-1))
    if pos not in snake:
        return pos 
#Game Reset function to initialize initial conditions    
def reset_game():
    dx,dy=1,0
    x=y=5
    snake=[(5,5),(4,5),(3,5)]
    score=0
    food=random_food(snake)
    running=True
    return x,y,dx,dy,snake,score,food

x,y,dx,dy,snake,score,food=reset_game()
game_over=False

#Main game loop
while running:
    for event in pygame.event.get():
    #Setting keymaps and position updates    
        if event.type==pygame.QUIT:
            running=False      

        if not game_over and event.type==pygame.KEYDOWN :
            if (event.key==pygame.K_LEFT or event.key==pygame.K_a)  and dx!=1:
                dx,dy=-1,0
            elif (event.key==pygame.K_RIGHT or event.key==pygame.K_d) and dx!=-1:
                dx,dy=1,0      
            elif (event.key==pygame.K_UP or event.key==pygame.K_w) and dy!=1:
                dx,dy=0,-1 
            elif (event.key==pygame.K_DOWN or event.key==pygame.K_s) and dy!=-1:
                dx,dy=0,1      

        if game_over and event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r:
                x,y,dx,dy,snake,score,food=reset_game()
                game_over=False
            if event.key==pygame.K_q or event.key==pygame.K_ESCAPE: 
                running=False           
    if not game_over:
     x+=dx;y+=dy;
    #snake movement according to updates
     snake.insert(0,(x,y))

     if(snake[0]==food):
        food=random_food(snake)
        score+=1
     else:    
        snake.pop()    
     if x<0 or x>=width//cell_size or y<0 or y>=height//cell_size or (x,y) in snake[1:]:
        game_over=True
    
    #Drawing game elements 
    screen.fill(black)

    rect_food=pygame.Rect(cell_size*food[0],cell_size*food[1],cell_size,cell_size)
    pygame.draw.rect(screen,(255,0,0),rect_food)

    for segment in snake:
       rect=pygame.Rect(cell_size*segment[0],cell_size*segment[1],cell_size,cell_size)
       pygame.draw.rect(screen,green,rect)
       
       
    score_text=font.render(f"Score: {score}",True,white)
    screen.blit(score_text,(10,10))
    if game_over:
        overlay=pygame.Surface((width,height),pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        screen.blit(overlay,(0,0))

        go_text=big_font.render("GAME OVER",True,white)
        info_line1=font.render("Press R to Restart", True, white)
        info_line2=font.render("Press Q or ESC to Quit", True, white)
        final_score=font.render(f"Final Score: {score}",True,white)

        screen.blit(go_text,((width-go_text.get_width())//2,height//2-80))
        screen.blit(final_score,((width-final_score.get_width())//2,height//2-20))
        screen.blit(info_line1,((width-info_line1.get_width())//2,height//2+20))
        screen.blit(info_line2,((width-info_line2.get_width())//2,height//2+50))
        
        
    pygame.display.flip()
    clock.tick(10)
pygame.quit()    
