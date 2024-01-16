# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 10:08:12 2024

@author: Chai Wah Wu

generators for graph classes in networkx.

"""

from itertools import combinations, product, zip_longest
import networkx as nx


def qdigits(n):
    """Return tuple of digits of n in base 4"""
    if n == 0:
        return (0,)
    s = "0" * (n.bit_length() & 1) + bin(n)[2:]
    return tuple(int(s[i : i + 2], 2) for i in range(0, len(s) - 1, 2))


def keller_graph(n, create_using=None):
    """Return the Keller graph

    Parameters
    ----------
    n : int

    Notes
    -----
    https://mathworld.wolfram.com/KellerGraph.html
    """
    k = 1 << (n << 1)
    G = nx.empty_graph(range(k), create_using)
    G.add_edges_from(
        (a, b)
        for a in range(k)
        for b in range(a)
        if (
            s := tuple(
                c - d & 3
                for c, d in zip_longest(qdigits(a)[::-1], qdigits(b)[::-1], fillvalue=0)
            )
        ).count(2)
        > 0
        and s.count(0) <= len(s) - 2
    )
    return G


def king_graph(n, m=None, create_using=None):
    """Return the n by m king graph

    Parameters
    ----------
    n, m : int
        Chess board of size n by m.

    Notes
    -----
    https://mathworld.wolfram.com/KingGraph.html
    """
    if m is None:
        m = n
    G = nx.empty_graph(((i, j) for i in range(n) for j in range(m)), create_using)
    G.add_edges_from(
        ((i, j), (i + k, j + l))
        for i in range(n)
        for j in range(m)
        for (k, l) in (
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        )
        if 0 <= i + k < n and 0 <= j + l < m
    )
    return G


def knight_graph(n, m=None, create_using=None):
    """Return the n by m knight graph

    Parameters
    ----------
    n, m : int
        Chess board of size n by m.

    Notes
    -----
    https://mathworld.wolfram.com/KnightGraph.html
    """
    if m is None:
        m = n
    G = nx.empty_graph(((i, j) for i in range(n) for j in range(m)), create_using)
    G.add_edges_from(
        ((i, j), (i + k, j + l))
        for i in range(n)
        for j in range(m)
        for (k, l) in (
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
        )
        if 0 <= i + k < n and 0 <= j + l < m
    )
    return G


def antelope_graph(n, m=None, create_using=None):
    """Return the n by m antelope graph

    Parameters
    ----------
    n, m : int
        Chess board of size n by m.

    Notes
    -----
    https://mathworld.wolfram.com/AntelopeGraph.html
    """
    if m is None:
        m = n
    G = nx.empty_graph(((i, j) for i in range(n) for j in range(m)), create_using)
    G.add_edges_from(
        ((i, j), (i + k, j + l))
        for i in range(n)
        for j in range(m)
        for (k, l) in (
            (3, 4),
            (3, -4),
            (-3, 4),
            (-3, -4),
            (4, 3),
            (4, -3),
            (-4, 3),
            (-4, -3),
        )
        if 0 <= i + k < n and 0 <= j + l < m
    )
    return G


def fiveleaper_graph(n, m=None, create_using=None):
    """Return the n by m fiveleaper graph

    Parameters
    ----------
    n, m : int
        Chess board of size n by m.

    Notes
    -----
    https://mathworld.wolfram.com/FiveleaperGraph.html
    """
    if m is None:
        m = n
    G = nx.empty_graph(((i, j) for i in range(n) for j in range(m)), create_using)
    G.add_edges_from(
        ((i, j), (i + k, j + l))
        for i in range(n)
        for j in range(m)
        for (k, l) in (
            (5, 0),
            (-5, 0),
            (0, 5),
            (0, -5),
            (3, 4),
            (3, -4),
            (-3, 4),
            (-3, -4),
            (4, 3),
            (4, -3),
            (-4, 3),
            (-4, -3),
        )
        if 0 <= i + k < n and 0 <= j + l < m
    )
    return G


def prism_graph(n, create_using=None):
    """Return the prism graph

    Parameters
    ----------
    n : int

    Notes
    -----
    https://mathworld.wolfram.com/PrismGraph.html
    """
    return nx.cartesian_product(
        nx.path_graph(2, create_using), nx.cycle_graph(n, create_using)
    )


def mobius_ladder_graph(n, create_using=None):
    """Return the Moebius ladder graph

    Parameters
    ----------
    n : int

    Notes
    -----
    https://mathworld.wolfram.com/MoebiusLadder.html
    """
    G = prism_graph(n, create_using=None)
    G.remove_edges_from((((0, 0), (0, 1)), ((1, 0), (1, 1))))
    G.add_edges_from((((0, 0), (1, 1)), ((1, 0), (0, 1))))
    return G


def book_graph(n, create_using=None):
    """Return the book graph of 2n nodes formed from the Cartesian product of a star graph of n nodes
       and a path graph of 2 nodes.

    Parameters
    ----------
    n : int

    Notes
    -----
    https://mathworld.wolfram.com/BookGraph.html
    """
    return nx.cartesian_product(
        nx.star_graph(n, create_using), nx.path_graph(2, create_using)
    )


def stacked_book_graph(n, m=None, create_using=None):
    """Return the stacked book graph of n*m nodes formed from the Cartesian product of a star graph of n nodes
       and a path graph of m nodes.

    Parameters
    ----------
    n, m : int

    Notes
    -----
    https://mathworld.wolfram.com/StackedBookGraph.html
    """
    if m is None:
        m = n
    return nx.cartesian_product(
        nx.star_graph(n, create_using), nx.path_graph(m, create_using)
    )


def odd_graph(n, create_using=None):
    """Return the odd graph of order n

    Parameters
    ----------
    n : int
        order of odd graph

    Notes
    -----
    https://mathworld.wolfram.com/OddGraph.html
    """
    G = nx.empty_graph(combinations(range((n << 1) - 1), n - 1))
    G.add_edges_from((a, b) for a, b in combinations(G, 2) if set(a).isdisjoint(b))
    return G


def fibonacci_cube_graph(n, create_using=None):
    """Return the Fibonacci cube graph

    Parameters
    ----------
    n : int

    Notes
    -----
    https://mathworld.wolfram.com/FibonacciCubeGraph.html
    """

    G = nx.empty_graph(
        int(q, 2)
        for q in ("".join(p) for p in product("01", repeat=n))
        if "11" not in q
    )
    G.add_edges_from(
        (a, b)
        for a, b in combinations(G, 2)
        if (lambda m: not (m & -m) ^ m if m else False)(a ^ b)
    )
    return G


def lucas_cube_graph(n, create_using=None):
    """Return the Lucas cube graph

    Parameters
    ----------
    n : int

    Notes
    -----
    https://mathworld.wolfram.com/LucasCubeGraph.html
    """

    G = nx.empty_graph(
        int(q, 2)
        for q in ("".join(p) for p in product("01", repeat=n))
        if "11" not in q + q[0]
    )
    G.add_edges_from(
        (a, b)
        for a, b in combinations(G, 2)
        if (lambda m: not (m & -m) ^ m if m else False)(a ^ b)
    )
    return G


def halved_cube_graph(n):
    """Return the halved cube graph

    Parameters
    ----------
    n : int

    Notes
    -----
    https://mathworld.wolfram.com/HalvedCubeGraph.html
    """
    if n == 1:
        return nx.trivial_graph()
    return nx.power(nx.hypercube_graph(n - 1), 2)


def folded_cube_graph(n):
    """Return the folded cube graph

    Parameters
    ----------
    n : int

    Notes
    -----
    https://mathworld.wolfram.com/FoldedCubeGraph.html
    """
    G = nx.hypercube_graph(n)
    for a in product((0, 1), repeat=n - 1):
        G = nx.contracted_nodes(G, (0,) + a, (1,) + tuple(1 - d for d in a))
    return G
