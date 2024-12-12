import pygame
import random
import math

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * 9/16)

black = pygame.color.Color('black')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('particle system test')

clock = pygame.time.Clock()
FPS = 120



def draw_text(text, size, text_color, x, y):
    font = pygame.font.SysFont('Arial', size)
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

def randomNum(max, min):
    return random.randint(max, min)
    

def randomColor():
    return pygame.color.Color(randomNum(0, 255), randomNum(0, 255), randomNum(0, 255))


class Ball:
    def __init__(self, x, y, velX, velY, color, size):
        self.x = x
        self.y = y
        self.velX = velX
        self.velY = velY
        self.color = color
        self.size = size
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)
        
    def update(self):
        if (self.x + self.size) >= SCREEN_WIDTH:
            self.velX = -(self.velX)  
            
        if (self.x + self.size) <= 0:
            self.velX = -(self.velX)
            
        if (self.y + self.size) >= SCREEN_HEIGHT:
            self.velY = -(self.velY)
            
        if (self.y + self.size) <= 0:
            self.velY = -(self.velY)
            
        self.x += self.velX
        self.y += self.velY
        
    def collisionDetection(self, balls):
        for ball in balls:
            if self != ball:
                dx = self.x - ball.x
                dy = self.y - ball.y
                distance = math.sqrt((dx**2 + dy**2))
                min_distance = self.size + ball.size

                
                if distance < min_distance:
                    
                    overlap = min_distance - distance
                    angle = math.atan2(dy, dx)
                    self.x += math.cos(angle) * (overlap / 2)
                    self.y += math.sin(angle) * (overlap / 2)
                    ball.x -= math.cos(angle) * (overlap / 2)
                    ball.y -= math.sin(angle) * (overlap / 2)

                    
                    normal = (dx / distance, dy / distance)
                    tangent = (-normal[1], normal[0])

                    
                    self_normal_velocity = self.velX * normal[0] + self.velY * normal[1]
                    ball_normal_velocity = ball.velX * normal[0] + ball.velY * normal[1]
                    self_tangent_velocity = self.velX * tangent[0] + self.velY * tangent[1]
                    ball_tangent_velocity = ball.velX * tangent[0] + ball.velY * tangent[1]

                    
                    self_normal_velocity, ball_normal_velocity = ball_normal_velocity, self_normal_velocity

                    
                    self.velX = self_tangent_velocity * tangent[0] + self_normal_velocity * normal[0]
                    self.velY = self_tangent_velocity * tangent[1] + self_normal_velocity * normal[1]
                    ball.velX = ball_tangent_velocity * tangent[0] + ball_normal_velocity * normal[0]
                    ball.velY = ball_tangent_velocity * tangent[1] + ball_normal_velocity * normal[1]
                

balls = []
createBall = False

def makeBalls(sizeMin, sizeMax):
    if createBall:
        size = randomNum(sizeMin, sizeMax)
        mousePos = pygame.mouse.get_pos()
        ball = Ball(
            mousePos[0],
            mousePos[1], 
            randomNum(-7, 7), 
            randomNum(-7, 7), 
            randomColor(), 
            size, 
            
        )
        
        balls.append(ball)
        
def changeFPS(type):
    global FPS
    if type == 'increase':
        if FPS < 420:
            FPS += 30
    elif type == 'decrease':
        if FPS > 30:
            FPS -= 30
        
        
        

run = True
while run:
    clock.tick(FPS)
    
    screen.fill("white")
    makeBalls(5, 15)
    
    
    for ball in balls:
        ball.draw()
        ball.update()
        ball.collisionDetection(balls)
    
    draw_text(f"Ball count: {len(balls)}", 20, black, 0, 0)
    draw_text(f"Simulation speed: {str(FPS)}", 20, black, 0, 20)
    draw_text("\'Up\' arrow key to speed up simulation", 14, black, 0, SCREEN_HEIGHT - 40)
    draw_text("\'Down\' arrow key to speed up simulation", 14, black, 0, SCREEN_HEIGHT - 20)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                run = False
                
            if event.key == pygame.K_UP:
                changeFPS("increase")
                
            if event.key == pygame.K_DOWN:
                changeFPS("decrease")

                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                createBall = True
                
                
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                createBall = False
                
                
                
    pygame.display.update()
    
pygame.quit()