# Asfrp-Optimizer
Advanced Vehicle Routing Problem (VRP) solver using Simulated Annealing. Optimizes secure fleet logistics with dynamic risk and time windows

# Advanced Secure Fleet Routing Protocol (ASFRP)



## English Version

### Project Overview
This project is an advanced variant of the Vehicle Routing Problem (VRP). The objective is to compute the optimal route for a heavily armored vehicle tasked with collecting physical drives containing sensitive IoT data from distributed secure nodes.

Unlike the standard Traveling Salesperson Problem (TSP), this algorithm must account for non-linear fuel consumption based on cargo weight, strict Time Windows for server access, and dynamic risk levels that fluctuate depending on the time of day.

### Mathematical Model & Constraints
The algorithm must find a valid path through `$N$` nodes (cities), starting and ending at the Base Node (Node 0), subject to the following strict constraints:

1. **Strict Time Windows:**
Each node `$i$` has a strict access time window `$[T_{start}^i,T_{end}^i]$`. The vehicle cannot extract data before `$T_{start}^i$` (though it is allowed to arrive early and idle) and is strictly forbidden from arriving after `$T_{end}^i$`.

2. **Non-linear Fuel Consumption:**
Fuel consumption for a given distance `$D$` scales with the current payload weight. Each collected server adds a specific weight `$w_i$`. The fuel consumed during a single edge traversal is calculated as:
`$$F_{step}=D\cdot(\mu+\lambda\cdot W_{current})$$`
where `$\mu$` is the baseline fuel consumption coefficient, `$\lambda$` is the weight penalty multiplier, and `$W_{current}$` is the cumulative weight of the cargo currently on board. Capacity is limited: `$F_{total}\le F_{max}$`.

3. **Dynamic Edge Risk:**
The risk level of traveling between node `$A$` and node `$B$` is a time-dependent function `$R(t)$` based on the departure time. For example, night travel increases the risk:
`$$R(t)=R_{base}\cdot(1+\sin(\frac{\pi t}{12}))$$`

4. **Multi-Objective Cost Function:**
The primary goal is to minimize the global cost function `$J$`:
`$$J=\alpha\sum D+\beta\max(R(t))+\gamma\sum F_{step}$$`
where `$\alpha$`, `$\beta$`, and `$\gamma$` are user-defined optimization weights.

### Implementation Details
* **Algorithm:** Implements **Simulated Annealing** (a meta-heuristic optimization algorithm) to efficiently solve the routing problem for `$N=25$` nodes where Brute Force is computationally impossible.
* **Testing:** Built-in Python `unittest` suite validates fitness evaluation logic and optimization boundaries.
