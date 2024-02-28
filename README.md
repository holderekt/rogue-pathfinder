# Pathfinder^2
### A pathfing genetic algorithm based on a subset of Pathfinder RPG rules

Assuming a rogue moving inside a closed map, with the goal of reaching an objective position, we try to find the optimal path that ensures:
- Minimal travavel
- Objects and difficult terrain
- Minimizes the probability of being caught by an enemy
- Take advantage of covers
In this problem the enemyes do not move, the probability of being seen is modeled as a penality function on movement cost based on enemy distance and presence of covers
Example:  
### GENERATION 0
```
Legal:     True
Complete:  False
Fitness:   29.5

      1 2 3 4 5 6 7 8 9
    # # # # # # # # # # #
  1 #   ← ←       T     # 1
  2 # → → ↑       T T   # 2
  3 # ↑   #       # Z T # 3
  4 # ↑ ← #       #     # 4
  5 # → ↑ #   Y   #     # 5
  6 # ↑ Z #       #     # 6
  7 # ↑ ← # # # # #   Z # 7
  8 #   ↑ ↓ ←           # 8
  9 #   ↑ ← ↑ ←         # 9
    # # # # # # # # # # #
      1 2 3 4 5 6 7 8 9
```
### GENERATION 100
```
Legal:     True
Complete:  True
Fitness:   7.0
    1 2 3 4 5 6 7 8 9
  # # # # # # # # # # #
1 #             T     # 1
2 #   → → → ↓   T T   # 2
3 # → ↑ #   ↓   # Z T # 3
4 # ↑ X #   ↓   #     # 4
5 # ↑ X #   Y   #     # 5
6 # ↑ Z #       #     # 6
7 # ↑ X # # # # #   Z # 7
8 # ↑ ← ← ←           # 8
9 #       ↑ ←         # 9
  # # # # # # # # # # #
    1 2 3 4 5 6 7 8 9
```
