import math
import random
import unittest

class ASFRP:
    def __init__(self, n, alpha, beta, gamma, mu, lmbda, f_max):
        self.n = n
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.mu = mu
        self.lmbda = lmbda
        self.f_max = f_max
        self.distances = [[random.uniform(10, 100) if i != j else 0 for j in range(n)] for i in range(n)]
        self.weights = [random.uniform(10, 50) for _ in range(n)]
        self.weights[0] = 0.0
        self.time_windows = []
        for i in range(n):
            start = random.uniform(0, 24)
            end = start + random.uniform(2, 10)
            self.time_windows.append((start, end))
        self.time_windows[0] = (0.0, 1000.0)
        self.r_base = [[random.uniform(1, 5) for _ in range(n)] for _ in range(n)]
        self.speed = 40.0

    def evaluate(self, route):
        t = 0.0
        w_curr = 0.0
        f_total = 0.0
        dist_total = 0.0
        max_risk = 0.0
        penalty = 0.0
        timeline = []
        curr = 0
        for nxt in route + [0]:
            d = self.distances[curr][nxt]
            f_step = d * (self.mu + self.lmbda * w_curr)
            f_total += f_step
            dist_total += d
            t_arr = t + d / self.speed
            if t_arr > self.time_windows[nxt][1]:
                penalty += 10000 * (t_arr - self.time_windows[nxt][1])
            t_dep = max(t_arr, self.time_windows[nxt][0])
            risk = self.r_base[curr][nxt] * (1 + math.sin(math.pi * t / 12))
            max_risk = max(max_risk, risk)
            timeline.append((nxt, t_arr, t_dep, f_total, w_curr))
            w_curr += self.weights[nxt]
            t = t_dep + 1.0 
            curr = nxt
        if f_total > self.f_max:
            penalty += 10000 * (f_total - self.f_max)
        j = self.alpha * dist_total + self.beta * max_risk + self.gamma * f_total + penalty
        return j, timeline, f_total

    def optimize(self, iterations=10000, temp=1000.0, cooling=0.995):
        curr_route = list(range(1, self.n))
        random.shuffle(curr_route)
        curr_cost, _, _ = self.evaluate(curr_route)
        best_route = curr_route[:]
        best_cost = curr_cost
        for _ in range(iterations):
            temp *= cooling
            if temp < 0.1:
                break
            new_route = curr_route[:]
            i, j = random.sample(range(self.n - 1), 2)
            new_route[i], new_route[j] = new_route[j], new_route[i]
            new_cost, _, _ = self.evaluate(new_route)
            if new_cost < curr_cost or random.random() < math.exp((curr_cost - new_cost) / temp):
                curr_route = new_route[:]
                curr_cost = new_cost
                if new_cost < best_cost:
                    best_route = new_route[:]
                    best_cost = new_cost
        return best_route, best_cost

    def report(self, route):
        cost, timeline, f_total = self.evaluate(route)
        rep = [
            f"Final Cost Function Value: {cost:.2f}",
            f"Total Fuel Consumed: {f_total:.2f} / {self.f_max}",
            f"Node Visitation Order: {[0] + route + [0]}",
            "Route Timeline:",
            "Node | Arrive | Depart | Fuel Total | Cargo Weight"
        ]
        for node, arr, dep, f, w in timeline:
            rep.append(f"{node:>4} | {arr:>6.2f} | {dep:>6.2f} | {f:>10.2f} | {w:>12.2f}")
        return "\n".join(rep)

class TestASFRP(unittest.TestCase):
    def test_evaluate(self):
        problem = ASFRP(5, 1.0, 1.0, 1.0, 0.1, 0.01, 10000)
        route = [1, 2, 3, 4]
        cost, timeline, f_total = problem.evaluate(route)
        self.assertTrue(cost > 0)
        self.assertEqual(len(timeline), 5)

    def test_optimization(self):
        problem = ASFRP(10, 1.0, 10.0, 0.5, 0.2, 0.05, 50000)
        route, cost = problem.optimize(iterations=100)
        self.assertEqual(len(route), 9)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    print("Execution Report for N=25")
    p = ASFRP(n=25, alpha=1.0, beta=50.0, gamma=2.0, mu=0.2, lmbda=0.05, f_max=100000)
    best_r, best_c = p.optimize(iterations=5000)
    print(p.report(best_r))