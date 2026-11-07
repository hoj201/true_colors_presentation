"""Run the protest model on a periodic square grid and save a video.

Each agent sits on a cell of an L x L torus (the grid wraps at the edges) and
is connected to its four neighbors: up, down, left and right. Because the
threshold is strictly more than 50%, a standby agent needs at least 3 of its
4 neighbors to be willing before it becomes active.

Usage:
    .venv/bin/python grid_video.py                      # defaults below
    .venv/bin/python grid_video.py --p 0.13 --T 5 --out slow.mp4

Saves an .mp4 with ffmpeg if it is installed. Otherwise, or if --out ends in
.gif, saves an animated GIF.
"""

import argparse

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib import animation
from matplotlib.colors import ListedColormap

from protest import STATE_NAMES, simulate

COLORS = {
    "inactive": "#e8e6e1",
    "standby": "#f2b134",
    "active": "#c8102e",
}


def run_grid(L: int, p: float, T: int, steps: int, seed: int):
    """Simulate on an L x L periodic grid; return states as (steps+1, L, L) plus fractions."""
    G = nx.grid_2d_graph(L, L, periodic=True)
    result = simulate(G, p, T, steps, seed=seed)

    # Put column k of result.states (node (i, j)) at pixel (i, j).
    rows = np.array([node[0] for node in result.nodes])
    cols = np.array([node[1] for node in result.nodes])
    frames = np.empty((steps + 1, L, L), dtype=np.int8)
    frames[:, rows, cols] = result.states
    return frames, result.fractions


def make_video(frames, fractions, p, T, out, fps):
    steps = len(frames) - 1
    cmap = ListedColormap([COLORS[name] for name in STATE_NAMES])

    fig, (ax_grid, ax_line) = plt.subplots(
        1, 2, figsize=(11, 5.5), gridspec_kw={"width_ratios": [1, 1.1]}
    )
    fig.suptitle(f"Protest model on a {frames.shape[1]}×{frames.shape[2]} grid  ·  p = {p}, T = {T}")

    image = ax_grid.imshow(frames[0], cmap=cmap, vmin=0, vmax=2, interpolation="nearest")
    ax_grid.set_xticks([])
    ax_grid.set_yticks([])
    title = ax_grid.set_title("t = 0")

    ax_line.set_xlim(0, steps)
    ax_line.set_ylim(0, 1)
    ax_line.set_xlabel("timestep")
    ax_line.set_ylabel("fraction of agents")
    ax_line.spines[["top", "right"]].set_visible(False)
    ax_line.grid(alpha=0.3)
    lines = []
    for s, name in enumerate(STATE_NAMES):
        # Inactive is drawn darker than its pale grid color so it shows on white.
        color = "#8a8780" if name == "inactive" else COLORS[name]
        (line,) = ax_line.plot([], [], color=color, lw=2, label=name)
        lines.append(line)
    ax_line.legend(loc="center right", frameon=False)
    fig.tight_layout()

    def update(t):
        image.set_data(frames[t])
        title.set_text(f"t = {t}")
        x = np.arange(t + 1)
        for s, line in enumerate(lines):
            line.set_data(x, fractions[: t + 1, s])
        return [image, title, *lines]

    anim = animation.FuncAnimation(fig, update, frames=steps + 1, blit=False)

    use_gif = out.endswith(".gif") or not animation.FFMpegWriter.isAvailable()
    if use_gif and not out.endswith(".gif"):
        out = out.rsplit(".", 1)[0] + ".gif"
        print("ffmpeg not found; saving a GIF instead.")
    writer = animation.PillowWriter(fps=fps) if use_gif else animation.FFMpegWriter(fps=fps, bitrate=2400)
    anim.save(out, writer=writer, dpi=120)
    plt.close(fig)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--L", type=int, default=100, help="grid side length (L x L agents)")
    parser.add_argument("--p", type=float, default=0.15, help="inactive -> standby probability")
    parser.add_argument("--T", type=int, default=5, help="max timesteps in standby")
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--out", default=None, help="output file (.mp4 or .gif)")
    args = parser.parse_args()

    frames, fractions = run_grid(args.L, args.p, args.T, args.steps, args.seed)
    if args.out is None:
        args.out = f"grid_protest_T{args.T}_p{args.p}_L{args.L}.mp4"
    out = make_video(frames, fractions, args.p, args.T, args.out, args.fps)
    final = fractions[-1]
    print(
        f"Saved {out}  (final: inactive {final[0]:.0%}, standby {final[1]:.0%}, active {final[2]:.0%})"
    )


if __name__ == "__main__":
    main()
