import gui      
import os
from loguru import logger

if __name__ == "__main__":
    try:
        game = gui.GAME();
        game.run();
    except Exception as e:
        logger.error(f"{e}");
