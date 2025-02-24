import pygame 

class Ship:
    def __init__(self, ai_game):
        # Initialize the ship and set its starting position
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('images/ship.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        # Store a float for the ship's horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def update(self):
        # Update the ship's position based on movement flags
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed  
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed  
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed  
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed  

        # Update rect object from self.x and self.y
        self.rect.x = int(self.x)  
        self.rect.y = int(self.y)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        """Center the ship on the screen after being hit."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)




