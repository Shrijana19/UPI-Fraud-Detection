import networkx as nx

class GraphEngine:
    def __init__(self):
        self.G = nx.DiGraph()

    def add_transaction(self, sender, receiver, amount):
        self.G.add_edge(sender, receiver, amount=amount)

    def compute_graph_risk(self, user):
        if user not in self.G:
            return 0.0, {}

        # High in-degree (mule detection)
        in_degree = self.G.in_degree(user)
        max_in_degree = max([self.G.in_degree(n) for n in self.G.nodes()], default=1)
        in_degree_score = in_degree / max_in_degree if max_in_degree > 0 else 0

        # Cycle detection
        cycles = list(nx.simple_cycles(self.G))
        cycle_flag = 1 if any(user in cycle for cycle in cycles) else 0

        # PageRank anomaly
        pagerank = nx.pagerank(self.G) if len(self.G.nodes()) > 0 else {}
        pagerank_score = pagerank.get(user, 0)

        graph_risk = (
            0.4 * in_degree_score +
            0.3 * cycle_flag +
            0.3 * pagerank_score
        )

        explanation = {
            "High in-degree": round(in_degree_score, 2),
            "Cycle detected": cycle_flag,
            "PageRank anomaly": round(pagerank_score, 2)
        }

        return min(graph_risk, 1.0), explanation
