class Settings:
    def __init__(self):
        """Initialize game settings."""
        #Lives function 
        self.ships_left = 3  # Number of lives for the player

        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed = 6.2

        # Alien settings
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

    

        # Bullet settings
        self.bullet_speed = 5.0  # Fixed incorrect attribute reference
        self.bullet_width = 3  # Fixed incorrect attribute reference
        self.bullet_height = 35
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 20

        
        
    
