import pygame
import random
import os

pygame.init()
pygame.mixer.init()
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
bg_music='assets/music_zapsplat_astro_race.mp3'
eat_sound=pygame.mixer.Sound('assets/music_food.mp3')
crash_sound=pygame.mixer.Sound('assets/battle-pop-424581.mp3')
gameover_sound=pygame.mixer.Sound('assets/5d6eab42-7905-4062-8879-ad08802a7412.mp3')
gameover_sound.set_volume(0.2)
select_sound=pygame.mixer.Sound('assets/select01.ogg')
select_sound.set_volume(0.3)

running=True
#Function for randomized food generation
def load_highscores(file_path='highscores.txt'):
   if not os.path.exists(file_path):
      return []
   scores=[]
   with open(file_path,'r')as f:
      for line in f:
         line=line.strip()
         try:
            scores.append(int(line))
         except ValueError:
            pass   
   return sorted(scores,reverse=True)[:5]     

def save_highscores(new_score,file_path='highscores.txt'):
   scores= load_highscores(file_path)
   scores.append(new_score)
   scores=sorted(scores, reverse=True)[:5]
   with open(file_path, 'w') as f:
      for s in scores:
         f.write(f"{s} \n")
   
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
    pygame.mixer.music.load(bg_music)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
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
                select_sound.play() 
                x,y,dx,dy,snake,score,food=reset_game()
                game_over=False
            if event.key==pygame.K_q or event.key==pygame.K_ESCAPE: 
                select_sound.play()
                running=False       
                    
    if not game_over:
     x+=dx;y+=dy;
     
    #snake movement according to updates
     snake.insert(0,(x,y))

    #eating food 

     if(snake[0]==food):
        food=random_food(snake)
        eat_sound.play()
        score+=1
    #Snake crash    
     else:    
        snake.pop()    
     if x<0 or x>=width//cell_size or y<0 or y>=height//cell_size or (x,y) in snake[1:]:
       if not game_over: 
        save_highscores(score)
        game_over=True
        crash_sound.play()
        gameover_sound.play()
        pygame.mixer.music.stop()
    
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
        scores=load_highscores()
        offset_y=270
        overlay=pygame.Surface((width,height),pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        screen.blit(overlay,(0,0))

        go_text=big_font.render("GAME OVER",True,white)
        info_line1=font.render("Press R to Restart", True, white)
        info_line2=font.render("Press Q or ESC to Quit", True, white)
        final_score=font.render(f"Final Score: {score}",True,white)
        title=font.render("Top 5 highscores",True,white)
    
        screen.blit(go_text,((width-go_text.get_width())//2,80))
        screen.blit(final_score,((width-final_score.get_width())//2,130))
        screen.blit(info_line1,((width-info_line1.get_width())//2,170))
        screen.blit(info_line2,((width-info_line2.get_width())//2,200))
        screen.blit(title, ((width-title.get_width())//2,240))
        for idx, s in enumerate(scores, 1):
          score_text = font.render(f"{idx}. {s}", True, white)
          screen.blit(score_text, ((width-score_text.get_width())//2 , offset_y))
          offset_y += 28
        
        
    pygame.display.flip()
    clock.tick(10)
pygame.quit()    
