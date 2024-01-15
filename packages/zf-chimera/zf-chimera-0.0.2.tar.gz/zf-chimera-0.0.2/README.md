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

## Parameters

You can control the simulation by changing parameter which will affect the spread of the idea.

### Transmission Rate

The transmission rate is the probability that an agent will be infected by another agent.
The argument name is `--rate` and its default value is set to 0.5.

For the following tables, the initial infected is set to 1 while varying the transmission rate.

<table>
<tr>
<td>
    <h4>Rate = 0.3</h4>
    <img src="./data/Anim_1.gif" width="250px" alt="rate_0.5">
</td>
<td>
    <h4>Rate = 0.5</h4>
    <img src="./data/Anim_2.gif" width="250px" alt="rate_1.0">
</td>
<td>
    <h4>Rate = 1.0</h4>
    <img src="./data/Anim_3.gif" width="250px" alt="rate_1.0">
</td>
</tr>
</table>

### Initial Infected

The initial infected is the number of agents that will be infected at the start of the simulation.
The argument name is `--infected` and its default value is set to 1.

For the following examples, the transmission rate is set to 0.5 while varying the initial infected.

<table>
<tr>
<td>
    <h4>Infected = 1</h4>
    <img src="./data/Infected_1.gif" width="250px" alt="rate_0.5">
</td>
<td>
    <h4>Infected = 3</h4>
    <img src="./data/Infected_3.gif" width="250px" alt="rate_1.0">
</td>
<td>
    <h4>Infected = 5</h4>
    <img src="./data/Infected_5.gif" width="250px" alt="rate_1.0">
</td>
</tr>
</table>

### Geographic Radius

The geographic radius is the distance that an agent can transmit the idea to another agent.

For the following examples, both the transmission rate and initial infected are set to 1 while varying the geographic
radius.

<table>
<tr>
<td>
    <h4>Radius = 1</h4>
    <img src="./data/Radius_1.gif" width="250px" alt="rate_0.5">
</td>
<td>
    <h4>Radius = 3</h4>
    <img src="./data/Radius_3.gif" width="250px" alt="rate_1.0">
</td>
<td>
    <h4>Radius = 5</h4>
    <img src="./data/Radius_5.gif" width="250px" alt="rate_1.0">
</td>
</tr>
</table>

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