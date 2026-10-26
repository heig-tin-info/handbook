"""Figures of the Box-Muller page: python figures.py <output directory>.

Needs matplotlib and numpy: uv run --with matplotlib --with numpy python figures.py docs/assets/images
"""
import sys
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

out = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
rng = np.random.default_rng(42)
N = 400
cmap = LinearSegmentedColormap.from_list("bm", ["#2b3cff", "#a030c0", "#ff2020"])

u1 = rng.uniform(size=N)
u2 = rng.uniform(size=N)
r = np.sqrt(-2.0 * np.log(u1))
theta = 2.0 * np.pi * u2
z0 = r * np.cos(theta)
z1 = r * np.sin(theta)
color = cmap(np.clip(r / 3.0, 0, 1))

plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold"})

# Figure 1: the three steps side by side.
fig = plt.figure(figsize=(11, 3.8))
ax = fig.add_subplot(1, 3, 1)
ax.scatter(u1, u2, s=7, c=color, lw=0)
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.set_xlabel("$U_1$")
ax.set_ylabel("$U_2$")
ax.grid(True, lw=0.5, alpha=0.5)
ax.set_title("1. Deux uniformes $(U_1, U_2)$")

ax = fig.add_subplot(1, 3, 2, projection="polar")
ax.scatter(theta, r, s=7, c=color, lw=0)
ax.set_rmax(3.2)
ax.set_rticks([1, 2, 3])
ax.set_xticks(np.linspace(0, 2 * np.pi, 8, endpoint=False))
ax.set_xticklabels(["0", "π/4", "π/2", "3π/4", "π", "5π/4", "3π/2", "7π/4"])
ax.grid(True, lw=0.5, alpha=0.6)
ax.set_title("2. Coordonnées polaires $(r, \\theta)$", pad=14)

ax = fig.add_subplot(1, 3, 3)
bins = np.linspace(-3.5, 3.5, 36)
counts, edges = np.histogram(z0, bins=bins)
centers = (edges[:-1] + edges[1:]) / 2
ax.bar(centers, counts, width=edges[1] - edges[0], color=cmap(np.clip(np.abs(centers) / 3.0, 0, 1)), lw=0)
x = np.linspace(-3.5, 3.5, 200)
ax.plot(x, N * (edges[1] - edges[0]) * np.exp(-x * x / 2) / np.sqrt(2 * np.pi), "k-", lw=1.2, label="$\\mathcal{N}(0,1)$")
ax.set_xlabel("$z_0 = r\\cos\\theta$")
ax.set_ylabel("Effectif")
ax.set_xlim(-3.5, 3.5)
ax.legend(frameon=False)
ax.grid(True, lw=0.5, alpha=0.5)
ax.set_title("3. Projection sur un axe")
fig.tight_layout()
fig.savefig(out / "box-muller-steps.svg", bbox_inches="tight")
plt.close(fig)

# Figure 2: why the radius follows sqrt(-2 ln U): the 2D cloud is isotropic,
# and the same points seen on the x axis and the y axis are both normal.
M = 2000
U1 = rng.uniform(size=M)
U2 = rng.uniform(size=M)
R = np.sqrt(-2.0 * np.log(U1))
T = 2.0 * np.pi * U2
X = R * np.cos(T)
Y = R * np.sin(T)
fig = plt.figure(figsize=(5.2, 5.2))
gs = fig.add_gridspec(2, 2, width_ratios=(4, 1), height_ratios=(1, 4), wspace=0.05, hspace=0.05)
ax = fig.add_subplot(gs[1, 0])
ax_top = fig.add_subplot(gs[0, 0], sharex=ax)
ax_right = fig.add_subplot(gs[1, 1], sharey=ax)
ax.scatter(X, Y, s=3, c=cmap(np.clip(R / 3.0, 0, 1)), lw=0, alpha=0.8)
for rad in (1, 2, 3):
    ax.add_patch(plt.Circle((0, 0), rad, fill=False, ec="k", lw=0.6, ls="--", alpha=0.6))
    ax.annotate(f"$r={rad}$", (rad * np.cos(np.pi / 4), rad * np.sin(np.pi / 4)), fontsize=7, ha="left", va="bottom")
ax.set_xlim(-3.8, 3.8)
ax.set_ylim(-3.8, 3.8)
ax.set_aspect("equal")
ax.set_xlabel("$z_0$")
ax.set_ylabel("$z_1$")
ax.grid(True, lw=0.5, alpha=0.4)
b = np.linspace(-3.8, 3.8, 40)
ax_top.hist(X, bins=b, color="#2b3cff", alpha=0.7)
ax_right.hist(Y, bins=b, color="#2b3cff", alpha=0.7, orientation="horizontal")
for a in (ax_top, ax_right):
    a.tick_params(labelbottom=False, labelleft=False, length=0)
    for s in a.spines.values():
        s.set_visible(False)
ax_top.set_title("Le nuage $(z_0, z_1)$ est isotrope : chaque axe est une normale", fontsize=9, fontweight="bold")
fig.savefig(out / "box-muller-cloud.svg", bbox_inches="tight")
plt.close(fig)

# Figure 3: Marsaglia's polar method, the points of the square that the unit
# disc keeps.
K = 1200
V1 = rng.uniform(-1, 1, size=K)
V2 = rng.uniform(-1, 1, size=K)
S = V1 * V1 + V2 * V2
keep = (S > 0) & (S < 1)
fig, ax = plt.subplots(figsize=(4.2, 4.2))
ax.scatter(V1[~keep], V2[~keep], s=6, c="#bbbbbb", lw=0, label=f"rejetés ({(~keep).sum()})")
ax.scatter(V1[keep], V2[keep], s=6, c=cmap(np.clip(np.sqrt(S[keep]), 0, 1)), lw=0, label=f"acceptés ({keep.sum()})")
ax.add_patch(plt.Circle((0, 0), 1, fill=False, ec="k", lw=1))
ax.add_patch(plt.Rectangle((-1, -1), 2, 2, fill=False, ec="k", lw=1))
ax.set_xlim(-1.1, 1.1)
ax.set_ylim(-1.1, 1.1)
ax.set_aspect("equal")
ax.set_xlabel("$V_1$")
ax.set_ylabel("$V_2$")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8, frameon=False)
ax.set_title("Méthode polaire : seuls les points du disque sont gardés")
fig.savefig(out / "box-muller-polar.svg", bbox_inches="tight")
plt.close(fig)
print("ok", sorted(p.name for p in out.glob("box-muller-*.svg")))
