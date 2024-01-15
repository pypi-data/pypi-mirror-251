import argparse

from loguru import logger

from .society import Society


def main():
    parser = argparse.ArgumentParser(description='Simulate the diffusion of innovations')
    parser.add_argument('--model', type=str, default='v1', help='The model to use (e.g. v1, v2)')
    parser.add_argument('--population', type=int, default=3481, help='The population size of the society')
    parser.add_argument('--start', type=str, default='middle', help='The style of the simulation (e.g. middle, random)')
    parser.add_argument('--infected', type=int, default=1, help='The number of initially infected (e.g. 1, 5)')
    parser.add_argument('--radius', type=int, default=5, help='The geographic radius of each agent (e.g. 1, 4)')
    parser.add_argument('--spread', type=int, default=4, help='The number of agents each agent will infect (e.g. 2, 7)')
    parser.add_argument('--rate', type=float, default=0.5, help='The rate of diffusion (e.g. 0.5, 0.7)')
    parser.add_argument('--steps', type=int, default=500, help='The number of steps to simulate (e.g. 50, 100)')
    args = parser.parse_args()

    if args.infected > 1:
        args.start = 'random'

    logger.info(f"Simulating {args.steps} steps with {args.population} people")
    logger.info(f"Initial infected: {args.infected}")
    logger.info(f"Geographic radius: {args.radius}")
    logger.info(f"Diffusion spread: {args.spread}")
    logger.info(f"Diffusion rate: {args.rate}")

    s = Society(args=args)
    if args.model == 'v1':
        s.simulate_v1(steps=args.steps)
    else:
        logger.error(f"Unknown model: {args.model}")


if __name__ == "__main__":
    main()
