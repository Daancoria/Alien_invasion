import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.bg_color = (0, 0, 0)  # Change background to dark
        
        # Score attributes
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)
        
        # Lives attribute
        self.lives = self.settings.ships_left
        
        # Game over flag
        self.game_active = True

    def _create_fleet(self):
        """Create a fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_x_space = self.settings.screen_width - 2 * alien_width
        available_y_space = self.settings.screen_height - 4 * alien_height
        
        number_aliens_x = available_x_space // (2 * alien_width)
        number_rows = available_y_space // (2 * alien_height)
        
        for row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_width + 2 * alien_width * alien_number, 
                                   alien_height + 2 * alien_height * row)
    
    def _create_alien(self, x_position, y_position):
        """Create an alien and add it to the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        
        self.aliens.add(new_alien)

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._check_collisions()
                self._check_ship_alien_collision()
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def _check_keydown_events(self, event):
        """Respond to key presses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_r and not self.game_active:
            self._restart_game()
        elif event.key == pygame.K_q:
            sys.exit()
    
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    
    def _fire_bullet(self):
        """Fire a bullet if limit is not reached."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        """Update bullet positions and remove old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
    
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()
    
    def _check_ship_alien_collision(self):
        """Check if an alien collides with the ship."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.lives -= 1
            if self.lives <= 0:
                self.game_active = False
            else:
                self._restart_round()
    
    def _check_collisions(self):
        """Check for bullet-alien collisions and remove them."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            self.score += len(collisions) * 10
        
        # If all aliens are destroyed, create a new fleet
        if not self.aliens:
            self._create_fleet()
    
    def _restart_game(self):
        """Restart the game after losing."""
        self.game_active = True
        self.lives = self.settings.ships_left
        self.score = 0
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
    
    def _restart_round(self):
        """Restart the round without resetting score."""
        self.aliens.empty()
        self.bullets.empty()
        self._create_fleet()
        self.ship.center_ship()
    
    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien in self.aliens.sprites():
            alien.blitme()
        self.ship.blitme()
        
        # Draw score and lives
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = self.font.render(f"Lives: {self.lives}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (self.settings.screen_width - 150, 10))
        
        if not self.game_active:
            game_over_text = self.font.render("GAME OVER! Press 'R' to Restart", True, (255, 0, 0))
            self.screen.blit(game_over_text, (self.settings.screen_width // 4, self.settings.screen_height // 2))
        
        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
