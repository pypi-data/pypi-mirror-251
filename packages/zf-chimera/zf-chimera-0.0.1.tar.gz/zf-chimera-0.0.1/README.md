# Chimera

Chimera simulates the spread of ideas within a population.

## Installation

```bash
pip install zf-chimera
```

## Usage

```bash
$ chimera --help
usage: chimera [-h] [--population POPULATION] [--start START] [--infected INFECTED] [--radius RADIUS] [--spread SPREAD] [--steps STEPS]

Simulate the diffusion of innovations

options:
  -h, --help            show this help message and exit
  --population POPULATION
                        The population size of the society
  --model MODEL         The model to use (e.g. v1, v2)
  --start START         The style of the simulation (e.g. middle, random)
  --infected INFECTED   The number of initially infected (e.g. 1, 10)
  --radius RADIUS       The geographic radius of each agent (e.g. 5, 10)
  --spread SPREAD       The number of agents each agent will infect (e.g. 2, 7)
  --steps STEPS         The number of steps to simulate (e.g. 50, 100)
```

```bash
$ chimera
Running simulation for 50 steps with 3481 agents
```

![Simulation](./data/Figure_1.png)

## Questions

- How many friends does a person have?
- How many people does a person talk to?
- When do people act upon some information?
- How to model hierarchies and groups?
- How to model lateral communication?

## References

* [Going Critical, Kevin Simler](https://meltingasphalt.com/interactive/going-critical/)
* [Modeling the Spread of Ideas in Networked Environments, Benjamin Simpkins](https://eprints.soton.ac.uk/271104/1/AHFE_CCDM_Poster.pdf)
* [Network Diffusion, Michal Czuba](https://network-diffusion.readthedocs.io/en/latest/propagation_model_example.html#purpose-of-propagationmodel-module)
* [Modeling the Spread of Rumors in Networks, Sanjay Roberts](https://digitalccbeta.coloradocollege.edu/pid/coccc:17723/datastream/OBJ)
* [Meme, Wikipedia](https://en.wikipedia.org/wiki/Meme)