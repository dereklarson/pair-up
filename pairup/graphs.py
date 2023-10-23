import streamlit.components.v1 as st_comp
from pyvis.network import Network


class ListNode:
    """Element of a singly-linked list."""

    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def ll2list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res


def list2ll(list):
    head = ListNode(0)
    curr = head
    for val in list:
        curr.next = ListNode(val)
        curr = curr.next
    return head.next


def ll2elements(head, level=0):
    nodes = []
    edges = []
    ct = 0
    while head:
        ct += 1
        id = f"{ct}_{level}_{head.val}"
        if nodes:
            edges.append((nodes[-1]["n_id"], id))
        nodes.append({"n_id": id, "label": str(head.val), "level": level})
        head = head.next
    return nodes, edges


def bt2elements(bt_list):
    nodes = []
    edges = []
    ct = 0
    level = 0
    for num in bt_list:
        ct += 1


def plot_graph(nodes: list, edges: list):
    network = Network(
        "400px",
        "1100px",
        directed=True,
        bgcolor="#222222",
        font_color="white",
        layout=True,
    )
    for node in nodes:
        network.add_node(**node)
    network.add_edges(edges)
    network.write_html("viz.html")
    with open("viz.html", "r", encoding="utf-8") as fh:
        st_comp.html(fh.read(), width=1200, height=430)
