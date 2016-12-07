import math
import pygame
import random
import pickle
import os.path

#block dimensions
block_width = 23
block_height = 15

#RGB color values
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)
magenta = (255, 0, 255)

class Ball(pygame.sprite.Sprite):

    def __init__(self, player):

        self.y = 180
        self.speed = 5 #starting speed (in pixels per cycle)
        self.direction = 200 #in degrees
        self.player = player
        self.width = 10
        self.height = 10

                # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])

        # Color the ball
        self.image.fill(white)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        if (player == 1):
            self.x = 0
        else:
            self.x = self.screenwidth/2 + block_width

        self.rect.x = self.x
        self.rect.y = self.y

    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):

        #angles are handles in radians, must convert
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # Do we bounce off the left of the screen?
        if(self.player == 1):

            if self.x <= 0:
                self.direction = (360 - self.direction) % 360
                self.x = 1
        else:

            if(self.x <= self.screenwidth/2 + block_width):
                self.direction = (360 - self.direction) % 360
                self.x = 1 + self.screenwidth/2 + block_width


        # Do we bounce of the right side of the screen?
        if(self.player == 1):

            if(self.x > self.screenwidth/2 - self.width - block_width):
                self.direction = (360 - self.direction) % 360
                self.x = self.screenwidth/2 - self.width - 1 - block_width

        else:
            if(self.x > self.screenwidth - self.width):
                self.direction = (360 - self.direction) % 360
                self.x = self.screenwidth - self.width - 1

    def isDead(self):
            # fall off the bottom of the screen?
        if(self.y > 600):
            return True
        else:
            return False

    def speedUp(self, speed):
        #update speed:
        if (self.player == 1):
            self.speed = speed
        else:
            self.speed = speed

    def respawn(self):
        self.y = 180
        self.direction = 200
        if(self.player == 1):
            self.x = 0
        else:
            self.x = self.screenwidth/2 + block_width

class Block(pygame.sprite.Sprite):

    def __init__(self, player, color, x, y):

        super().__init__()

        self.image = pygame.Surface([block_width, block_height])

        self.image.fill(color)

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

class Paddle(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.speed = 5

        if(player == 1):

            self.rect.x = block_width + self.screenwidth/4 - self.width
            self.rect.y = self.screenheight - self.height

        elif(player == 2):

            self.rect.x = 2*block_width + self.screenwidth*3/4 - self.width
            self.rect.y = self.screenheight - self.height


    def move(self, dir):
        #move player left
        if (dir == "left"):
            if(self.player == 1):
                if(self.rect.x - self.speed >= 0):
                    self.rect.x -= self.speed
                else:
                    self.rect.x = 0
            else:
                if(self.rect.x - self.speed >= self.screenwidth/2 + block_width):
                    self.rect.x -= self.speed
                else:
                    self.rect.x = self.screenwidth/2 + block_width

        if (dir == "right"):
            if (self.player == 1):
                if(self.rect.x + self.speed <= self.screenwidth/2 - self.width - block_width):
                    self.rect.x += self.speed
                else:
                    self.rect.x = self.screenwidth/2 - self.width - block_width

            else:
                if(self.rect.x + self.speed <= self.screenwidth - self.width):
                    self.rect.x += self.speed
                else:
                    self.rect.x = self.screenwidth - self.width
        #move the player left or right

    def speedUp(self, speed):
        #update speed:
        if (self.player == 1):
            self.speed = speed
        else:
            self.speed = speed

class Game:

    def __init__(self):

        #initialize pygame
        pygame.init()

        #setup screen
        screen = pygame.display.set_mode([800, 600])
        pygame.display.set_caption('Steven A Moore')
        font = pygame.font.Font(None, 36)
        font2 = pygame.font.Font(None, 64)
        background = pygame.Surface(screen.get_size())
        screenheight = pygame.display.get_surface().get_height()
        screenwidth = pygame.display.get_surface().get_width()
        pygame.key.set_repeat(2, 10)

        #define sprite groups
        blocks1 = pygame.sprite.Group()
        blocks2 = pygame.sprite.Group()
        balls = pygame.sprite.Group()
        players = pygame.sprite.Group()
        allsprites = pygame.sprite.Group()

        #add in players
        player1 = Paddle(1)
        allsprites.add(player1)
        players.add(player1)
        player1_speed = 5

        player2 = Paddle(2)
        allsprites.add(player2)
        players.add(player2)
        player2_speed = 5

        #create balls
        ball1 = Ball(1)
        allsprites.add(ball1)
        balls.add(ball1)

        ball2 = Ball(2)
        allsprites.add(ball2)
        balls.add(ball2)

        #create blocks
        # The top of the block (y position)
        top1 = 80
        top2 = 80

        # Number of blocks to create(changed it from 15 to 1 to make the game finish faster)
        blockcount = 1

        colors1 = [red, blue, green, yellow, magenta]
        random.shuffle(colors1)
        colors2 = [red, blue, green, yellow, magenta]
        random.shuffle(colors2)

        for row in colors1:
            for column in range(0, blockcount):
                # Create a block (color,x,y)
                block = Block(1, row, column * (block_width + 2) + 1, top1)
                blocks1.add(block)
                allsprites.add(block)
            top1 += block_height + 2

        for row in colors2:
            for column in range(0, blockcount):
                block = Block(2, row, block_width + screenwidth/2 +  column * (block_width + 2) + 1, top2)
                blocks2.add(block)
                allsprites.add(block)
            #move next row down
            top2 += block_height + 2

        #create clock to limit speed
        clock = pygame.time.Clock()

        #create second clock to record time for highscores
        clock2 = pygame.time.Clock()

        #create timer to keep track of highscores
        timer = 0

        #create respawn timers
        respawn_timer_1 = 0
        respawn_timer_2 = 0

        #sends a speedup event every  5 seconds (5000 milliseconds)
        SPEEDUP = pygame.USEREVENT+1
        pygame.time.set_timer(SPEEDUP, 10000)

        #sends an event every 10 milliseconds for the timer
        TIMER = pygame.USEREVENT+2
        pygame.time.set_timer(TIMER, 10)

        #define timers for ball respawn
        RESPAWNTIMER1 = pygame.USEREVENT + 3
        RESPAWNTIMER2 = pygame.USEREVENT + 4
        timer_set1 = False
        timer_set2 = False

        # Is the game over?
        game_over = False

        # Exit the program?
        exit_program = False

        while (exit_program == False):

            #check if balls are dead
            dead1 = ball1.isDead()
            dead2 = ball2.isDead()

            #set fps to 60
            clock.tick(60)

            #clear screen
            screen.fill(black)

            #draw dividing line
            pygame.draw.line(screen, white, (screenwidth/2 - block_width, 0), (screenwidth/2 - block_width, screenheight), 1)
            pygame.draw.line(screen, white, (screenwidth/2 + block_width, 0), (screenwidth/2 + block_width, screenheight), 1)

            # Process the events in the game
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    exit_program = True
                if(event.type == SPEEDUP):
                    player1_speed += 1
                    player2_speed += 1
                if(event.type == TIMER):
                    timer += .01
                if(dead1 == True):
                    if(event.type == RESPAWNTIMER1):
                        respawn_timer_1 += 1
                if(dead2 == True):
                    if(event.type == RESPAWNTIMER2):
                        respawn_timer_2 += 1
            #return an array of all keys pressed during each cycle
            pressed = pygame.key.get_pressed()

            #determine which keys are pressed and move accordingly
            if(pressed[ord("a")] == 1):
                player1.move("left")
            if(pressed[ord("d")] == 1):
                player1.move("right")
            if(pressed[ord("j")] == 1):
                player2.move("left")
            if(pressed[ord("l")] == 1):
                player2.move("right")


            if (game_over == False):

                #update balls
                if(dead1 == True):
                    if(timer_set1 == False):
                        pygame.time.set_timer(RESPAWNTIMER1, 1000)
                        timer_set1 = True
                    if(respawn_timer_1 == 5):
                        ball1.respawn()
                        player1_speed = 5
                        timer_set1 = False
                        respawn_timer_1 = 0
                else:
                    ball1.update()
                    player1.speedUp(player1_speed)
                    ball1.speedUp(player1_speed)

                if(dead2 == True):
                    if(timer_set2 == False):
                        pygame.time.set_timer(RESPAWNTIMER2, 1000)
                        timer_set2 = True
                    if(respawn_timer_2 == 5):
                        ball2.respawn()
                        player2_speed = 5
                        timer_set2 = False
                        respawn_timer_2 = 0
                else:
                    ball2.update()
                    player2.speedUp(player2_speed)
                    ball2.speedUp(player2_speed)


                #draw timer
                label = font.render(str(timer)[:len(str(round(timer))) + 3], 1, white)
                screen.blit(label, (screenwidth - 100, 30))
                if(dead1):
                    label1 = font2.render(str(5 - respawn_timer_1), 1, white)
                    screen.blit(label1, (block_width + screenwidth/4 - 50, 325))
                if(dead2):
                    label2 = font2.render(str(5 - respawn_timer_2), 1, white)
                    screen.blit(label2, (2*block_width + screenwidth*3/4 - 50, 325))


            if (game_over == True):
                text = font.render("Game Over", True, white)
                textpos = text.get_rect(centerx=background.get_width()/2)
                textpos.top = 300
                screen.blit(text, textpos)

                # Records and adds time to high score list when finished
                if(os.path.isfile("BlockGame_Highscores.txt") == False):
                    high_scores = [800,700,600,500,400]
                    for x in range(1):
                        end_time = int(round(pygame.time.get_ticks()/1000))
                    high_scores.append(end_time)
                    high_scores.sort()

                    while(len(high_scores) > 5):
                        del high_scores[-1]

                    pickle.dump(high_scores, open("BlockGame_Highscores.txt", "wb"))

                else:
                    with open('BlockGame_Highscores.txt', 'rb') as f:
                        high_scores = pickle.load(f)
                    for x in range(1):
                        end_time = int(round(pygame.time.get_ticks()/1000))
                    high_scores.append(end_time)
                    high_scores.sort()

                    while(len(high_scores) > 5):
                        del high_scores[-1]

                    with open('BlockGame_Highscores.txt', 'wb') as f:
                        pickle.dump(high_scores, f)

                #This is test code to show that it is printing several times
                for x in range(1):
                    end_score = int(round(pygame.time.get_ticks()/1000))
                    print(end_score)


            if (pygame.sprite.spritecollide(ball1, players, 0)):

                # The 'diff' lets you try to bounce the ball left or right
                # depending where on the paddle you hit it
                diff = (player1.rect.x + player1.width/2) - (ball1.rect.x+ball1.width/2)

                # Set the ball's y position in case
                # we hit the ball on the edge of the paddle
                ball1.rect.y = screen.get_height() - player1.rect.height - ball1.rect.height - 1
                ball1.bounce(diff)

            if (pygame.sprite.spritecollide(ball2, players, 0)):
                # The 'diff' lets you try to bounce the ball left or right
                # depending where on the paddle you hit it
                diff = (player2.rect.x + player2.width/2) - (ball2.rect.x+ball2.width/2)

                # Set the ball's y position in case
                # we hit the ball on the edge of the paddle
                ball2.rect.y = screen.get_height() - player2.rect.height - ball2.rect.height - 1
                ball2.bounce(diff)

            deadblocks1 = pygame.sprite.spritecollide(ball1, blocks1, True)
            deadblocks2 = pygame.sprite.spritecollide(ball2, blocks2, True)

            if len(deadblocks1) > 0:
                ball1.bounce(0)

            if len(deadblocks2) > 0:
                ball2.bounce(0)

            # Game ends if all the blocks are gone
            if (len(blocks1) == 0 or len(blocks2) == 0):
                game_over = True

            allsprites.draw(screen)

            pygame.display.flip()

        pygame.quit()


def main():
    game = Game()

main()
