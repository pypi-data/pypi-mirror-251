if __name__ == "__main__":
    from gzeuge.graphs.hypergraph import BaseHyperGraph
    from gzeuge.graphs.schema import OrdinaryEdge
    hg = BaseHyperGraph(hash='g1', label='DATA STACK')
    hg.add_nodes(nodes=[
        ("A", {'label': 'tom'}),
        ("B", {'label': 'jerry', 'is': 'Mouse'})
    ])
    hg.add_edge(edge=OrdinaryEdge(
        source="A", target="B", attributes={"label": "likes"}))
    sub1 = BaseHyperGraph(hash='g2', label='CLOUD')
    sub1.merge([
        ("S1", {'label': 'tom'}),
        ("S2", {'label': 'jerry', 'is': 'Mouse'}),
        ("S1", "S2", {'label': 'dominates'})
    ])
    hg.merge([sub1])
    hg.merge_interedges([("A", "S1"),
                        ("g1", "g2", {'label': 'dominates'})])
    sub1.merge_interedges([("S2", "B"), (sub1.hash, hg.hash)])
    hg.print()
