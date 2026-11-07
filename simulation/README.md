# Description
This directory contains code for simulation of protests.

## The model

Agents are the nodes of a social network (any `networkx` graph). Each agent is in one of three states:

| State      | Meaning                                    |
|------------|--------------------------------------------|
| `inactive` | not currently willing to protest           |
| `standby`  | privately willing to protest, for a limited time |
| `active`   | publicly protesting                        |

There are two global parameters:

- **p**: the probability per timestep that an inactive agent moves to standby.
- **T**: the most timesteps an agent can stay in standby without becoming active.

An agent counts a neighbor as **willing** if that neighbor is in standby or active.

Each timestep, all agents update at the same time:

1. **Coin flip.** Each inactive agent moves to standby with probability `p`.
2. **Threshold check.** Using the states after step 1:
   - a standby agent becomes **active** if *strictly more than 50%* of its neighbors are willing;
   - an active agent **stays active** if more than 50% of its neighbors are willing. Otherwise it goes straight back to **inactive**.
3. **Standby timeout.** An agent that has spent `T` timesteps in standby without becoming active goes back to inactive. The step in which it entered standby counts as its first. Back in inactive, it flips the coin again on later steps.

Some consequences of these rules:

- Inactive agents never become active directly. They must reach standby first, however many of their neighbors are protesting.
- Agents with no neighbors never become active.
- On a directed graph, an agent looks at its out-neighbors (`G.successors`).
- Edge weights are ignored.

## Setup

```sh
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Usage

```python
import networkx as nx
from protest import simulate

G = nx.watts_strogatz_graph(1000, 6, 0.1, seed=0)
result = simulate(G, p=0.1, T=3, steps=100, seed=0)

result.states     # int8 array (steps+1, n_agents): 0 inactive, 1 standby, 2 active
result.counts     # (steps+1, 3) agents per state at each timestep
result.fractions  # same as counts, divided by the population
result.state_at(10)  # {node: "inactive" | "standby" | "active"} at timestep 10
```

To step through a run yourself, for example to animate it, use `ProtestModel(G, p, T, seed=...)` and call `.step()` repeatedly. You can set a starting configuration with `initial_state={node: "standby", ...}`. Nodes you leave out start inactive.

From the command line, this runs a small-world network and prints counts every 10 steps (add `--plot` to see a chart):

```sh
.venv/bin/python protest.py --n 1000 --p 0.15 --T 3 --plot
```

## Grid video

`grid_video.py` puts agents on a 100×100 grid that wraps around at the edges (a torus). Each agent is connected to its four neighbors (up, down, left, right). The script runs 100 timesteps and saves `grid_protest.mp4`. The left panel shows the grid (gray = inactive, amber = standby, red = active). The right panel shows the fraction of agents in each state over time.

```sh
.venv/bin/python grid_video.py                       # p = 0.15, T = 5
.venv/bin/python grid_video.py --p 0.13 --T 5 --out slow.mp4
```

With four neighbors, a standby agent needs at least 3 willing neighbors to become active. The outcome changes sharply with `p` and `T`. With seed 0, after 100 steps:

| T | p = 0.10 | p = 0.13 | p = 0.15 | p = 0.20 |
|---|----------|----------|----------|----------|
| 3 | 2% active  | –   | 8% active  | 99% active |
| 5 | 7% active  | 50% active | 99% active | 100% active |

Writing `.mp4` needs `ffmpeg`. Without it, or if `--out` ends in `.gif`, the script saves a GIF.

## Tests

```sh
.venv/bin/python -m pytest -q
```
