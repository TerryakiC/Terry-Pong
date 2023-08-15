import pygame
import random
from sklearn.linear_model import LogisticRegression


#colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
purple = pygame.Color(128, 0, 128)

#window
window_x = 720
window_y = 480


#paddles
paddle_speed = 30
paddle_size = [10, 40]
paddle1_position = [25, 40]
paddle2_position = [695, 40]

#score handling
#player 1 is the left paddle and player 2 is the right
p1score = 0
p2score = 0


#ball
ball_position = [window_x // 2, window_y // 2]
ballYM = 5 #ball x momentum
ballXM = 5 #ball y momentum
ball_size = [10, 10]
ball_clone = [ball_position[0], ball_position[1]]
ball_cloneX = 5
ball_cloneY = 5

#direction handling
direction = None
direction2 = None

#game status handling
tie = False
WON = False
gameStart = False
gamePause = False

Cpu = False
Cpu2 = False
change = False

#pygame setting up the game window
pygame.init()
pygame.display.set_caption('Tong')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()
pad1Speed = 10
pad2Speed = 10
def getnum(num = 0):
    return num

#displays the pause menu
def pause():
    font = pygame.font.SysFont('boldarial', 64)
    pause = font.render("PAUSED", True, white)
    game_window.blit(pause, (window_x // 2.5, 100))

#displays the score of each player
def showScore():
    font = pygame.font.SysFont('boldarial', 40)
    text1 = font.render(str(p1score), True, white)
    text2 = font.render(str(p2score), True, white)
    game_window.blit(text1, (window_x // 3, 20))
    game_window.blit(text2, (window_x - (window_x // 3), 20))

#displays the prompt to start the game/round
def start():
    font = pygame.font.SysFont('boldarial', 32)
    start = font.render("Press _Space_ to Launch the Ball", True, white)
    game_window.blit(start, (window_x // 4, 60))


#displays the winner
def win(winner):
    font = pygame.font.SysFont('boldarial', 32)
    win_text = font.render(winner + " wins!!", True, white)
    game_window.blit(win_text, (window_x // 2.5, 60))

#reset the ball to middle of the screen
def resetBall():
    return [window_x // 2, window_y // 2]



while True:
    #grab keyboard inputs that will determine the direction of the paddles
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                direction = 'W'
            elif event.key == pygame.K_s:
                direction = 'S'
            if event.key == pygame.K_UP:
                direction2 = 'UP'
            elif event.key == pygame.K_DOWN:
                direction2 = 'DOWN'
            #exits game window
            if event.key == pygame.K_RIGHT:
                pygame.quit()
            #space key will launch the ball at a random direction if the game is not paused or won and game has not started.This is start the game
            if event.key == pygame.K_SPACE:
                if not gamePause:
                    if not WON:
                        if not gameStart:
                            gameStart = True
                            ballXM = random.choice([-5, 5])
                            ballYM = random.choice([-5, 5])
            #p key will pause the game
            if event.key == pygame.K_p:
                if gamePause:
                    gamePause = False
                else:
                    gamePause = True
            #pressing o will reset the game after a win
            if event.key == pygame.K_o:
                if WON:
                    if not gamePause:
                        WON = False
                        p1score = 0
                        p2score = 0
                        tie = False
            if event.key == pygame.K_i:
                if Cpu:
                    Cpu = False
                else:
                    Cpu = True
            if event.key == pygame.K_u:
                if Cpu2:
                    Cpu2 = False
                else:
                    Cpu2 = True
        #if the up and down arrows or w and s keys are lifted, make the direction to none which will stop the paddles
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                direction = None
            if not Cpu:
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    direction2 = None




    #if cpu is activated let the code move the paddles
    if Cpu:
        if ball_position[0] > window_x // 3:
            if paddle2_position[1] + paddle_size[1] // 2 < ball_position[1]:
                direction2 = 'DOWN'
            elif paddle2_position[1] + paddle_size[1] // 2 > ball_position[1]:
                direction2 = 'UP'
            elif paddle2_position[1] + paddle_size[1] // 2 == ball_position[1]:
                direction2 = None
        else:
            if paddle2_position[1] < window_y // 2:
                direction2 = 'DOWN'
            elif paddle2_position[1] > window_y // 2:
                direction2 = 'UP'
            else:
                direction2 = None
    if Cpu2:

        #basic machine learning linear regression to predict whether to go up or down based on position
        #data of paddle y value and data of ball y value in a list
        training_data = [[400, 300], [200, 300], [150, 50], [250, 350], [440, 400], [200, 250], [200, 150], [100, 200]]
        target_values = [0, 1, 0, 1, 0, 1, 0, 1]
        #target values is the prediction
        model = LogisticRegression()
        model.fit(training_data, target_values)

        paddle_center = paddle1_position[1] + paddle_size[1] / 2
        ball_center = ball_position[1] + ball_size[1] / 2
        if ball_position[0] <= window_x / 2:
            prediction = model.predict([[paddle_center, ball_center]])
            #print('input: [{}, {}], prediction: {}'.format(paddle_center, ball_center, prediction))
            if prediction == 0:
                if ballYM < 0:
                    direction = 'W'
                else:
                    direction = None
            if prediction == 1:
                if ballYM > 0:
                    direction = 'S'
                else:
                    direction = None
        else:
            if paddle_center <= window_y / 3.5:
                if ballYM < 0:
                    direction = None
                else:
                    direction = 'S'
            elif paddle_center >= window_y - window_y / 3.5:
                if ballYM > 0:
                    direction = None
                else:
                    direction = 'W'

        print(direction)



    #if the game is paused, prevent the paddles from moving
    if gamePause:
        direction = None
        direction2 = None


    #if the direction of each paddles is set to a corresponding direction, check if the current
    # y position of the paddles is not beyond the top or bottom side of the window and prevent them from moving
    #if not move the paddles by the corresponding direction by 10 units
    if direction2 == 'UP':
        if paddle2_position[1] == 0:
            paddle2_position[1] += 0
        else:
            paddle2_position[1] -= 10
    if direction2 == 'DOWN':
        if paddle2_position[1] == 440:
            paddle2_position[1] -= 0
        else:
            paddle2_position[1] += 10
    if direction == 'W':
        if paddle1_position[1] == 0:
            paddle1_position[1] += 0
        else:
            paddle1_position[1] -= pad1Speed
    if direction == 'S':
        if paddle1_position[1] == 440:
            paddle1_position[1] -= 0
        else:
            paddle1_position[1] += pad1Speed


    #if the ball hits the side of the screen then its trajectory is reflected and goes the other way
    if ball_position[1] < 5:
        ballYM = (ballYM * -1) + (random.randint(1, 10) / 10)
    if ball_position[1] > 465:
        ballYM = 0 - ballYM - (random.randint(1, 10) / 10)
    if ball_position[0] < 0:
        ballXM = (ballXM * -1) + (random.randint(1, 10) / 10)
    if ball_position[0] > 705:
        ballXM = 0 - ballXM - (random.randint(1, 10) / 10)


    #if the ball collides with the left paddle based on position, then its horizontal trjectory is reversed and goes the other way
    if paddle_size[0] + 25 >= ball_position[0] > 25:
        if ball_position[1] >= paddle1_position[1] - 5 and ball_position[1] <= paddle1_position[1] + paddle_size[1] + 5:
            ballXM = (ballXM - (random.randint(1, 10) / 10)) * -1
    #if the ball collides with the right paddle based on position, then its horizontal trajectory is reversed and goes the other way
    if ball_position[0] >= 720 - 25 - paddle_size[0] and ball_position[0] < 720 - 25:
        if ball_position[1] >= paddle2_position[1] - 5 and ball_position[1] <= paddle2_position[1] + paddle_size[1] + 5:
            ballXM = (0 - ballXM) - (random.randint(1, 10) / 10)


    #if the game is not paused and game is started, then the ball can start moving at a certain momentum of x and y values
    if not gamePause:
        if gameStart:
            ball_position[0] += ballXM
            ball_position[1] += ballYM
        else:
            #if the game is not paused and the game is not started, then the ball is reset
            ball_position = resetBall()


    #if the ball reaches the left side of the screen past the paddle, then the ball position is reset for another round and player 2 is given a point
    if ball_position[0] < 10:
        ball_position = resetBall()
        p2score += 1
        gameStart = False
    #if the ball reaches the right side of the sceen past the paddle, then the ball position is reset for another round and player 1 is given a point
    if ball_position[0] > 705:
        ball_position = resetBall()
        p1score += 1
        gameStart = False


    # fills the screen background as black
    game_window.fill(black)
    hi = True
    if hi:
        #determines whether or not the game is tied
        if p1score == 10 and p2score == 10 and tie == False:
            tie = True
        #based on if the game is tied at 10 or not it will determine the winner
        #if tied and a player lead by 2 then that player wins
        if tie:
            if p1score > p2score and p1score - p2score == 2:
                win('Player 1')
                WON = True
            elif p2score > p1score and p2score - p1score == 2:
                win('Player 2')
                WON = True
        #if not tied and a player scores 11, the person then wins
        elif p1score == 11:
            win('Player 1')
            WON = True
        elif p2score == 11:
            win('Player 2')
            WON = True




    #if the game should be paused then display the pause menu
    if gamePause:
        pause()
    #if the game/round has not started and no one has one then display the start menu that shows how to start the game
    if not gameStart:
        if not WON:
            start()



    #showing score, paddles, and ball
    showScore()
    pygame.draw.rect(game_window, white, pygame.Rect(paddle2_position[0], paddle2_position[1], paddle_size[0], paddle_size[1]))
    pygame.draw.rect(game_window, white, pygame.Rect(paddle1_position[0], paddle1_position[1], paddle_size[0], paddle_size[1]))
    pygame.draw.rect(game_window, white, pygame.Rect(ball_position[0], ball_position[1], ball_size[0], ball_size[1]))
    #pygame.draw.rect(game_window, green, pygame.Rect(ball_clone[0], ball_clone[1], ball_size[0], ball_size[1]))
    #updating the image
    pygame.display.update()
    #framerate
    fps.tick(paddle_speed)


#trying to simulate a cloned ball that is a few steps ahead of the current ball to predict it
"""""
    if ball_position[0] > window_x // 2:

        if change:
            ball_clone = [ball_position[0], ball_position[1]]
            ball_cloneX = getnum(ballXM)
            ball_cloneY = getnum(ballYM)
            change = False

        if ball_clone[1] < 5:
            ball_cloneY = (ball_cloneY * -1) + (random.randint(1, 10) / 10)
        if ball_clone[1] > 465:
            ball_cloneY = 0 - ball_cloneY - (random.randint(1, 10) / 10)
        if ball_clone[0] < 0:
            ball_cloneX = (ball_cloneX * -1) + (random.randint(1, 10) / 10)
        if ball_clone[0] > 705:
            ball_cloneX = 0 - ball_cloneX - (random.randint(1, 10) / 10)

        ball_clone[0] += ball_cloneX * 1.04
        ball_clone[1] += ball_cloneY * 1.04
    else:
        change = True
"""""
#normal fuctioning computer for cpu 2
"""
    if Cpu2:
        if ball_position[0] < window_x // 2 + window_x // 3:
            paddle_center = paddle1_position[1] + paddle_size[1] / 2
            ball_center = ball_position[1] + ball_size[1] / 2
            distance = abs(paddle_center - ball_center)
            if distance > 20 and paddle_center < ball_center:
                direction = 'S'
            elif distance < 20 and paddle_center > ball_center:
                direction = 'W'
            else:
                direction = None
        else:
            if paddle1_position[1] < window_y // 2:
                direction = 'S'
            elif paddle1_position[1] > window_y // 2:
                direction = 'W'
            else:
                direction = None
"""