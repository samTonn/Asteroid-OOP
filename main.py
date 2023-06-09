import pygame, sys, random


#Class Definitions
class Ship(pygame.sprite.Sprite):
  def __init__(self,groups):
    super().__init__(groups)
    self.image = pygame.image.load("Sprites/player.png").convert_alpha()
    self.image_to_rotate = self.image
    self.rect = self.image.get_rect(center =(SCREEN_W/2,SCREEN_H/2))
    self.position = pygame.Vector2(SCREEN_W/2,SCREEN_H/2)
    self.velocity = pygame.Vector2(0,0)
    self.forward_speed = 2
    self.rotation_amount = 2
    self.current_direction = pygame.Vector2(0,-1)
    #New Attributes############################################
    self.can_shoot = True
    self.cooldown_time = None
  
  def ship_acceleration(self):
    if abs(self.velocity.x) < 50 and abs(self.velocity.y) < 50:
      self.velocity += self.current_direction *  self.forward_speed
    

    
  def ship_rotation(self, clockwise = True):
    sign = 1 if clockwise else -1
    angle = self.rotation_amount*sign
    self.current_direction.rotate_ip(angle)
  
  def ship_controls(self):
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_a]:
      self.ship_rotation(False)
    if keystate[pygame.K_d]:
      self.ship_rotation(True)
    if keystate[pygame.K_w]:
      self.ship_acceleration()
    if not keystate[pygame.K_w]:
      self.ship_drag()

  def screen_wrap(self):
    x, y = self.position
    self.position = pygame.Vector2(x % SCREEN_W, y % SCREEN_H)

  def move(self):
    self.screen_wrap()
    self.position = self.position + self.velocity

  def ship_drag(self):
    drag = 0.98
    self.velocity.y *= drag
    self.velocity.x *= drag
  #New Methods################################################
  def laser_cooldown(self):
    if not self.can_shoot:
      current_time = pygame.time.get_ticks()
      if current_time - self.cooldown_time > 500:
        self.can_shoot = True

  def laser_shoot(self):
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_SPACE] and self.can_shoot:
      angle = self.current_direction.angle_to((0,-1))
      
      self.can_shoot = False
      self.cooldown_time = pygame.time.get_ticks()
      Laser(self.position, angle, laser_group)
        
  def update(self):
    self.laser_cooldown()
    self.laser_shoot()
    self.ship_controls()
    self.move()
    self.debugRect()
  
  def draw(self,surface):
    angle = self.current_direction.angle_to((0,-1))
    self.image = pygame.transform.rotozoom(self.image_to_rotate, angle, 1.0)
    rotated_surface_size = pygame.Vector2(self.image.get_size())
    blit_position = self.position - rotated_surface_size * 0.5
    surface.blit(self.image, blit_position)

  def debugRect(self):
    self.rect.center = self.position
    pygame.draw.rect(display_surface, "red", self.rect)

class Laser(pygame.sprite.Sprite):
  def __init__(self, position, angle, groups):
    super().__init__(groups)
    self.image = pygame.image.load("Sprites/effect_purple.png").convert_alpha()
    self.image_og = self.image
    self.rect = self.image.get_rect(center = position)
    self.position = pygame.math.Vector2(self.rect.center)
    self.direction = pygame.math.Vector2(ship.current_direction)
    self.angle = angle
    self.speed = 2


  def debugRect(self):
    self.rect.center = self.position
    pygame.draw.rect(display_surface, "red", self.rect)

  def move(self):
    self.image = pygame.transform.rotozoom(self.image_og, self.angle, 1.0)
    self.position += self.direction*dt*50000
    self.rect.center = (round(self.position.x),round(self.position.y))
    
    #Laser Update
  def update(self):
    self.move()
    self.debugRect()

class Asteroid(pygame.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.img_list = ["Sprites/asteroid-L.png", "Sprites/asteroid-LD.png", "Sprites/asteroid-S.png", "Sprites/asteroid-SD.png"]
    #self.image = pygame.image.load(self.img_list[random.randint(0, (self.img_list.len() - 1))]).convert_alpha()
    self.position = pygame.math.Vector2(random.randint(-50, SCREEN_W + 50),-50)
    self.rect = self.image.get_rect(center = self.position)
    self.direction = pygame.math.Vector2(random.randint(-10,10)/10 , 1)
    self.speed = 800
  
  def fall(self):
    self.position += self.direction*self.speed*dt
    self.rect.center = (round(self.position.x),round(self.position.y))
    if self.position.y > SCREEN_H:
      self.kill()

  def debugRect(self):
    self.rect.center = self.position
    pygame.draw.rect(display_surface, "red", self.rect)
  
  def update(self):
    self.fall()
    #self.debugRect()
    
#Game Setup
    
pygame.init()
pygame.display.set_caption('Asteroid Clone - OOP')
SCREEN_W, SCREEN_H = 1280, 720 
display_surface = pygame.display.set_mode((SCREEN_W, SCREEN_H),pygame.FULLSCREEN)
clock = pygame.time.Clock()

#Game Files
background = pygame.image.load("Sprites/background.png").convert()

#Game Sprites
spaceship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
asteroid_group = pygame.sprite.Group()
ship = Ship(spaceship_group)


#Main Game Loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  #Primary Background
  display_surface.blit(background,(0,0))

  #Delta Time - Managing Velocity and FR
  dt = clock.tick() / 1000

  #Updates
  ship.update()
  laser_group.update()
  
  if (random.randint(1,500) == 1): #spawn rate; increase to decrease rate
    Asteroid(asteroid_group)
    
  asteroid_group.update()
  #Draw Call - Sprites
  ship.draw(display_surface)
  laser_group.draw(display_surface)
  asteroid_group.draw(display_surface)
	#Draw Call - Final
  pygame.display.update()
