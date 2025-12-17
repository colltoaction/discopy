from discopy.frobenius import Ty, Box, Hypergraph as H
from discopy.utils import from_tree

def test_to_hif():
    x, y, z = map(Ty, "xyz")
    f = Box('f', x, y).to_hypergraph()
    g = Box('g', y, z).to_hypergraph()
    h = f >> g

    hif = h.to_hif()
    assert hif["network-type"] == "directed"
    assert hif["metadata"]["dom"] == "x"
    assert hif["metadata"]["cod"] == "z"
    assert len(hif["nodes"]) == 3
    assert len(hif["edges"]) == 2
    assert len(hif["incidences"]) == 4

    # Check edges
    box0 = next(e for e in hif["edges"] if e["edge"] == "box_0")
    assert box0["attrs"]["name"] == "f"
    box1 = next(e for e in hif["edges"] if e["edge"] == "box_1")
    assert box1["attrs"]["name"] == "g"

    # Check nodes
    spider0 = next(n for n in hif["nodes"] if n["node"] == "spider_0")
    assert spider0["attrs"]["type"] == "x"
    assert spider0["attrs"]["input_ports"] == [0]

    # Check incidences
    # spider_0 (input) -> box_0 (f)
    inc0 = next(i for i in hif["incidences"]
                if i["node"] == "spider_0" and i["edge"] == "box_0")
    assert inc0["direction"] == "tail"
    assert inc0["attrs"]["role"] == "dom"

def test_to_hif_copy():
    x = Ty('x')
    h = H.copy(x, 2)
    hif = h.to_hif()

    assert hif["network-type"] == "directed"
    assert len(hif["nodes"]) == 1
    assert len(hif["edges"]) == 0
    assert len(hif["incidences"]) == 0

    node = hif["nodes"][0]
    assert node["attrs"]["input_ports"] == [0]
    assert node["attrs"]["output_ports"] == [0, 1]

def test_to_hif_scalar():
    h = H.id()
    hif = h.to_hif()
    assert hif["nodes"] == []
    assert hif["edges"] == []
    assert hif["incidences"] == []

def test_to_from_tree():
    x, y, z = map(Ty, "xyz")
    f = Box('f', x, y).to_hypergraph()
    g = Box('g', y, z).to_hypergraph()
    h = f >> g

    tree = h.to_tree()
    h_loaded = H.from_tree(tree)
    assert h == h_loaded

    h_copy = H.copy(x, 2)
    assert H.from_tree(h_copy.to_tree()) == h_copy

    h_id = H.id(x)
    assert H.from_tree(h_id.to_tree()) == h_id

def test_tree_hif_consistency():
    x, y, z = map(Ty, "xyz")
    f = Box('f', x, y).to_hypergraph()
    g = Box('g', y, z).to_hypergraph()
    h = f >> g

    tree = h.to_tree()
    hif = h.to_hif()

    # Check that hif generated from tree-reconstructed object is identical
    h_from_tree = H.from_tree(tree)
    assert h_from_tree.to_hif() == hif

    # Check structural correspondence between Tree and HIF
    assert len(tree['boxes']) == len(hif['edges'])
    assert len(tree['spider_types']) == len(hif['nodes'])

    # Wire calculation in tree is implicit, but incidences in HIF reflect connections
    # Each box input/output in tree corresponds to an incidence in HIF
    box_incidences = sum(len(box['dom']['inside']) + len(box['cod']['inside'])
                         for box in tree['boxes'])
    assert box_incidences == len(hif['incidences'])
