#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ai_toolkit.py - Bộ thuật toán AI mini của Nhóm 2
=================================================

Một file duy nhất gom các nhóm thuật toán kinh điển trong môn Trí tuệ nhân tạo:

    [LEADER]    Phần lõi dùng chung: Grid, Graph, SearchResult, tiện ích
    [MEMBER 1]  Tìm kiếm mù (BFS, DFS, DLS, IDS, UCS, Bidirectional)
    [MEMBER 2]  Tìm kiếm có thông tin (Greedy, A*, Weighted A*, IDA*)
    [MEMBER 3]  Tìm kiếm cục bộ / tối ưu (Hill Climbing, SA, GA) trên bài toán TSP
    [MEMBER 4]  Đối kháng + CSP (Minimax, Alpha-Beta, N-Queens, Tô màu bản đồ, Sudoku)
    [SHARED]    REGISTRY, CHANGELOG, main() -> khu vực DỄ CONFLICT khi merge

Cách chạy:
    python ai_toolkit.py --list          # liệt kê thuật toán đã đăng ký
    python ai_toolkit.py --run all       # chạy demo tất cả
    python ai_toolkit.py --run astar     # chạy demo một thuật toán
    python ai_toolkit.py --selftest      # chạy bộ kiểm tra tự động

Quy ước: mỗi member CHỈ sửa trong vùng BEGIN/END của mình, trừ các vùng SHARED.
"""
from __future__ import annotations

import argparse
import heapq
import itertools
import math
import random
import sys
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Dict, Hashable, Iterable, List, Optional, Sequence, Tuple

# =============================================================================
# [LEADER] CẤU HÌNH CHUNG
# =============================================================================
__version__ = "0.1.0"
AUTHORS = ["Leader"]

DEFAULT_SEED = 42            # CONFLICT-ZONE-A: M1 và M2 cùng muốn đổi dòng này
DEFAULT_MAX_ITER = 1000      # CONFLICT-ZONE-B: M3 và M4 cùng muốn đổi dòng này
GRID_ROWS = 15
GRID_COLS = 25
OBSTACLE_RATIO = 0.25
SQRT2 = math.sqrt(2.0)

State = Hashable
DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIRS_DIAG = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


# =============================================================================
# [LEADER] BEGIN - KẾT QUẢ TÌM KIẾM & TIỆN ÍCH
# =============================================================================
@dataclass
class SearchResult:
    """Kết quả chuẩn hóa của mọi thuật toán tìm kiếm đường đi."""

    name: str
    found: bool
    path: List[State] = field(default_factory=list)
    cost: float = math.inf
    expanded: int = 0
    elapsed_ms: float = 0.0
    visited: set = field(default_factory=set)

    def summary(self) -> str:
        if not self.found:
            return (f"{self.name:<18} KHÔNG tìm thấy đường | "
                    f"mở rộng={self.expanded:>6} | {self.elapsed_ms:7.2f} ms")
        return (f"{self.name:<18} cost={self.cost:8.2f} | độ dài={len(self.path):>4} | "
                f"mở rộng={self.expanded:>6} | {self.elapsed_ms:7.2f} ms")


def reconstruct_path(parent: Dict[State, Optional[State]], goal: State) -> List[State]:
    """Dựng đường đi từ bảng cha (parent) về trạng thái bắt đầu."""
    path: List[State] = []
    cur: Optional[State] = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path


def make_result(name: str, found: bool, parent: Dict[State, Optional[State]],
                goal: Optional[State], cost: float, expanded: int,
                t0: float) -> SearchResult:
    """Đóng gói kết quả, tự tính thời gian từ mốc t0 (time.perf_counter)."""
    elapsed = (time.perf_counter() - t0) * 1000.0
    path = reconstruct_path(parent, goal) if (found and goal is not None) else []
    return SearchResult(name, found, path, cost if found else math.inf,
                        expanded, elapsed, set(parent.keys()))


def compute_path_cost(problem, path: Sequence[State]) -> float:
    """Tính lại chi phí của một đường đi bằng cách tra bảng neighbors."""
    total = 0.0
    for a, b in zip(path, path[1:]):
        step = None
        for nxt, c in problem.neighbors(a):
            if nxt == b:
                step = c
                break
        if step is None:
            return math.inf
        total += step
    return total


def timed(fn: Callable) -> Callable:
    """Decorator đo thời gian chạy, in ra khi bật DEBUG_TIMING."""
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()
        out = fn(*args, **kwargs)
        if DEBUG_TIMING:
            print(f"  [timing] {fn.__name__}: {(time.perf_counter() - t0) * 1000:.2f} ms")
        return out
    wrapper.__name__ = fn.__name__
    wrapper.__doc__ = fn.__doc__
    return wrapper


DEBUG_TIMING = False


def banner(title: str, width: int = 72) -> str:
    line = "=" * width
    return f"\n{line}\n{title}\n{line}"


# -----------------------------------------------------------------------------
# Bài toán Lưới (Grid) - dùng chung cho tìm kiếm mù và có thông tin
# -----------------------------------------------------------------------------
class Grid:
    """Lưới 2D có tường. Trạng thái là tuple (row, col)."""

    def __init__(self, rows: int, cols: int, walls: Optional[Iterable[Tuple[int, int]]] = None,
                 start: Tuple[int, int] = (0, 0), goal: Optional[Tuple[int, int]] = None,
                 diagonal: bool = False) -> None:
        self.rows = rows
        self.cols = cols
        self.walls = set(walls or ())
        self.start = start
        self.goal = goal if goal is not None else (rows - 1, cols - 1)
        self.diagonal = diagonal

    def in_bounds(self, p: Tuple[int, int]) -> bool:
        return 0 <= p[0] < self.rows and 0 <= p[1] < self.cols

    def passable(self, p: Tuple[int, int]) -> bool:
        return self.in_bounds(p) and p not in self.walls

    def is_goal(self, s: State) -> bool:
        return s == self.goal

    def neighbors(self, s: Tuple[int, int]) -> List[Tuple[Tuple[int, int], float]]:
        r, c = s
        out: List[Tuple[Tuple[int, int], float]] = []
        for dr, dc in DIRS_4:
            n = (r + dr, c + dc)
            if self.passable(n):
                out.append((n, 1.0))
        if self.diagonal:
            for dr, dc in DIRS_DIAG:
                n = (r + dr, c + dc)
                # không cho cắt góc tường
                if self.passable(n) and self.passable((r + dr, c)) and self.passable((r, c + dc)):
                    out.append((n, SQRT2))
        return out

    @classmethod
    def random_grid(cls, rows: int = GRID_ROWS, cols: int = GRID_COLS,
                    ratio: float = OBSTACLE_RATIO, seed: int = DEFAULT_SEED,
                    diagonal: bool = False) -> "Grid":
        """Sinh lưới ngẫu nhiên, đảm bảo luôn có đường từ start tới goal."""
        rng = random.Random(seed)
        start, goal = (0, 0), (rows - 1, cols - 1)
        for _ in range(300):
            walls = {(r, c) for r in range(rows) for c in range(cols)
                     if rng.random() < ratio and (r, c) not in (start, goal)}
            g = cls(rows, cols, walls, start, goal, diagonal)
            if g._reachable():
                return g
        return cls(rows, cols, set(), start, goal, diagonal)

    def _reachable(self) -> bool:
        seen = {self.start}
        queue = deque([self.start])
        while queue:
            cur = queue.popleft()
            if cur == self.goal:
                return True
            for n, _ in self.neighbors(cur):
                if n not in seen:
                    seen.add(n)
                    queue.append(n)
        return False

    def render(self, path: Optional[Sequence[State]] = None,
               visited: Optional[set] = None) -> str:
        """Vẽ lưới ra text: S=start, G=goal, #=tường, *=đường đi, o=đã duyệt."""
        on_path = set(path or ())
        seen = visited or set()
        lines = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                p = (r, c)
                if p == self.start:
                    ch = "S"
                elif p == self.goal:
                    ch = "G"
                elif p in self.walls:
                    ch = "#"
                elif p in on_path:
                    ch = "*"
                elif p in seen:
                    ch = "o"
                else:
                    ch = "."
                row.append(ch)
            lines.append("".join(row))
        return "\n".join(lines)


# -----------------------------------------------------------------------------
# Bài toán Đồ thị có trọng số (bản đồ Romania rút gọn)
# -----------------------------------------------------------------------------
class Graph:
    """Đồ thị có trọng số, lưu danh sách kề."""

    def __init__(self) -> None:
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def add_edge(self, u: str, v: str, w: float, directed: bool = False) -> None:
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, [])
        if not directed:
            self.adj[v].append((u, w))

    def nodes(self) -> List[str]:
        return sorted(self.adj)

    @classmethod
    def romania(cls) -> "Graph":
        g = cls()
        edges = [
            ("Arad", "Zerind", 75), ("Arad", "Sibiu", 140), ("Arad", "Timisoara", 118),
            ("Zerind", "Oradea", 71), ("Oradea", "Sibiu", 151), ("Timisoara", "Lugoj", 111),
            ("Lugoj", "Mehadia", 70), ("Mehadia", "Drobeta", 75), ("Drobeta", "Craiova", 120),
            ("Craiova", "Rimnicu", 146), ("Craiova", "Pitesti", 138), ("Sibiu", "Fagaras", 99),
            ("Sibiu", "Rimnicu", 80), ("Rimnicu", "Pitesti", 97), ("Pitesti", "Bucharest", 101),
            ("Fagaras", "Bucharest", 211), ("Bucharest", "Giurgiu", 90),
        ]
        for u, v, w in edges:
            g.add_edge(u, v, w)
        return g

    # khoảng cách đường chim bay tới Bucharest (dùng làm heuristic)
    ROMANIA_SLD = {
        "Arad": 366, "Bucharest": 0, "Craiova": 160, "Drobeta": 242, "Fagaras": 176,
        "Giurgiu": 77, "Lugoj": 244, "Mehadia": 241, "Oradea": 380, "Pitesti": 100,
        "Rimnicu": 193, "Sibiu": 253, "Timisoara": 329, "Zerind": 374,
    }


class GraphProblem:
    """Bọc Graph thành bài toán tìm đường start -> goal."""

    def __init__(self, graph: Graph, start: str, goal: str) -> None:
        self.graph = graph
        self.start = start
        self.goal = goal

    def is_goal(self, s: State) -> bool:
        return s == self.goal

    def neighbors(self, s: str) -> List[Tuple[str, float]]:
        return list(self.graph.adj.get(s, []))


# =============================================================================
# [LEADER] END
# =============================================================================


# =============================================================================
# [MEMBER 1] BEGIN - TÌM KIẾM MÙ (UNINFORMED SEARCH)
# Phụ trách: Member 1 | Nhánh: feature/uninformed-search
# =============================================================================
def bfs(problem) -> SearchResult:
    """Breadth-First Search: mở rộng theo từng lớp, tối ưu khi chi phí bước đều nhau."""
    t0 = time.perf_counter()
    start = problem.start
    parent: Dict[State, Optional[State]] = {start: None}
    g: Dict[State, float] = {start: 0.0}
    if problem.is_goal(start):
        return make_result("BFS", True, parent, start, 0.0, 0, t0)
    frontier = deque([start])
    expanded = 0
    while frontier:
        s = frontier.popleft()
        expanded += 1
        for n, c in problem.neighbors(s):
            if n in parent:
                continue
            parent[n] = s
            g[n] = g[s] + c
            if problem.is_goal(n):
                return make_result("BFS", True, parent, n, g[n], expanded, t0)
            frontier.append(n)
    return make_result("BFS", False, parent, None, math.inf, expanded, t0)


def dfs(problem) -> SearchResult:
    """Depth-First Search (lặp, dùng stack): nhanh nhưng KHÔNG đảm bảo tối ưu."""
    t0 = time.perf_counter()
    start = problem.start
    parent: Dict[State, Optional[State]] = {start: None}
    g: Dict[State, float] = {start: 0.0}
    stack = [start]
    explored = set()
    expanded = 0
    while stack:
        s = stack.pop()
        if s in explored:
            continue
        explored.add(s)
        expanded += 1
        if problem.is_goal(s):
            return make_result("DFS", True, parent, s, g[s], expanded, t0)
        for n, c in reversed(problem.neighbors(s)):
            if n not in explored and n not in parent:
                parent[n] = s
                g[n] = g[s] + c
                stack.append(n)
    return make_result("DFS", False, parent, None, math.inf, expanded, t0)


CUTOFF = "cutoff"


def depth_limited_search(problem, limit: int) -> SearchResult:
    """Depth-Limited Search (đệ quy). Trả về found=False nếu chạm giới hạn độ sâu."""
    t0 = time.perf_counter()
    counter = {"expanded": 0}
    parent: Dict[State, Optional[State]] = {problem.start: None}
    costs: Dict[State, float] = {problem.start: 0.0}

    def recurse(s: State, depth: int, on_path: set):
        counter["expanded"] += 1
        if problem.is_goal(s):
            return s
        if depth == limit:
            return CUTOFF
        cutoff_occurred = False
        for n, c in problem.neighbors(s):
            if n in on_path:
                continue  # tránh vòng lặp trên đường hiện tại
            parent[n] = s
            costs[n] = costs[s] + c
            on_path.add(n)
            result = recurse(n, depth + 1, on_path)
            on_path.discard(n)
            if result == CUTOFF:
                cutoff_occurred = True
            elif result is not None:
                return result
        return CUTOFF if cutoff_occurred else None

    outcome = recurse(problem.start, 0, {problem.start})
    if outcome is None or outcome == CUTOFF:
        return make_result(f"DLS(l={limit})", False, parent, None, math.inf,
                           counter["expanded"], t0)
    return make_result(f"DLS(l={limit})", True, parent, outcome, costs[outcome],
                       counter["expanded"], t0)


def iterative_deepening_search(problem, max_depth: int = 200) -> SearchResult:
    """IDS: lặp DLS với giới hạn tăng dần; tối ưu theo số bước, tốn ít bộ nhớ."""
    t0 = time.perf_counter()
    total_expanded = 0
    for limit in range(max_depth + 1):
        res = depth_limited_search(problem, limit)
        total_expanded += res.expanded
        if res.found:
            res.name = "IDS"
            res.expanded = total_expanded
            res.elapsed_ms = (time.perf_counter() - t0) * 1000.0
            return res
    return SearchResult("IDS", False, [], math.inf, total_expanded,
                        (time.perf_counter() - t0) * 1000.0)


def uniform_cost_search(problem) -> SearchResult:
    """UCS (Dijkstra): luôn mở rộng nút có g nhỏ nhất, tối ưu với chi phí không âm."""
    t0 = time.perf_counter()
    start = problem.start
    tie = itertools.count()
    parent: Dict[State, Optional[State]] = {start: None}
    best: Dict[State, float] = {start: 0.0}
    heap = [(0.0, next(tie), start)]
    closed = set()
    expanded = 0
    while heap:
        g, _, s = heapq.heappop(heap)
        if s in closed:
            continue
        closed.add(s)
        expanded += 1
        if problem.is_goal(s):
            return make_result("UCS", True, parent, s, g, expanded, t0)
        for n, c in problem.neighbors(s):
            ng = g + c
            if n not in best or ng < best[n]:
                best[n] = ng
                parent[n] = s
                heapq.heappush(heap, (ng, next(tie), n))
    return make_result("UCS", False, parent, None, math.inf, expanded, t0)


def bidirectional_bfs(problem) -> SearchResult:
    """BFS hai chiều (chỉ dùng cho đồ thị vô hướng, ví dụ Grid)."""
    t0 = time.perf_counter()
    start, goal = problem.start, problem.goal
    if start == goal:
        return make_result("Bidirectional", True, {start: None}, start, 0.0, 0, t0)
    parent_f: Dict[State, Optional[State]] = {start: None}
    parent_b: Dict[State, Optional[State]] = {goal: None}
    front_f, front_b = deque([start]), deque([goal])
    expanded = 0
    meet: Optional[State] = None

    def expand_layer(frontier, mine, other):
        nonlocal expanded
        for _ in range(len(frontier)):
            s = frontier.popleft()
            expanded += 1
            for n, _c in problem.neighbors(s):
                if n in mine:
                    continue
                mine[n] = s
                if n in other:
                    return n
                frontier.append(n)
        return None

    while front_f and front_b and meet is None:
        if len(front_f) <= len(front_b):
            meet = expand_layer(front_f, parent_f, parent_b)
        else:
            meet = expand_layer(front_b, parent_b, parent_f)
    if meet is None:
        return make_result("Bidirectional", False, parent_f, None, math.inf, expanded, t0)
    left = reconstruct_path(parent_f, meet)    # start -> meet
    right = reconstruct_path(parent_b, meet)   # goal -> meet (gốc là goal)
    full = left + right[::-1][1:]              # nối meet -> goal
    cost = compute_path_cost(problem, full)
    elapsed = (time.perf_counter() - t0) * 1000.0
    visited = set(parent_f) | set(parent_b)
    return SearchResult("Bidirectional", True, full, cost, expanded, elapsed, visited)


def count_reachable(problem) -> int:
    """Đếm số trạng thái đi tới được từ start (tiện ích để kiểm thử BFS)."""
    seen = {problem.start}
    queue = deque([problem.start])
    while queue:
        s = queue.popleft()
        for n, _ in problem.neighbors(s):
            if n not in seen:
                seen.add(n)
                queue.append(n)
    return len(seen)


def shortest_hops(problem) -> int:
    """Số bước ngắn nhất (không tính trọng số) từ start tới goal, -1 nếu không có."""
    res = bfs(problem)
    return len(res.path) - 1 if res.found else -1


# TODO(M1): thêm hàm `bfs_all_shortest_paths(problem)` trả về TẤT CẢ đường ngắn nhất.
# TODO(M1): thêm hàm `detect_cycle(graph)` kiểm tra đồ thị có chu trình không.


def demo_uninformed() -> str:
    grid = Grid.random_grid(seed=DEFAULT_SEED)
    out = [banner("[M1] TÌM KIẾM MÙ trên lưới %dx%d" % (grid.rows, grid.cols))]
    for algo in (bfs, dfs, uniform_cost_search, bidirectional_bfs):
        out.append(algo(grid).summary())
    # IDS có độ phức tạp mũ -> chỉ demo trên lưới nhỏ 6x6 để chạy nhanh
    small = Grid.random_grid(rows=6, cols=6, ratio=0.15, seed=DEFAULT_SEED)
    out.append("Lưới nhỏ 6x6 (cho IDS): " + iterative_deepening_search(small, max_depth=20).summary())
    res = bfs(grid)
    if res.found:
        out.append("\nĐường đi BFS:")
        out.append(grid.render(res.path))
    gp = GraphProblem(Graph.romania(), "Arad", "Bucharest")
    out.append("\nBản đồ Romania: Arad -> Bucharest")
    for algo in (bfs, uniform_cost_search):
        r = algo(gp)
        out.append(r.summary() + "  " + " > ".join(map(str, r.path)))
    return "\n".join(out)


# =============================================================================
# [MEMBER 1] END
# =============================================================================


# =============================================================================
# [MEMBER 2] BEGIN - TÌM KIẾM CÓ THÔNG TIN (INFORMED SEARCH)
# Phụ trách: Member 2 | Nhánh: feature/informed-search
# =============================================================================
Heuristic = Callable[[State], float]


def manhattan(goal: Tuple[int, int]) -> Heuristic:
    """Heuristic Manhattan: chấp nhận được khi chỉ đi 4 hướng."""
    gr, gc = goal
    return lambda s: abs(s[0] - gr) + abs(s[1] - gc)


def euclidean(goal: Tuple[int, int]) -> Heuristic:
    """Heuristic Euclid: chấp nhận được với cả 4 và 8 hướng."""
    gr, gc = goal
    return lambda s: math.hypot(s[0] - gr, s[1] - gc)


def chebyshev(goal: Tuple[int, int]) -> Heuristic:
    """Heuristic Chebyshev: phù hợp khi đi chéo có cùng chi phí với đi thẳng."""
    gr, gc = goal
    return lambda s: max(abs(s[0] - gr), abs(s[1] - gc))


def octile(goal: Tuple[int, int]) -> Heuristic:
    """Heuristic Octile: chuẩn cho lưới 8 hướng với chi phí chéo = sqrt(2)."""
    gr, gc = goal

    def h(s: Tuple[int, int]) -> float:
        dr, dc = abs(s[0] - gr), abs(s[1] - gc)
        return (dr + dc) + (SQRT2 - 2.0) * min(dr, dc)
    return h


def zero_heuristic() -> Heuristic:
    """h(n) = 0 -> A* suy biến thành UCS (dùng để đối chứng)."""
    return lambda s: 0.0


def table_heuristic(table: Dict[State, float]) -> Heuristic:
    """Heuristic tra bảng (ví dụ khoảng cách chim bay trên bản đồ Romania)."""
    return lambda s: table.get(s, 0.0)


def greedy_best_first(problem, h: Heuristic) -> SearchResult:
    """Greedy Best-First: chỉ xét h(n). Nhanh nhưng không tối ưu."""
    t0 = time.perf_counter()
    start = problem.start
    tie = itertools.count()
    parent: Dict[State, Optional[State]] = {start: None}
    g: Dict[State, float] = {start: 0.0}
    heap = [(h(start), next(tie), start)]
    closed = set()
    expanded = 0
    while heap:
        _, _, s = heapq.heappop(heap)
        if s in closed:
            continue
        closed.add(s)
        expanded += 1
        if problem.is_goal(s):
            return make_result("Greedy", True, parent, s, g[s], expanded, t0)
        for n, c in problem.neighbors(s):
            if n not in parent:
                parent[n] = s
                g[n] = g[s] + c
                heapq.heappush(heap, (h(n), next(tie), n))
    return make_result("Greedy", False, parent, None, math.inf, expanded, t0)


def astar(problem, h: Heuristic, name: str = "A*") -> SearchResult:
    """A*: f(n) = g(n) + h(n). Tối ưu nếu h chấp nhận được và nhất quán."""
    return weighted_astar(problem, h, weight=1.0, name=name)


def weighted_astar(problem, h: Heuristic, weight: float = 1.5,
                   name: Optional[str] = None) -> SearchResult:
    """Weighted A*: f = g + w*h. w > 1 chạy nhanh hơn nhưng có thể lệch tối ưu."""
    label = name or f"WA*(w={weight})"
    t0 = time.perf_counter()
    start = problem.start
    tie = itertools.count()
    parent: Dict[State, Optional[State]] = {start: None}
    best: Dict[State, float] = {start: 0.0}
    heap = [(weight * h(start), next(tie), start)]
    closed = set()
    expanded = 0
    while heap:
        _, _, s = heapq.heappop(heap)
        if s in closed:
            continue
        closed.add(s)
        expanded += 1
        if problem.is_goal(s):
            return make_result(label, True, parent, s, best[s], expanded, t0)
        for n, c in problem.neighbors(s):
            ng = best[s] + c
            if n not in best or ng < best[n]:
                best[n] = ng
                parent[n] = s
                closed.discard(n)  # cho phép mở lại nếu tìm được đường rẻ hơn
                heapq.heappush(heap, (ng + weight * h(n), next(tie), n))
    return make_result(label, False, parent, None, math.inf, expanded, t0)


def ida_star(problem, h: Heuristic, max_iterations: int = 200) -> SearchResult:
    """IDA*: A* lặp sâu dần theo ngưỡng f, tốn rất ít bộ nhớ."""
    t0 = time.perf_counter()
    start = problem.start
    expanded = 0
    path: List[State] = [start]
    on_path = {start}

    def search(g: float, threshold: float):
        nonlocal expanded
        s = path[-1]
        f = g + h(s)
        if f > threshold:
            return f
        if problem.is_goal(s):
            return "FOUND"
        expanded += 1
        minimum = math.inf
        for n, c in problem.neighbors(s):
            if n in on_path:
                continue
            path.append(n)
            on_path.add(n)
            t = search(g + c, threshold)
            if t == "FOUND":
                return "FOUND"
            if t < minimum:
                minimum = t
            path.pop()
            on_path.discard(n)
        return minimum

    threshold = h(start)
    for _ in range(max_iterations):
        t = search(0.0, threshold)
        if t == "FOUND":
            elapsed = (time.perf_counter() - t0) * 1000.0
            return SearchResult("IDA*", True, list(path), compute_path_cost(problem, path),
                                expanded, elapsed, set(path))
        if t == math.inf:
            break
        threshold = t
    return SearchResult("IDA*", False, [], math.inf, expanded,
                        (time.perf_counter() - t0) * 1000.0)


def compare_heuristics(grid: Grid) -> List[SearchResult]:
    """Chạy A* với nhiều heuristic để so sánh số nút mở rộng."""
    goal = grid.goal
    candidates = [
        ("A*-zero", zero_heuristic()),
        ("A*-manhattan", manhattan(goal)),
        ("A*-euclid", euclidean(goal)),
        ("A*-chebyshev", chebyshev(goal)),
    ]
    if grid.diagonal:
        candidates.append(("A*-octile", octile(goal)))
    return [astar(grid, hf, name=label) for label, hf in candidates]


def is_admissible(grid: Grid, h: Heuristic, samples: int = 30, seed: int = DEFAULT_SEED) -> bool:
    """Kiểm tra thực nghiệm h có chấp nhận được không (h <= chi phí thật)."""
    rng = random.Random(seed)
    cells = [(r, c) for r in range(grid.rows) for c in range(grid.cols) if grid.passable((r, c))]
    rng.shuffle(cells)
    for cell in cells[:samples]:
        sub = Grid(grid.rows, grid.cols, grid.walls, cell, grid.goal, grid.diagonal)
        real = bfs_cost_dijkstra(sub)
        if real is not None and h(cell) > real + 1e-9:
            return False
    return True


def bfs_cost_dijkstra(problem) -> Optional[float]:
    """Dijkstra gọn: trả về chi phí tối ưu hoặc None nếu không có đường."""
    tie = itertools.count()
    best = {problem.start: 0.0}
    heap = [(0.0, next(tie), problem.start)]
    while heap:
        g, _, s = heapq.heappop(heap)
        if g > best.get(s, math.inf):
            continue
        if problem.is_goal(s):
            return g
        for n, c in problem.neighbors(s):
            if g + c < best.get(n, math.inf):
                best[n] = g + c
                heapq.heappush(heap, (g + c, next(tie), n))
    return None


# TODO(M2): thêm hàm `beam_search(problem, h, beam_width)` (Beam Search).
# TODO(M2): thêm hàm `bidirectional_astar(problem, h)` nếu còn thời gian.


def demo_informed() -> str:
    grid = Grid.random_grid(seed=DEFAULT_SEED, diagonal=False)
    out = [banner("[M2] TÌM KIẾM CÓ THÔNG TIN trên lưới %dx%d" % (grid.rows, grid.cols))]
    hm = manhattan(grid.goal)
    out.append(greedy_best_first(grid, hm).summary())
    out.append(astar(grid, hm).summary())
    out.append(weighted_astar(grid, hm, 2.0).summary())
    out.append(ida_star(grid, hm).summary())
    out.append("\nSo sánh heuristic:")
    for r in compare_heuristics(grid):
        out.append("  " + r.summary())
    gd = Grid.random_grid(seed=DEFAULT_SEED, diagonal=True)
    out.append("\nLưới 8 hướng (octile):")
    out.append("  " + astar(gd, octile(gd.goal), name="A*-octile").summary())
    gp = GraphProblem(Graph.romania(), "Arad", "Bucharest")
    ht = table_heuristic(Graph.ROMANIA_SLD)
    out.append("\nBản đồ Romania: Arad -> Bucharest")
    for r in (greedy_best_first(gp, ht), astar(gp, ht)):
        out.append(r.summary() + "  " + " > ".join(map(str, r.path)))
    return "\n".join(out)


# =============================================================================
# [MEMBER 2] END
# =============================================================================


# =============================================================================
# [MEMBER 3] BEGIN - TÌM KIẾM CỤC BỘ & TỐI ƯU (LOCAL SEARCH)
# Phụ trách: Member 3 | Nhánh: feature/local-search
# Bài toán minh họa: Người bán hàng du lịch (TSP)
# =============================================================================
class TSP:
    """Bài toán TSP: tìm chu trình ngắn nhất đi qua mọi thành phố đúng một lần."""

    def __init__(self, cities: Sequence[Tuple[float, float]]) -> None:
        self.cities = list(cities)
        self.n = len(self.cities)
        self.dist = [[math.dist(a, b) for b in self.cities] for a in self.cities]

    @classmethod
    def random(cls, n: int = 30, seed: int = DEFAULT_SEED, size: float = 100.0) -> "TSP":
        rng = random.Random(seed)
        return cls([(rng.uniform(0, size), rng.uniform(0, size)) for _ in range(n)])

    def tour_length(self, tour: Sequence[int]) -> float:
        total = 0.0
        for i in range(self.n):
            total += self.dist[tour[i]][tour[(i + 1) % self.n]]
        return total

    def random_tour(self, rng: random.Random) -> List[int]:
        tour = list(range(self.n))
        rng.shuffle(tour)
        return tour


@dataclass
class OptResult:
    """Kết quả của thuật toán tối ưu cục bộ."""

    name: str
    best: List[int]
    best_value: float
    iterations: int
    history: List[float] = field(default_factory=list)
    elapsed_ms: float = 0.0

    def summary(self) -> str:
        return (f"{self.name:<22} độ dài tour={self.best_value:9.2f} | "
                f"vòng lặp={self.iterations:>6} | {self.elapsed_ms:8.2f} ms")


def nearest_neighbor_tour(tsp: TSP, start: int = 0) -> List[int]:
    """Heuristic tham lam: luôn đi tới thành phố gần nhất chưa thăm."""
    unvisited = set(range(tsp.n))
    unvisited.discard(start)
    tour = [start]
    while unvisited:
        last = tour[-1]
        nxt = min(unvisited, key=lambda j: tsp.dist[last][j])
        tour.append(nxt)
        unvisited.discard(nxt)
    return tour


def two_opt_swap(tour: Sequence[int], i: int, j: int) -> List[int]:
    """Đảo đoạn tour[i..j] (phép biến đổi láng giềng 2-opt)."""
    return list(tour[:i]) + list(reversed(tour[i:j + 1])) + list(tour[j + 1:])


def hill_climbing(tsp: TSP, max_iter: int = DEFAULT_MAX_ITER, restarts: int = 5,
                  seed: int = DEFAULT_SEED) -> OptResult:
    """Hill Climbing (steepest ascent) + random restart với láng giềng 2-opt."""
    t0 = time.perf_counter()
    rng = random.Random(seed)
    best_tour: List[int] = []
    best_val = math.inf
    history: List[float] = []
    iters = 0
    for _ in range(restarts):
        tour = tsp.random_tour(rng)
        cur_val = tsp.tour_length(tour)
        improved = True
        while improved and iters < max_iter:
            improved = False
            best_move = None
            best_move_val = cur_val
            for i in range(1, tsp.n - 1):
                for j in range(i + 1, tsp.n):
                    cand = two_opt_swap(tour, i, j)
                    val = tsp.tour_length(cand)
                    if val < best_move_val - 1e-12:
                        best_move, best_move_val = cand, val
            iters += 1
            if best_move is not None:
                tour, cur_val = best_move, best_move_val
                improved = True
            history.append(cur_val)
        if cur_val < best_val:
            best_tour, best_val = tour, cur_val
    return OptResult("HillClimbing+Restart", best_tour, best_val, iters, history,
                     (time.perf_counter() - t0) * 1000.0)


def simulated_annealing(tsp: TSP, t_start: float = 100.0, t_end: float = 1e-3,
                        cooling: float = 0.995, max_iter: int = DEFAULT_MAX_ITER * 20,
                        seed: int = DEFAULT_SEED) -> OptResult:
    """Simulated Annealing: chấp nhận nước đi xấu với xác suất exp(-delta/T)."""
    t0 = time.perf_counter()
    rng = random.Random(seed)
    cur = nearest_neighbor_tour(tsp)
    cur_val = tsp.tour_length(cur)
    best, best_val = list(cur), cur_val
    temp = t_start
    history: List[float] = []
    it = 0
    while temp > t_end and it < max_iter:
        i, j = sorted(rng.sample(range(1, tsp.n), 2))
        cand = two_opt_swap(cur, i, j)
        delta = tsp.tour_length(cand) - cur_val
        if delta < 0 or rng.random() < math.exp(-delta / temp):
            cur, cur_val = cand, cur_val + delta
            if cur_val < best_val:
                best, best_val = list(cur), cur_val
        temp *= cooling
        it += 1
        if it % 50 == 0:
            history.append(best_val)
    return OptResult("SimulatedAnnealing", best, tsp.tour_length(best), it, history,
                     (time.perf_counter() - t0) * 1000.0)


def order_crossover(p1: Sequence[int], p2: Sequence[int], rng: random.Random) -> List[int]:
    """Order Crossover (OX): giữ một đoạn của p1, phần còn lại lấy theo thứ tự p2."""
    n = len(p1)
    a, b = sorted(rng.sample(range(n), 2))
    child: List[Optional[int]] = [None] * n
    child[a:b + 1] = list(p1[a:b + 1])
    taken = set(child[a:b + 1])
    fill = [x for x in p2 if x not in taken]
    idx = 0
    for i in range(n):
        if child[i] is None:
            child[i] = fill[idx]
            idx += 1
    return [int(x) for x in child]  # type: ignore[arg-type]


def swap_mutation(tour: List[int], rng: random.Random) -> List[int]:
    """Đột biến: hoán đổi hai thành phố ngẫu nhiên."""
    i, j = rng.sample(range(len(tour)), 2)
    tour = list(tour)
    tour[i], tour[j] = tour[j], tour[i]
    return tour


def tournament_select(pop: List[List[int]], fitness: List[float], k: int,
                      rng: random.Random) -> List[int]:
    """Chọn lọc giải đấu: lấy cá thể tốt nhất trong k cá thể ngẫu nhiên."""
    picks = rng.sample(range(len(pop)), min(k, len(pop)))
    winner = min(picks, key=lambda i: fitness[i])
    return pop[winner]


def genetic_algorithm(tsp: TSP, pop_size: int = 80, generations: int = 300,
                      mutation_rate: float = 0.2, elite: int = 2, tournament_k: int = 4,
                      seed: int = DEFAULT_SEED) -> OptResult:
    """Thuật toán di truyền: quần thể tour, lai ghép OX, đột biến hoán đổi, giữ elite."""
    t0 = time.perf_counter()
    rng = random.Random(seed)
    pop = [tsp.random_tour(rng) for _ in range(pop_size)]
    pop[0] = nearest_neighbor_tour(tsp)  # gieo một cá thể tốt
    history: List[float] = []
    best, best_val = pop[0], tsp.tour_length(pop[0])
    for _gen in range(generations):
        fitness = [tsp.tour_length(t) for t in pop]
        order = sorted(range(pop_size), key=lambda i: fitness[i])
        if fitness[order[0]] < best_val:
            best, best_val = list(pop[order[0]]), fitness[order[0]]
        history.append(best_val)
        new_pop = [list(pop[i]) for i in order[:elite]]
        while len(new_pop) < pop_size:
            p1 = tournament_select(pop, fitness, tournament_k, rng)
            p2 = tournament_select(pop, fitness, tournament_k, rng)
            child = order_crossover(p1, p2, rng)
            if rng.random() < mutation_rate:
                child = swap_mutation(child, rng)
            new_pop.append(child)
        pop = new_pop
    return OptResult("GeneticAlgorithm", best, best_val, generations, history,
                     (time.perf_counter() - t0) * 1000.0)


def rastrigin(x: Sequence[float]) -> float:
    """Hàm Rastrigin: nhiều cực tiểu địa phương, cực tiểu toàn cục = 0 tại x=0."""
    return 10 * len(x) + sum(v * v - 10 * math.cos(2 * math.pi * v) for v in x)


def annealing_continuous(f: Callable[[Sequence[float]], float], dim: int = 3,
                         bound: float = 5.12, iterations: int = 20000,
                         seed: int = DEFAULT_SEED) -> Tuple[List[float], float]:
    """SA cho hàm liên tục: dùng để minh họa thoát cực tiểu địa phương."""
    rng = random.Random(seed)
    x = [rng.uniform(-bound, bound) for _ in range(dim)]
    fx = f(x)
    best, best_f = list(x), fx
    for k in range(iterations):
        temp = 5.0 * (1.0 - k / iterations) + 1e-6
        cand = [min(bound, max(-bound, v + rng.gauss(0, 0.3))) for v in x]
        fc = f(cand)
        if fc < fx or rng.random() < math.exp(-(fc - fx) / temp):
            x, fx = cand, fc
            if fx < best_f:
                best, best_f = list(x), fx
    return best, best_f


# TODO(M3): thêm hàm `tabu_search(tsp, ...)` (Tabu Search).
# TODO(M3): thêm hàm `plot_history(result)` vẽ đồ thị hội tụ bằng matplotlib (tùy chọn).


def demo_local() -> str:
    tsp = TSP.random(n=25, seed=DEFAULT_SEED)
    out = [banner("[M3] TÌM KIẾM CỤC BỘ trên TSP (%d thành phố)" % tsp.n)]
    nn = nearest_neighbor_tour(tsp)
    out.append(f"{'NearestNeighbor':<22} độ dài tour={tsp.tour_length(nn):9.2f}")
    out.append(hill_climbing(tsp, max_iter=300, restarts=3).summary())
    out.append(simulated_annealing(tsp).summary())
    out.append(genetic_algorithm(tsp, generations=200).summary())
    xb, fb = annealing_continuous(rastrigin)
    out.append(f"\nSA liên tục trên Rastrigin: f_min={fb:.4f} tại x={[round(v, 3) for v in xb]}")
    return "\n".join(out)


# =============================================================================
# [MEMBER 3] END
# =============================================================================


# =============================================================================
# [MEMBER 4] BEGIN - TÌM KIẾM ĐỐI KHÁNG & CSP
# Phụ trách: Member 4 | Nhánh: feature/adversarial-csp
# =============================================================================
WIN_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (0, 4, 8), (2, 4, 6)]


class TicTacToe:
    """Cờ ca-rô 3x3. Bàn cờ là tuple 9 phần tử: 'X', 'O' hoặc ' '."""

    EMPTY = " "

    @staticmethod
    def initial() -> Tuple[str, ...]:
        return tuple(" " for _ in range(9))

    @staticmethod
    def player(board: Tuple[str, ...]) -> str:
        return "X" if board.count("X") == board.count("O") else "O"

    @staticmethod
    def actions(board: Tuple[str, ...]) -> List[int]:
        return [i for i, v in enumerate(board) if v == " "]

    @staticmethod
    def result(board: Tuple[str, ...], move: int) -> Tuple[str, ...]:
        b = list(board)
        b[move] = TicTacToe.player(board)
        return tuple(b)

    @staticmethod
    def winner(board: Tuple[str, ...]) -> Optional[str]:
        for a, b, c in WIN_LINES:
            if board[a] != " " and board[a] == board[b] == board[c]:
                return board[a]
        return None

    @staticmethod
    def terminal(board: Tuple[str, ...]) -> bool:
        return TicTacToe.winner(board) is not None or " " not in board

    @staticmethod
    def utility(board: Tuple[str, ...]) -> int:
        """+1 nếu X thắng, -1 nếu O thắng, 0 nếu hòa."""
        w = TicTacToe.winner(board)
        return 1 if w == "X" else -1 if w == "O" else 0

    @staticmethod
    def render(board: Tuple[str, ...]) -> str:
        rows = [" " + " | ".join(board[i:i + 3]) for i in (0, 3, 6)]
        return "\n---+---+---\n".join(rows)


class NodeCounter:
    """Đếm số nút được duyệt để so sánh Minimax và Alpha-Beta."""

    def __init__(self) -> None:
        self.nodes = 0


def minimax(board: Tuple[str, ...], counter: Optional[NodeCounter] = None) -> int:
    """Minimax thuần: X là MAX, O là MIN. Trả về giá trị của trạng thái."""
    if counter:
        counter.nodes += 1
    if TicTacToe.terminal(board):
        return TicTacToe.utility(board)
    values = [minimax(TicTacToe.result(board, m), counter) for m in TicTacToe.actions(board)]
    return max(values) if TicTacToe.player(board) == "X" else min(values)


def alphabeta(board: Tuple[str, ...], alpha: float = -math.inf, beta: float = math.inf,
              counter: Optional[NodeCounter] = None) -> int:
    """Minimax với cắt tỉa Alpha-Beta: cùng kết quả nhưng duyệt ít nút hơn."""
    if counter:
        counter.nodes += 1
    if TicTacToe.terminal(board):
        return TicTacToe.utility(board)
    if TicTacToe.player(board) == "X":
        value = -math.inf
        for m in TicTacToe.actions(board):
            value = max(value, alphabeta(TicTacToe.result(board, m), alpha, beta, counter))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return int(value)
    value = math.inf
    for m in TicTacToe.actions(board):
        value = min(value, alphabeta(TicTacToe.result(board, m), alpha, beta, counter))
        beta = min(beta, value)
        if alpha >= beta:
            break
    return int(value)


def best_move(board: Tuple[str, ...], use_alphabeta: bool = True) -> int:
    """Chọn nước đi tối ưu cho người chơi hiện tại."""
    me = TicTacToe.player(board)
    scored = []
    for m in TicTacToe.actions(board):
        nxt = TicTacToe.result(board, m)
        v = alphabeta(nxt) if use_alphabeta else minimax(nxt)
        scored.append((v, m))
    return max(scored)[1] if me == "X" else min(scored)[1]


def play_self(verbose: bool = False) -> Optional[str]:
    """Cho hai máy tối ưu đấu nhau; kết quả đúng luật phải là hòa (None)."""
    board = TicTacToe.initial()
    while not TicTacToe.terminal(board):
        board = TicTacToe.result(board, best_move(board))
        if verbose:
            print(TicTacToe.render(board), "\n")
    return TicTacToe.winner(board)


# -----------------------------------------------------------------------------
# Bài toán thỏa mãn ràng buộc (CSP)
# -----------------------------------------------------------------------------
class CSP:
    """CSP nhị phân: biến, miền giá trị, láng giềng và hàm ràng buộc."""

    def __init__(self, variables: Sequence[Hashable], domains: Dict[Hashable, Sequence],
                 neighbors: Dict[Hashable, Sequence[Hashable]],
                 constraint: Callable[[Hashable, object, Hashable, object], bool]) -> None:
        self.variables = list(variables)
        self.domains = {v: list(domains[v]) for v in self.variables}
        self.neighbors = {v: list(neighbors.get(v, [])) for v in self.variables}
        self.constraint = constraint
        self.nassigned = 0

    def consistent(self, var, val, assignment: Dict) -> bool:
        for other in self.neighbors[var]:
            if other in assignment and not self.constraint(var, val, other, assignment[other]):
                return False
        return True


def ac3(csp: CSP) -> bool:
    """AC-3: lan truyền nhất quán cung. Trả về False nếu có miền rỗng."""
    queue = deque((a, b) for a in csp.variables for b in csp.neighbors[a])
    while queue:
        a, b = queue.popleft()
        revised = False
        for x in list(csp.domains[a]):
            if not any(csp.constraint(a, x, b, y) for y in csp.domains[b]):
                csp.domains[a].remove(x)
                revised = True
        if revised:
            if not csp.domains[a]:
                return False
            for c in csp.neighbors[a]:
                if c != b:
                    queue.append((c, a))
    return True


def backtracking_search(csp: CSP, mrv: bool = True, forward_check: bool = True) -> Optional[Dict]:
    """Quay lui với MRV (biến ít lựa chọn nhất) và Forward Checking."""
    csp.nassigned = 0
    domains = {v: list(d) for v, d in csp.domains.items()}

    def select_var(assignment: Dict):
        unassigned = [v for v in csp.variables if v not in assignment]
        if mrv:
            return min(unassigned, key=lambda v: len(domains[v]))
        return unassigned[0]

    def backtrack(assignment: Dict) -> Optional[Dict]:
        if len(assignment) == len(csp.variables):
            return dict(assignment)
        var = select_var(assignment)
        for val in list(domains[var]):
            if not csp.consistent(var, val, assignment):
                continue
            assignment[var] = val
            csp.nassigned += 1
            pruned: List[Tuple[Hashable, object]] = []
            ok = True
            if forward_check:
                for nb in csp.neighbors[var]:
                    if nb in assignment:
                        continue
                    for x in list(domains[nb]):
                        if not csp.constraint(var, val, nb, x):
                            domains[nb].remove(x)
                            pruned.append((nb, x))
                    if not domains[nb]:
                        ok = False
                        break
            if ok:
                found = backtrack(assignment)
                if found is not None:
                    return found
            for nb, x in pruned:
                domains[nb].append(x)
            del assignment[var]
        return None

    return backtrack({})


def australia_map_coloring(colors: Sequence[str] = ("Red", "Green", "Blue")) -> CSP:
    """Tô màu bản đồ nước Úc: hai bang kề nhau phải khác màu."""
    adj = {
        "WA": ["NT", "SA"], "NT": ["WA", "SA", "Q"], "SA": ["WA", "NT", "Q", "NSW", "V"],
        "Q": ["NT", "SA", "NSW"], "NSW": ["Q", "SA", "V"], "V": ["SA", "NSW"], "T": [],
    }
    return CSP(list(adj), {v: colors for v in adj}, adj, lambda a, x, b, y: x != y)


def nqueens_csp(n: int) -> CSP:
    """N-Queens dạng CSP: biến là cột, giá trị là hàng đặt hậu."""
    cols = list(range(n))

    def no_attack(c1, r1, c2, r2) -> bool:
        return r1 != r2 and abs(r1 - r2) != abs(c1 - c2)

    return CSP(cols, {c: list(range(n)) for c in cols},
               {c: [o for o in cols if o != c] for c in cols}, no_attack)


def count_nqueens(n: int) -> int:
    """Đếm số nghiệm N-Queens bằng quay lui với tập cột/đường chéo."""
    cols, d1, d2 = set(), set(), set()

    def place(r: int) -> int:
        if r == n:
            return 1
        total = 0
        for c in range(n):
            if c in cols or (r - c) in d1 or (r + c) in d2:
                continue
            cols.add(c)
            d1.add(r - c)
            d2.add(r + c)
            total += place(r + 1)
            cols.discard(c)
            d1.discard(r - c)
            d2.discard(r + c)
        return total

    return place(0)


def sudoku_csp(puzzle: str) -> CSP:
    """Sudoku 9x9 dạng CSP. puzzle: chuỗi 81 ký tự, '0' hoặc '.' là ô trống."""
    assert len(puzzle) == 81, "Chuỗi sudoku phải đủ 81 ký tự"
    cells = [(r, c) for r in range(9) for c in range(9)]
    domains = {}
    for (r, c), ch in zip(cells, puzzle):
        domains[(r, c)] = [int(ch)] if ch in "123456789" else list(range(1, 10))
    neighbors: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
    for (r, c) in cells:
        peers = set()
        for k in range(9):
            peers.add((r, k))
            peers.add((k, c))
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                peers.add((i, j))
        peers.discard((r, c))
        neighbors[(r, c)] = sorted(peers)
    return CSP(cells, domains, neighbors, lambda a, x, b, y: x != y)


def render_sudoku(solution: Dict[Tuple[int, int], int]) -> str:
    rows = []
    for r in range(9):
        cells = [str(solution[(r, c)]) for c in range(9)]
        rows.append(" ".join(" ".join(cells[i:i + 3]) for i in (0, 3, 6)).replace("   ", "   "))
        if r in (2, 5):
            rows.append("-" * 21)
    return "\n".join(rows)


SUDOKU_EASY = ("530070000600195000098000060800060003400803001700020006060000280000419005"
               "000080079")


# TODO(M4): thêm hàm `forward_check_only(csp)` hoặc `min_conflicts(csp)` (Min-Conflicts).
# TODO(M4): thêm test cho Sudoku khó hơn (SUDOKU_HARD) và đo thời gian.


def demo_adversarial_csp() -> str:
    out = [banner("[M4] ĐỐI KHÁNG & CSP")]
    empty = TicTacToe.initial()
    c1, c2 = NodeCounter(), NodeCounter()
    v1 = minimax(empty, c1)
    v2 = alphabeta(empty, counter=c2)
    out.append(f"Minimax:    giá trị={v1}, số nút={c1.nodes}")
    out.append(f"Alpha-Beta: giá trị={v2}, số nút={c2.nodes} "
               f"(giảm {100 * (1 - c2.nodes / c1.nodes):.1f}%)")
    out.append(f"Hai máy tối ưu tự đấu -> người thắng: {play_self()}")
    sol = backtracking_search(australia_map_coloring())
    out.append(f"\nTô màu bản đồ Úc: {sol}")
    for n in (6, 8):
        q = backtracking_search(nqueens_csp(n))
        out.append(f"{n}-Queens (CSP): {[q[c] for c in range(n)] if q else None} | "
                   f"tổng nghiệm={count_nqueens(n)}")
    t0 = time.perf_counter()
    puzzle = sudoku_csp(SUDOKU_EASY)
    solved = backtracking_search(puzzle)
    out.append(f"\nSudoku giải trong {(time.perf_counter() - t0) * 1000:.1f} ms:")
    out.append(render_sudoku(solved) if solved else "Không giải được")
    return "\n".join(out)


# =============================================================================
# [MEMBER 4] END
# =============================================================================


# =============================================================================
# [SHARED] BEGIN - TỰ KIỂM TRA (SELFTEST)  -- ai cũng có thể thêm test ở cuối hàm
# =============================================================================
def selftest() -> int:
    """Chạy các kiểm tra tự động. Trả về số test lỗi."""
    failures = 0

    def check(name: str, cond: bool) -> None:
        nonlocal failures
        status = "PASS" if cond else "FAIL"
        if not cond:
            failures += 1
        print(f"  [{status}] {name}")

    print(banner("SELFTEST"))
    grid = Grid.random_grid(seed=DEFAULT_SEED)
    r_bfs, r_ucs = bfs(grid), uniform_cost_search(grid)
    r_a = astar(grid, manhattan(grid.goal))
    r_ida = ida_star(grid, manhattan(grid.goal))
    check("BFS tìm được đường", r_bfs.found)
    check("BFS cost == UCS cost", abs(r_bfs.cost - r_ucs.cost) < 1e-9)
    check("A* cost == UCS cost (tối ưu)", abs(r_a.cost - r_ucs.cost) < 1e-9)
    check("A* mở rộng ít nút hơn UCS", r_a.expanded <= r_ucs.expanded)
    check("IDA* cost == A* cost", abs(r_ida.cost - r_a.cost) < 1e-9)
    check("Bidirectional cost == BFS cost", abs(bidirectional_bfs(grid).cost - r_bfs.cost) < 1e-9)
    check("DFS tìm được đường", dfs(grid).found)
    check("Manhattan chấp nhận được", is_admissible(grid, manhattan(grid.goal)))
    gp = GraphProblem(Graph.romania(), "Arad", "Bucharest")
    ra = astar(gp, table_heuristic(Graph.ROMANIA_SLD))
    check("Romania A* cost = 418", abs(ra.cost - 418) < 1e-9)
    check("Romania UCS cost = 418", abs(uniform_cost_search(gp).cost - 418) < 1e-9)
    tsp = TSP.random(n=15, seed=DEFAULT_SEED)
    nn_len = tsp.tour_length(nearest_neighbor_tour(tsp))
    sa = simulated_annealing(tsp)
    ga = genetic_algorithm(tsp, generations=100)
    check("SA tour hợp lệ", sorted(sa.best) == list(range(tsp.n)))
    check("GA tour hợp lệ", sorted(ga.best) == list(range(tsp.n)))
    check("SA không tệ hơn Nearest Neighbor", sa.best_value <= nn_len + 1e-9)
    check("GA không tệ hơn Nearest Neighbor", ga.best_value <= nn_len + 1e-9)
    empty = TicTacToe.initial()
    check("Minimax(rỗng) = 0 (hòa)", minimax(empty) == 0)
    check("Alpha-Beta == Minimax", alphabeta(empty) == minimax(empty))
    check("Hai máy tối ưu hòa nhau", play_self() is None)
    check("8-Queens có 92 nghiệm", count_nqueens(8) == 92)
    q = backtracking_search(nqueens_csp(8))
    check("8-Queens CSP giải được", q is not None and len(set(q.values())) == 8)
    sol = backtracking_search(sudoku_csp(SUDOKU_EASY))
    check("Sudoku giải được", sol is not None and all(
        len({sol[(r, c)] for c in range(9)}) == 9 for r in range(9)))
    print(f"\nTổng kết: {failures} lỗi")
    return failures


# =============================================================================
# [SHARED] BEGIN - REGISTRY / CHANGELOG / MAIN  (KHU VỰC DỄ CONFLICT)
# =============================================================================
# Mỗi member thêm 1 dòng đăng ký thuật toán của mình NGAY DƯỚI dòng comment này.
# Cố ý đặt sát nhau để khi merge sẽ phát sinh conflict -> Leader xử lý.
REGISTRY: Dict[str, Tuple[str, Callable[[], str]]] = {
    "uninformed": ("Tìm kiếm mù", demo_uninformed),
    "informed": ("Tìm kiếm có thông tin", demo_informed),
    "local": ("Tìm kiếm cục bộ", demo_local),
    "adversarial_csp": ("Đối kháng và CSP", demo_adversarial_csp),
}

CHANGELOG = [
    "v0.1.0 - Leader: khởi tạo khung dự án và 4 khu vực cho 4 member",
]


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Bộ thuật toán AI mini - Nhóm 2")
    p.add_argument("--list", action="store_true", help="liệt kê các demo đã đăng ký")
    p.add_argument("--run", metavar="NAME", help="chạy demo theo tên, hoặc 'all'")
    p.add_argument("--selftest", action="store_true", help="chạy bộ kiểm tra tự động")
    p.add_argument("--changelog", action="store_true", help="in lịch sử thay đổi")
    p.add_argument("--timing", action="store_true", help="bật đo thời gian chi tiết")
    return p


def main(argv: Optional[Sequence[str]] = None) -> int:
    global DEBUG_TIMING
    args = build_parser().parse_args(argv)
    DEBUG_TIMING = args.timing
    if args.list:
        print(f"ai_toolkit v{__version__} - tác giả: {', '.join(AUTHORS)}")
        for key, (desc, _) in REGISTRY.items():
            print(f"  {key:<18} {desc}")
        return 0
    if args.changelog:
        print("\n".join(CHANGELOG))
        return 0
    if args.selftest:
        return 1 if selftest() else 0
    if args.run:
        names = list(REGISTRY) if args.run == "all" else [args.run]
        for name in names:
            if name not in REGISTRY:
                print(f"Không có demo '{name}'. Dùng --list để xem danh sách.")
                return 2
            print(REGISTRY[name][1]())
        return 0
    build_parser().print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
