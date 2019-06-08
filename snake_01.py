import pygame,sys,random

pygame.init()

game_display = pygame.display.set_mode((800,600))
pygame.display.set_caption("snake")

clock = pygame.time.Clock()

#function for msg on screen

font = pygame.font.SysFont(None, 35)
def display_text(msg, color):
    text = font.render(msg, True, color)
    return text, text.get_rect()

red = (255,0,0)

def screen_msg(msg,color,y=300):
    surface_text,text_rect = display_text(msg, color)
    text_rect.center = 400,y
    game_display.blit(surface_text,text_rect)

#=======================================================================

def score(points):
    text = font.render("SCORE: " + str(points), True, (0,140,0))
    game_display.blit(text , [10,10])


direction = "right"
green = (0,140,0)
def start():
    while True:
        screen_msg("welcome to snake game!",green,200)
        screen_msg("press 'c' for continue, 'q' for quit",green,300)
        screen_msg("you can use 'space' to pause the game",green,400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    run_game()
                elif event.key == pygame.K_q:
                    sys.exit()
        pygame.display.update()
        clock.tick(5)

def game_pause():

    paused = True

    while paused: 
        screen_msg("paused",red,300)
        screen_msg("press 'c' for continue or 'q' to quit",red,350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    game_pause()

        pygame.display.update()
        clock.tick(5)



def run_game():
    random_food_x = round(random.randrange(20,770)/10.0)*10.0
    random_food_y = round(random.randrange(20,570)/10.0)*10.0
    lead_x = 300
    lead_y = 200
    lead_x_change = 0
    lead_y_change = 0
    FPS = 30
    white = (255,255,255)
    black = (0,0,0)
    red = (255,0,0)
    game_over = False
    game_close = False
    # pygame.init()
    snake_list = []
    snake_len = 1

    global direction

    img = pygame.image.load("snakehead1.png")
    apple_img = pygame.image.load("snake_food.png")


    def snake(snake_list, img):
        if direction == "right":
            head = pygame.transform.rotate(img,270)
        elif direction == "left":
            head = pygame.transform.rotate(img,90)
        elif direction == "up":
            head = pygame.transform.rotate(img,0)
        elif direction == "down":
            head = pygame.transform.rotate(img,180)
         
        game_display.blit(head , [snake_list[-1][0],snake_list[-1][1]])
        for XnY in snake_list[:-1] :
            pygame.draw.rect(game_display, white, [XnY[0],XnY[1],10,10])

    while not game_close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = 10
                    lead_y_change = 0
                elif event.key == pygame.K_LEFT:
                    direction = "left"                    
                    lead_x_change = -10
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -10
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = 10
                    lead_x_change = 0
                elif event.key == pygame.K_SPACE:
                    game_pause()



        if random_food_x <= lead_x <= random_food_x+20 and random_food_y <= lead_y <= random_food_y+20:
            random_food_x = round(random.randrange(20,770)/10.0)*10.0
            random_food_y = round(random.randrange(20,570)/10.0)*10.0
            snake_len +=1

        if lead_x >= 770 or lead_x <= 20 or lead_y <= 20 or lead_y >= 570:
            game_over = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        game_display.fill(white)
        game_display.fill(black, rect = [10,10,780,580])
        game_display.blit(apple_img, [random_food_x,random_food_y,20,20])
        # game_display.fill(red, rect = [random_food_x,random_food_y,20,20])
        game_display.fill(white, rect = [lead_x,lead_y,10,10])
        
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_len:
            del snake_list[0]

        snake(snake_list,img)

        if len(snake_list) > 2:
            for tip in snake_list[:-1]:
                if tip == snake_head:
                    game_over = True

        score(snake_len - 1)
 
        pygame.display.update()

        while game_over:
            screen_msg("GAME OVER PRESS 'C' FOR CONTINUE AND 'Q' FOR QUIT",red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        run_game()
                    elif event.key == pygame.K_q:
                        sys.exit()

        clock.tick(FPS)
        
    pygame.quit()
start()
# run_game()
