"""Agent-based model of protest on a social network.

Each node of a networkx graph is an agent in one of three states:

    INACTIVE (0) -- not currently willing to protest
    STANDBY  (1) -- privately willing to protest, for at most T timesteps
    ACTIVE   (2) -- publicly protesting

One timestep, applied to all agents at once (synchronous update):

  1. Coin flip. Each INACTIVE agent becomes STANDBY with probability p and
     starts a standby clock.
  2. Threshold check. Using the states after step 1, each agent counts how
     many of its neighbors are "willing" (STANDBY or ACTIVE).
       - A STANDBY agent becomes ACTIVE if strictly more than 50% of its
         neighbors are willing.
       - An ACTIVE agent stays ACTIVE if strictly more than 50% of its
         neighbors are willing. Otherwise it drops straight to INACTIVE.
  3. Standby timeout. A STANDBY agent that has spent T timesteps in standby
     without becoming active goes back to INACTIVE. The step it entered
     standby counts as its first. With T = 1 an agent gets exactly one
     chance to activate. Once back in INACTIVE it flips the coin again on
     later steps.

Agents with no neighbors never become ACTIVE. For a directed graph an agent
looks at its out-neighbors (G.successors), which matches G.neighbors.
Edge weights are ignored.
"""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np

INACTIVE, STANDBY, ACTIVE = 0, 1, 2
STATE_NAMES = ("inactive", "standby", "active")


@dataclass
class SimulationResult:
    """Output of `simulate`.

    states: int8 array, shape (steps + 1, n_agents). Row t is the state of
        every agent after t timesteps; row 0 is the initial condition.
    nodes: node labels, in the same order as the columns of `states`.
    """

    states: np.ndarray
    nodes: list

    @property
    def counts(self) -> np.ndarray:
        """Agents in each state per timestep, shape (steps + 1, 3)."""
        return np.stack([(self.states == s).sum(axis=1) for s in range(3)], axis=1)

    @property
    def fractions(self) -> np.ndarray:
        """Like `counts`, but as fractions of the population."""
        return self.counts / self.states.shape[1]

    def state_at(self, t: int) -> dict:
        """{node: state name} at timestep t."""
        return {node: STATE_NAMES[s] for node, s in zip(self.nodes, self.states[t])}


class ProtestModel:
    """Holds the network and the current state; call `step()` to advance."""

    def __init__(
        self,
        G: nx.Graph,
        p: float,
        T: int,
        seed: int | np.random.Generator | None = None,
        initial_state: dict | None = None,
    ):
        """
        G: any networkx graph. Each node is an agent.
        p: per-timestep probability that an INACTIVE agent goes to STANDBY.
        T: maximum number of timesteps an agent stays in STANDBY (integer >= 1).
        seed: seed or numpy Generator, for reproducible runs.
        initial_state: optional {node: 0/1/2 or "inactive"/"standby"/"active"}.
            Nodes not listed start INACTIVE. For an agent that starts in
            STANDBY, timestep 0 counts as its first standby step.
        """
        if not 0.0 <= p <= 1.0:
            raise ValueError(f"p must be in [0, 1], got {p}")
        if int(T) != T or T < 1:
            raise ValueError(f"T must be an integer >= 1, got {T}")

        self.G = G
        self.p = float(p)
        self.T = int(T)
        self.rng = np.random.default_rng(seed)

        self.nodes = list(G.nodes())
        index = {node: i for i, node in enumerate(self.nodes)}
        self.n = len(self.nodes)

        # Edge list as two index arrays: agent src looks at agent dst.
        # An undirected edge is added in both directions.
        pairs = [(index[u], index[v]) for u, v in G.edges() if u != v]
        if not G.is_directed():
            pairs += [(v, u) for u, v in pairs]
        pairs = np.array(pairs, dtype=np.int64).reshape(-1, 2)
        self._src, self._dst = pairs[:, 0], pairs[:, 1]
        self.degree = np.bincount(self._src, minlength=self.n)

        self.state = np.zeros(self.n, dtype=np.int8)
        # Number of timesteps each agent has spent in STANDBY (0 otherwise).
        self.standby_age = np.zeros(self.n, dtype=np.int64)
        if initial_state:
            for node, s in initial_state.items():
                if isinstance(s, str):
                    s = STATE_NAMES.index(s)
                self.state[index[node]] = s

    def willing_fraction(self, state: np.ndarray | None = None) -> np.ndarray:
        """Per agent: fraction of neighbors in STANDBY or ACTIVE (0 if no neighbors)."""
        state = self.state if state is None else state
        willing = (state != INACTIVE).astype(np.int64)
        count = np.bincount(self._src, weights=willing[self._dst], minlength=self.n)
        return np.divide(count, self.degree, out=np.zeros(self.n), where=self.degree > 0)

    def step(self) -> np.ndarray:
        """Advance one timestep and return the new state array."""
        state = self.state.copy()

        # 1. Coin flip: INACTIVE -> STANDBY with probability p.
        flips = (state == INACTIVE) & (self.rng.random(self.n) < self.p)
        state[flips] = STANDBY
        self.standby_age[flips] = 0

        # 2. Threshold check, synchronous, on the post-flip states.
        supported = self.willing_fraction(state) > 0.5
        was_standby = state == STANDBY
        was_active = state == ACTIVE
        state[was_standby & supported] = ACTIVE
        state[was_active & ~supported] = INACTIVE

        # 3. Standby timeout for agents still in STANDBY.
        still_standby = state == STANDBY
        self.standby_age[still_standby] += 1
        state[still_standby & (self.standby_age >= self.T)] = INACTIVE
        self.standby_age[state != STANDBY] = 0

        self.state = state
        return state

    def run(self, steps: int) -> SimulationResult:
        """Run `steps` timesteps; return the full history including the start."""
        history = np.empty((steps + 1, self.n), dtype=np.int8)
        history[0] = self.state
        for t in range(1, steps + 1):
            history[t] = self.step()
        return SimulationResult(states=history, nodes=self.nodes)


def simulate(
    G: nx.Graph,
    p: float,
    T: int,
    steps: int,
    seed: int | np.random.Generator | None = None,
    initial_state: dict | None = None,
) -> SimulationResult:
    """Run the protest model on graph G for `steps` timesteps."""
    return ProtestModel(G, p, T, seed=seed, initial_state=initial_state).run(steps)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the protest model on a small-world network.")
    parser.add_argument("--n", type=int, default=1000, help="number of agents")
    parser.add_argument("--k", type=int, default=6, help="neighbors per agent (Watts-Strogatz)")
    parser.add_argument("--rewire", type=float, default=0.1, help="Watts-Strogatz rewiring probability")
    parser.add_argument("--p", type=float, default=0.05, help="inactive -> standby probability")
    parser.add_argument("--T", type=int, default=5, help="max timesteps in standby")
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--plot", action="store_true", help="plot state fractions over time")
    args = parser.parse_args()

    G = nx.watts_strogatz_graph(args.n, args.k, args.rewire, seed=args.seed)
    result = simulate(G, args.p, args.T, args.steps, seed=args.seed)

    print(f"{'t':>4} {'inactive':>9} {'standby':>8} {'active':>7}")
    for t, (i, s, a) in enumerate(result.counts):
        if t % 10 == 0 or t == args.steps:
            print(f"{t:>4} {i:>9} {s:>8} {a:>7}")

    if args.plot:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 4))
        for s, name in enumerate(STATE_NAMES):
            ax.plot(result.fractions[:, s], label=name)
        ax.set_xlabel("timestep")
        ax.set_ylabel("fraction of agents")
        ax.set_title(f"Protest model: p={args.p}, T={args.T}, n={args.n}")
        ax.legend()
        fig.tight_layout()
        plt.show()
