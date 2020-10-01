#SHMUP

import pygame
import random
from os import path
img_dir = path.join(path.dirname(__file__),"data\img")
snd_dir = path.join(path.dirname(__file__),"data\snd")


W=480
H=600
FPS=60


WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(0,0,255)
RED=(255,0,0)
GREEN=(0,255,0)
BUL= (255,125,125)

#initialising modules
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((W,H))
player_img =  pygame.image.load(path.join(img_dir,"player.png")).convert()
pygame.display.set_icon(player_img)
pygame.display.set_caption("SHMUP GAME")
clock=pygame.time.Clock()

#loading images
player_img =  pygame.image.load(path.join(img_dir,"player.png")).convert()
mob_img =  pygame.image.load(path.join(img_dir,"enemy.png")).convert()
bullet_img =  pygame.image.load(path.join(img_dir,"bullete.png")).convert()

#for texts in game
font_name = pygame.font.match_font('arial')

def draw_text (surface,text,size,x,y):
    font = pygame.font.Font(font_name,size)
    text_surface = font.render(text,True,WHITE) #for smoothness of font
    text_rect = text_surface.get_rect()
    text_rect.midtop =(int(x),int(y))
    surface.blit (text_surface,text_rect)

#draw health bar

def health_bar (surface,x,y,health):
    if health < 0:
        health=0
    BAR_LEN =100
    BAR_WID = 10
    outline_rect = pygame.Rect(x,y,BAR_LEN,BAR_WID)
    health_rect = pygame.Rect (x,y,health,BAR_WID)
    pygame.draw.rect(surface,GREEN,health_rect )
    pygame.draw.rect(surface,WHITE,outline_rect,2)

#new mob
def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#class player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,35))
        self.image.set_colorkey (BLACK)
        self.rect= self.image.get_rect()
        self.radius=20
        self.rect.centerx = round(W/2)
        self.rect.bottom = H-10 #10 from bottom
        self.speedx = 0
        self.speedy = 0
        self.health = 100
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.speedy =0
        keystat = pygame.key.get_pressed() #To make variable as keystat anytime when update runs and
                                            # pygame.key.get_pressed() is used for input
        if keystat[pygame.K_LEFT]: #this uses list of keys on board so [] is used
            self.speedx = -5
        if keystat[pygame.K_RIGHT]:
            self.speedx = 5
        if keystat[pygame.K_UP]: #this uses list of keys on board so [] is used
            self.speedy = -5
        if keystat[pygame.K_DOWN]:
            self.speedy = 5
        if keystat[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > W:
            self.rect.right = W
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > H-10:
            self.rect.bottom = H-10
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - player.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullete=Bullet(self.rect.centerx,self.rect.top)
            all_sprites.add(bullete)
            bullets.add(bullete)
            shoot_sound.set_volume(0.3)
            shoot_sound.play()



#class enemy
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img, (50, 35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius=20
        self.rect.x = random.randrange(W - self.rect.width)
        self.rect.y = random.randrange(25)
        self.speedy = random.randrange(1,5)
        self.speedx= random.randrange(-2,2)


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top >= H + 20 or  self.rect.left < -25 or self.rect.right > W + 20:
            self.rect.x = random.randrange(W - self.rect.width)
            self.rect.y = random.randrange(25)
            self.speedy = random.randrange(1, 8)

# BUllets
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (10, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -15   # - is for upward

    def update(self):
        self.rect.y += self.speedy
        #kill if it moves up above window
        if self.rect.bottom < 0:
            self.kill()

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen,"SHMUP",64,int(W/2),int(H/4))
    draw_text(screen, " ~BY AJINKYA", 20, int(W *3/4), int(H / 4)+60)
    draw_text(screen,"Arrow keys to move and space to fire",30,int(W/2),int(H/2))
    draw_text(screen,"Press a key to start",20,int (W/2),int(H * 3/4))
    pygame.display.flip()
    waiting =True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

#sprites
all_sprites=pygame.sprite.Group()

player =Player()
all_sprites.add(player)

#load graphics
background = pygame.image.load(path.join(img_dir,"background.png")).convert()
background_rect = background.get_rect()
#load sounds
shoot_sound= pygame.mixer.Sound(path.join(snd_dir,"laser1.wav"))
mob_sound= pygame.mixer.Sound(path.join(snd_dir,"mob.wav"))
player_sound= pygame.mixer.Sound(path.join(snd_dir,"player.ogg"))
pygame.mixer.music.load(path.join(snd_dir,"background.mp3"))
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()


#enemy
mobs = pygame.sprite.Group()
for i in range(8): #no of mobs at a time
    newmob()

#Bullets
bullets = pygame.sprite.Group()

score=0
#Game loop
game_over = True
running=True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        mobs = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        bullets = pygame.sprite.Group()
        score = 0
    #Keep game run at right speed
    clock.tick(FPS)
    # EVENTS


    #to perform exit
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    #update
    all_sprites.update()

    # to check bullet hits mob
    hits = pygame.sprite.groupcollide(bullets,mobs,True,True)
    for hit in hits:
        score += 1
        mob_sound.set_volume(0.3)
        mob_sound.play()
        newmob()
    # check to see whether player hits mob
    hits = pygame.sprite.spritecollide(player,mobs ,True,pygame.sprite.collide_circle)
    for hit in hits:
        player.health -= 20
        player_sound.set_volume(0.3)
        player_sound.play()
        newmob()
    if player.health <=\
            0:
        screen.blit(background,background_rect)
        draw_text(screen,"Your score is  "+str(score)+"  Good game !!",40,int(W/2),int(H/2))
        pygame.display.flip()
        pygame.time.wait(1500)
        if event.type == pygame.KEYUP:
            game_over = True
    #draw or render

    screen.fill(BLACK)
    screen.blit (background,background_rect)
    all_sprites.draw(screen)
    #text
    draw_text(screen,str(score),40,W/2,10)
    health_bar(screen,15,15,player.health)

    #to refresh
    pygame.display.flip()

pygame.quit()

