import sys
import pygame
import random
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    def __init__(self):
        pygame.init()

        #Initialize the mixer for music
        pygame.mixer.init()
        
        # Load and play background music
        pygame.mixer.music.load('audio/spacemusic.mp3')  # Ensure the file is in the 'audio' folder
        pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Loop the music indefinitely
        
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Set a default ship image
        self.ship_image = "ship.png"  # Default ship image

        # Load and scale the background image
        self.background = pygame.image.load('images/background.png')
        self.background = pygame.transform.scale(self.background, (self.settings.screen_width, self.settings.screen_height))

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        
        # Score attributes
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)
        
        # Lives attribute
        self.lives = self.settings.ships_left
        
        # Game state flags
        self.game_active = False
        self.game_paused = False  # Add a flag to track if the game is paused
    
    def show_start_menu(self):    
        """Display the start menu with instructions and ship selection."""
        title_font = pygame.font.SysFont(None, 72)
        text_font = pygame.font.SysFont(None, 48)

        # Title
        title_text = title_font.render("Alien Invasion", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 10))

        # Instructions
        instructions = [
            "Instructions:",
            "Arrow keys to move the ship",
            "Spacebar to shoot bullets",
            "Press 'Q' to quit the game",
            "Press 'Enter' to start",
            "Press 'P' to pause/unpause",
            "Use 'Up' and 'Down' to select your ship",
            "Press 'Enter' to confirm your ship selection"
        ]
        start_y = self.settings.screen_height // 5  # Adjusted starting position for instructions
        line_spacing = 30  # Spacing between instruction lines

        # Ship selection
        ships = {
            "ship.png": "Blue Ship",
            "shipg.png": "Green Ship",
            "shipo.png": "Orange Ship",
            "shipr.png": "Red Ship"
        }
        ship_keys = list(ships.keys())
        selected_index = 0

        while not self.game_active:
            self.screen.fill((0, 0, 0))  # Clear the screen
            self.screen.blit(title_text, title_rect)  # Draw the title

            # Draw instructions
            for i, line in enumerate(instructions):
                instruction_text = text_font.render(line, True, (255, 255, 255))
                instruction_rect = instruction_text.get_rect(center=(self.settings.screen_width // 2, start_y + i * line_spacing))
                self.screen.blit(instruction_text, instruction_rect)

            # Display ship options
            ship_start_y = start_y + len(instructions) * line_spacing + 50  # Start ship options below instructions
            for i, ship_key in enumerate(ship_keys):
                color = (255, 255, 0) if i == selected_index else (255, 255, 255)
                ship_text = text_font.render(ships[ship_key], True, color)
                ship_rect = ship_text.get_rect(center=(self.settings.screen_width // 2, ship_start_y + i * 40))
                self.screen.blit(ship_text, ship_rect)

            pygame.display.flip()  # Update the screen

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_index = (selected_index - 1) % len(ship_keys)
                    elif event.key == pygame.K_DOWN:
                        selected_index = (selected_index + 1) % len(ship_keys)
                    elif event.key == pygame.K_RETURN:  # Confirm selection
                        self.ship_image = ship_keys[selected_index]
                        self.game_active = True
                        
    def _create_fleet(self):
        """Create a fleet of aliens."""
        alien_images = ["alien.png", "alienb.png", "alienr.png", "alieny.png"]  # List of alien images
        alien_width, alien_height = Alien(self, alien_images[0]).rect.size  # Use the first image to get dimensions

        # Adjust the available space to fit more aliens
        available_x_space = self.settings.screen_width - 2 * alien_width
        available_y_space = self.settings.screen_height - 3 * alien_height  # Reduced top and bottom padding

        # Ensure the number of rows and columns is valid
        number_aliens_x = max(1, available_x_space // int(1.5 * alien_width))  # Use integer division
        number_rows = max(1, available_y_space // int(1.5 * alien_height))  # Use integer division

        for row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_width + 1.5 * alien_width * alien_number,
                                   alien_height + 1.5 * alien_height * row)
                
    def _create_alien(self, x_position, y_position):
        """Create an alien with a random image and add it to the fleet."""
        alien_images = ["alien.png", "alienb.png", "alienr.png", "alieny.png"]  # List of alien images
        selected_image = random.choice(alien_images)  # Randomly select an image
                
        """Create an alien and add it to the fleet."""
        new_alien = Alien(self, selected_image)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        
        self.aliens.add(new_alien)
        
    def run_game(self):
        self.show_start_menu()  # Show the start menu before starting the game

        # Initialize the ship after the user selects a ship
        self.ship = Ship(self)

        while True:
            self._check_events()
            
            if self.game_active and not self.game_paused:
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
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:  # Toggle pause
            self.game_paused = not self.game_paused
    
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
        self._check_fleet_edges()
        self.aliens.update()
        
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _check_ship_alien_collision(self):
        """Check if an alien collides with the ship."""
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.lives -= 1
            if self.lives <= 0:
                self.game_active = False
            else:
                # Restore the ship to its starting position without resetting aliens
                self.ship.center_ship()
                self.bullets.empty()  # Clear bullets to avoid immediate collisions
                pygame.time.delay(500)  # Add a short delay for better gameplay experience
    
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
        """Update images on the screen and flip to the new screen."""
        # Draw the background image
        self.screen.blit(self.background, (0, 0))  # Draw the background image at the top-left corner
        
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
        
        if self.game_paused:  # Display "Paused" message
            paused_text = self.font.render("PAUSED", True, (255, 255, 0))
            self.screen.blit(paused_text, (self.settings.screen_width // 2 - 50, self.settings.screen_height // 2))

        pygame.display.flip()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
