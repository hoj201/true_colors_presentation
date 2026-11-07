import networkx as nx
import numpy as np

from protest import ACTIVE, INACTIVE, STANDBY, ProtestModel, simulate


def test_p_zero_nothing_happens():
    G = nx.erdos_renyi_graph(50, 0.1, seed=1)
    result = simulate(G, p=0.0, T=3, steps=20, seed=1)
    assert (result.states == INACTIVE).all()


def test_p_one_complete_graph_all_active():
    # Everyone flips to standby in step 1, so every neighborhood is 100% willing.
    result = simulate(nx.complete_graph(10), p=1.0, T=3, steps=5, seed=0)
    assert (result.states[1:] == ACTIVE).all()


def test_standby_times_out_after_T_steps():
    # Isolated agent: can never activate, so it sits in standby for exactly T steps.
    G = nx.empty_graph(1)
    m = ProtestModel(G, p=0.0, T=3, initial_state={0: "standby"})
    assert [m.step()[0] for _ in range(4)] == [STANDBY, STANDBY, INACTIVE, INACTIVE]
    # The initial standby state counts as step 0, so the clock runs out after
    # three calls: two more steps in standby, then back to inactive.


def test_T_one_means_one_chance():
    G = nx.empty_graph(1)
    m = ProtestModel(G, p=1.0, T=1)
    # Flips to standby, gets no support, and times out in the same step.
    assert m.step()[0] == INACTIVE


def test_strictly_more_than_half():
    # Path a - b - c. b has 2 neighbors; exactly 1 willing (50%) is not enough.
    G = nx.path_graph(3)
    m = ProtestModel(G, p=0.0, T=10, initial_state={0: "standby", 1: "standby"})
    assert m.step()[1] == STANDBY
    # With both neighbors willing (100%), b activates.
    m = ProtestModel(G, p=0.0, T=10, initial_state={0: "standby", 1: "standby", 2: "standby"})
    assert m.step()[1] == ACTIVE


def test_inactive_agents_do_not_activate_from_neighbors():
    # Star: center inactive, all leaves active. Center only activates via standby.
    G = nx.star_graph(4)
    init = {leaf: "active" for leaf in range(1, 5)}
    m = ProtestModel(G, p=0.0, T=3, initial_state=init)
    assert m.step()[0] == INACTIVE


def test_active_drops_to_inactive_without_support():
    G = nx.path_graph(2)
    m = ProtestModel(G, p=0.0, T=3, initial_state={0: "active"})
    assert m.step()[0] == INACTIVE


def test_active_counts_as_willing_and_sustains():
    G = nx.complete_graph(4)
    m = ProtestModel(G, p=0.0, T=3, initial_state={n: "active" for n in G})
    for _ in range(10):
        assert (m.step() == ACTIVE).all()


def test_directed_graph_uses_out_neighbors():
    # 0 -> 1 and 1 is standby, so 0 sees 100% willing. 1 has no out-neighbors.
    G = nx.DiGraph([(0, 1)])
    m = ProtestModel(G, p=0.0, T=3, initial_state={0: "standby", 1: "standby"})
    s = m.step()
    assert s[0] == ACTIVE and s[1] == STANDBY


def test_reproducible_with_seed():
    G = nx.watts_strogatz_graph(200, 6, 0.1, seed=3)
    a = simulate(G, 0.1, 4, 30, seed=42).states
    b = simulate(G, 0.1, 4, 30, seed=42).states
    assert np.array_equal(a, b)


def test_counts_sum_to_population():
    G = nx.barabasi_albert_graph(300, 3, seed=0)
    result = simulate(G, 0.2, 3, 25, seed=0)
    assert (result.counts.sum(axis=1) == 300).all()
