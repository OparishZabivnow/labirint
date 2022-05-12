
from turtle import right
from pygame import *

display.set_caption("LABIRINT")

win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
fon = image.load('fon.jpg')
fon = transform.scale(fon,(win_width, win_height))

class Game_sprite (sprite.Sprite):
    def __init__(self,picture, wight, height, x,y ):
        super().__init__()
        self.image = transform.scale(image.load(picture),(wight, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x , self.rect.y))


class Player(Game_sprite):
    def __init__(self,picture, width,height,x,y,x_speed,y_speed):
        Game_sprite.__init__(self,picture, width,height,x,y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def reset(self):
        window.blit(self.image,(self.rect.x , self.rect.y))
    def update(self):
        if player.rect.x <= win_width - 75 and player.x_speed>0 or player.rect.x >= 0 and player.x_speed < 0:
            self.rect.x += self.x_speed
        platfort_touch = sprite.spritecollide(self,barriers,False)
        if self.x_speed > 0:
            for p in platfort_touch:
                self.rect.right = min(self.rect.right, p.rect.left )
        elif self.x_speed < 0:
            for p in platfort_touch:
                self.rect.left = max(self.rect.left, p.rect.right )
        
        if player.rect.y <= win_height-75 and player.y_speed>0 or player.rect.y >=0 and player.y_speed <0:
            self.rect.y += self.y_speed
        platfort_touch = sprite.spritecollide(self,barriers,False)
        if self.y_speed > 0:
            for p in platfort_touch:
                self.rect.bottom = min(self.rect.bottom, p.rect.top )
        elif self.y_speed < 0:
            for p in platfort_touch:
                self.rect.top = max(self.rect.top, p.rect.bottom )
    def fire(self):
        bullet = Bullet('bullete (2).png', self.rect.right, self.rect.centery-11, 20, 10, 15)
        bullets.add(bullet)        

class Enemy(Game_sprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y,player_speed):
        Game_sprite.__init__(self,player_image,player_x,player_y,size_x,size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = "right"
        if self.rect.x >= win_width-85:
            self.side = 'left'
        
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
class Bullet(Game_sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        #Game_sprite.__init__(self, player_image, player_x,player_y, size_x, size_y)
        Game_sprite.__init__(self, player_image,size_x,size_y,player_x,player_y)
        self.speed = player_speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width + 10:
            self.kill()



w1 = Game_sprite('stena.jpg',300,20,100,393)
w2 = Game_sprite('stena.jpg',300,20,500,200)
w3 = Game_sprite('stena.jpg',30,200,365,200)
w4 = Game_sprite('stena.jpg',30,200,365,400)

monster1 = Enemy('Sobaka_law.png',60,75,500,400, 5)
monster2 = Enemy('Sobaka_law.png',60,75,450,316, 5)
monster3 = Enemy('Sobaka_law.png',60,75,250,100, 5)

final_pop = Game_sprite('finih.png',60,75,640,426)

player = Player('playser.png',60,75,285,416,0,0)

bullets = sprite.Group()
monsters = sprite.Group()
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)

barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)

finish = False

run = True
while run:
    window.blit(fon,(0,0))

    barriers.draw(window)
 

    time.delay(60)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                player.x_speed=-10
            elif e.key == K_RIGHT:
                player.x_speed =10
            elif e.key == K_DOWN:
                player.y_speed =10
            elif e.key == K_UP:
                player.y_speed =-10
            elif e.key == K_0:
                player.fire()

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                player.x_speed =0
            elif e.key == K_RIGHT:
                player.x_speed =0
            elif e.key == K_DOWN:
                player.y_speed =0
            elif e.key == K_UP:
                player.y_speed =0

    if not finish:
        player.reset()
        player.update()
        bullets.update()
        final_pop.reset()
        bullets.draw(window)
        sprite.groupcollide(monsters, bullets, True,True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets,barriers,True,False)

        if sprite.spritecollide(player,monsters , False ):
            finish = True
            img = image.load('game_over.jpg')
            d = img.get_width() // img.get_height()
            window.fill((255,255,255))
            window.blit(transform.scale(img, (win_width, win_height)), (0,0))

        if sprite.collide_rect(player, final_pop):
            finish = True
            img = image.load('win.png')
            window.fill((255,255,255))
            window.blit(transform.scale(img, (win_width, win_height)), (0,0))


        display.update()

