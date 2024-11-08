import pygame as pg
import config as cfg
import sys
from random import randint
from loguru import logger

class GAME:
    def __init__(self) -> None:
        pg.init();
        pg.mixer.init();
        self.screen = pg.display.set_mode((cfg.WIDTH, cfg.HEIGHT));
        pg.display.set_caption('THE SPACE SHOOTER');
        self.clock=pg.time.Clock();

        self.running: bool = True;
        self.playing: bool = False;
        self.alien_spawn_timer: int = 0;
        self.aliens: list = [];
        self.bullets: list = [];
        self.bullet_cd: int = 0;
        self.score: int = 0;

        self.background = pg.image.load("../resources/images/space_background.jpg");
        self.background = pg.transform.scale(self.background, (cfg.WIDTH, cfg.HEIGHT));
        self.font = pg.font.SysFont('../resources/fonts/FiraCodeNerdFont-Regular.ttf', 50);
        self.text_score = self.font.render(f'Score: {self.score}', True, (255, 255, 255));

        self.player = PLayer();

    def run(self) -> None:
        logger.info("running...");
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    logger.warning("closing the program");
                    self.running = False;
                    sys.exit();

            self.update();
            self.draw();
            pg.display.flip();
            self.clock.tick(cfg.FPS);
        pg.quit();

    def update(self) -> None:
        self.player.update();

        self.alien_spawn_timer += 1
        if self.alien_spawn_timer >= cfg.ALIEN_SPAWN_RATE:
            self.aliens.append(Alien());
            self.alien_spawn_timer = 0;

        for alien in self.aliens:
            alien.update()
            if alien.rect.bottom > cfg.HEIGHT - 1:
                self.aliens.remove(alien);
                print("GAME OVER");
                logger.warning("closing the program");
                self.running = False;
                sys.exit()

        if self.bullet_cd > 0:
            self.bullet_cd -= 1;

        keys = pg.key.get_pressed();
        if keys[pg.K_SPACE] and self.bullet_cd <= 0:
            self.bullets.append(Bullet(x=self.player.rect.centerx, y=self.player.rect.top));
            self.bullet_cd = cfg.LASER_CD;

        for bullet in self.bullets[:]:
            bullet.update();
            if bullet.rect.y < 1:
                self.bullets.remove(bullet);

        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.aliens.remove(alien);
                    self.bullets.remove(bullet);
                    self.score += 1;
                    self.text_score = self.font.render(f"Score: {self.score}", True, (255, 255, 255));
                    logger.info(f"updated self.text_score -> {self.score}");
                    break;

    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0));
        self.player.draw(self.screen);
        self.screen.blit(self.text_score, (5, 5));
        for alien in self.aliens:
            alien.draw(self.screen);
        for bullet in self.bullets:
            bullet.draw(self.screen);


class PLayer(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__();
        self.image = pg.image.load("../resources/images/space_ship.png");
        self.rect = self.image.get_rect();
        self.rect.centerx = cfg.WIDTH // 2;
        self.rect.bottom = cfg.HEIGHT - 10;

    def update(self) -> None:
        keys = pg.key.get_pressed();
        if keys[pg.K_a]: self.rect.x -= cfg.SHIP_VEL;
        if keys[pg.K_d]: self.rect.x += cfg.SHIP_VEL;
        if keys[pg.K_w]: self.rect.y -= cfg.SHIP_VEL;
        if keys[pg.K_s]: self.rect.y += cfg.SHIP_VEL;

        self.rect.left = max(0, self.rect.left);
        self.rect.right = min(cfg.WIDTH, self.rect.right);
        self.rect.top = max(0, self.rect.top);
        self.rect.bottom = min(cfg.HEIGHT, self.rect.bottom);

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect);


class Alien(pg.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__();
        self.image = pg.image.load("../resources/images/alien_ship.png");
        self.rect = self.image.get_rect();
        self.rect.centerx = randint(0, cfg.WIDTH);
        self.rect.bottom = 0;

    def update(self) -> None:
        self.rect.y += cfg.ALIEN_VEL;

        if (self.rect.bottom > cfg.HEIGHT):
            self.kill();

        self.rect.left = max(0, self.rect.left);
        self.rect.right = min(cfg.WIDTH, self.rect.right);
        self.rect.top = max(0, self.rect.top);
        self.rect.bottom = min(cfg.HEIGHT, self.rect.bottom);

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect);


class Bullet(pg.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__();
        self.image = pg.image.load("../resources/images/laser_particle.png");
        self.rect = self.image.get_rect();
        self.rect.centerx = x;
        self.rect.bottom = y;

    def update(self) -> None:
        self.rect.y -= cfg.LASER_VEL;

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect);


