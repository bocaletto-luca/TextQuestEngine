from engine.core.game import Game

def main():
    game = Game()
    game.load_world('config/world.yaml')
    game.run()

if __name__ == '__main__':
    main()
