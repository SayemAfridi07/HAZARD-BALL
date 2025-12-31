# 🟢 Hazard Ball - 3D OpenGL Survival Game

**Hazard Ball** is a physics-based 3D arcade survival game built from scratch using **Python** and **PyOpenGL**. The game features a custom physics engine, procedurally generated levels, and dynamic difficulty scaling. The player controls a rolling ball through a grid-based arena, avoiding static and moving hazards while collecting "Energy Cores" to unlock the exit portal.

## 🎮 Game Features

### Core Gameplay

* **Procedural Level Generation:** Every time the game starts or resets, the map logic generates a unique layout of safe zones, holes, and obstacles. No two runs are the same.
* **Physics-Based Movement:** Custom implementation of momentum, friction, acceleration, and gravity. The ball doesn't just stop; it rolls and glides, requiring precise control.
* **Level Progression:** The game features a 5-Level difficulty system.
* **Level 1-2:** Static holes and obstacles.
* **Level 3-4:** Introduction of **Moving Walls** and **Moving Voids** that patrol specific paths.
* **Level 5 (Meltdown):** The floor begins to crumble dynamically, forcing the player to keep moving.


* **Dual Camera System:** Toggle between **Third-Person** (Orbital view) and **First-Person** (On-the-ball view) in real-time.

### Mechanics & Power-ups

* **Objective:** Collect 5 **Diamonds (Energy Cores)** to activate the Exit Portal.
* **Hazards:** Bottomless pits, red spike blocks, and patrolling enemies.
* **Power-ups:**
* ⚡ **Speed Boost:** Temporarily doubles acceleration and reduces friction.
* ❤️ **Extra Life:** Rare drop to extend gameplay.


* **Developer Tools:** Built-in **Level Skip** function for testing high-level mechanics instantly.

---

## 🕹️ Controls

| Key | Action |
| --- | --- |
| **W, A, S, D** | Move the ball (Physics-based) |
| **Arrow Keys** | Rotate Camera / Look Up & Down |
| **C** | **Cheat/Dev Tool:** Skip to Next Level |
| **Right Click** | Toggle Camera Mode (1st / 3rd Person) |
| **R** | Hard Reset (Restart from Level 1) |

---

## 🛠️ Technical Implementation

This project demonstrates core Computer Graphics and Game Development concepts without relying on high-level game engines like Unity.

### 1. Physics Engine

Instead of using a physics library, the movement logic is calculated manually in the `idle()` loop:

* **Integration:** `Position += Velocity` applied every frame.
* **Friction:** `Velocity *= 0.97` simulates rolling resistance.
* **Gravity:** When `falling` state is triggered, Z-axis velocity increases exponentially.

### 2. Collision Detection

* **Grid Snapping:** The continuous float position of the player is converted to discrete grid coordinates using integer division (`//`) to perform O(1) lookup for floor tiles (Holes/Items).
* **AABB Collision:** Axis-Aligned Bounding Box logic is used to detect collisions with moving enemies in Level 3+.
* **Boundary Checking:** Hard constraints keep the player within the `-1200` to `+1200` world limits.

### 3. Rendering Pipeline

* **Matrix Stack:** extensive use of `glPushMatrix()` and `glPopMatrix()` to isolate transformations for the player, enemies, and UI.
* **Double Buffering:** Implemented via `GLUT_DOUBLE` to ensure smooth animation without screen tearing.
* **Z-Buffering:** `GL_DEPTH_TEST` enabled to handle proper 3D occlusion of objects.

---

## 🚀 How to Run

### Prerequisites

You need Python installed along with the PyOpenGL library.

```bash
pip install PyOpenGL PyOpenGL_accelerate

```

### Execution

Clone the repository and run the main script:

```bash
git clone https://github.com/your-username/Hazard-Ball.git
cd Hazard-Ball
python "final project.py"

```

---

## 🔮 Future Improvements

* Add dynamic lighting and shadows.
* Implement high-score saving to a local file.
* Add texture mapping to the floor and ball.
