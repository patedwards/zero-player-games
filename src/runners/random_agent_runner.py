# pylint: disable-all

from environments.random_walkers import RandomWalkers

def main():
    
    env = RandomWalkers(10, render_mode="human")

    for _ in range(1000):
        env.step(None)

if __name__ == "__main__":
    main()