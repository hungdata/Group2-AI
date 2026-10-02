# AI Toolkit — Bài tập Git teamwork (Nhóm 2)

> **Leader** đã viết sẵn file `ai_toolkit.py` (~1400 dòng, chạy được, có selftest).
> **4 member** mỗi người lấy **1 nhánh riêng**, sửa/bổ sung phần của mình, push và tạo Pull Request.
> **Leader** merge từng nhánh vào `develop`, gặp **conflict** thì xử lý.

Mục tiêu bài tập: luyện quy trình `branch → commit → push → Pull Request → merge → resolve conflict`.

---

## 1. File trong thư mục này

```
ai_toolkit/
├── README.md        ← file này (phân công + hướng dẫn)
└── ai_toolkit.py    ← code thuật toán (chia 4 vùng cho 4 member)
```

Chạy thử trước khi sửa:

```bash
cd ai_toolkit
python ai_toolkit.py --list        # xem các demo
python ai_toolkit.py --run all     # chạy demo
python ai_toolkit.py --selftest    # PHẢI ra "0 lỗi" trước khi push
```

Yêu cầu: Python 3.8+ (không cần cài thư viện ngoài).

---

## 2. Phân công

| Vai trò | Nhánh (branch) | Vùng được sửa trong `ai_toolkit.py` | Thuật toán |
|---|---|---|---|
| **Leader** | `develop` | `[LEADER]` + merge | Grid, Graph, SearchResult, selftest |
| **Member 1** | `feature/member1-uninformed` | `[MEMBER 1]` | BFS, DFS, DLS, IDS, UCS, Bidirectional |
| **Member 2** | `feature/member2-informed` | `[MEMBER 2]` | Greedy, A\*, Weighted A\*, IDA\* |
| **Member 3** | `feature/member3-local-search` | `[MEMBER 3]` | Hill Climbing, Simulated Annealing, GA (TSP) |
| **Member 4** | `feature/member4-adversarial-csp` | `[MEMBER 4]` | Minimax, Alpha-Beta, CSP, N-Queens, Sudoku |

**Quy tắc vàng:** chỉ sửa trong vùng `BEGIN … END` của mình. Đừng sửa code của người khác.

---

## 3. Việc cần làm của từng member

Mỗi member làm **đủ 4 việc (a) → (d)**. Việc (b), (c), (d) cố tình đụng vào **cùng dòng** với người khác để tạo conflict thật.

### 👤 Member 1 — nhánh `feature/member1-uninformed`
- (a) Tại `# TODO(M1)` thêm hàm `bfs_all_shortest_paths(problem)` (trả về mọi đường ngắn nhất) và `detect_cycle(graph)`.
- (b) Đổi `DEFAULT_SEED = 42` thành `DEFAULT_SEED = 7`.
- (c) Trong `AUTHORS = ["Leader"]` thêm tên mình, ví dụ `["Leader", "Member1"]`.
- (d) Trong `REGISTRY` thêm dòng cuối: `"m1_extra": ("M1 - đường ngắn nhất", demo_uninformed),` và thêm 1 dòng vào `CHANGELOG`: `"v0.2.0 - Member1: ..."`.

### 👤 Member 2 — nhánh `feature/member2-informed`
- (a) Tại `# TODO(M2)` thêm hàm `beam_search(problem, h, beam_width)`.
- (b) Đổi `DEFAULT_SEED = 42` thành `DEFAULT_SEED = 2026`.
- (c) Trong `AUTHORS = ["Leader"]` thêm tên mình, ví dụ `["Leader", "Member2"]`.
- (d) Trong `REGISTRY` thêm dòng cuối: `"m2_extra": ("M2 - beam search", demo_informed),` và 1 dòng `CHANGELOG`.

### 👤 Member 3 — nhánh `feature/member3-local-search`
- (a) Tại `# TODO(M3)` thêm hàm `tabu_search(tsp, ...)`.
- (b) Đổi `DEFAULT_MAX_ITER = 1000` thành `DEFAULT_MAX_ITER = 2000`.
- (c) Trong `AUTHORS = ["Leader"]` thêm tên mình, ví dụ `["Leader", "Member3"]`.
- (d) Trong `REGISTRY` thêm dòng cuối: `"m3_extra": ("M3 - tabu search", demo_local),` và 1 dòng `CHANGELOG`.

### 👤 Member 4 — nhánh `feature/member4-adversarial-csp`
- (a) Tại `# TODO(M4)` thêm hàm `min_conflicts(csp, max_steps)` cho CSP.
- (b) Đổi `DEFAULT_MAX_ITER = 1000` thành `DEFAULT_MAX_ITER = 500`.
- (c) Trong `AUTHORS = ["Leader"]` thêm tên mình, ví dụ `["Leader", "Member4"]`.
- (d) Trong `REGISTRY` thêm dòng cuối: `"m4_extra": ("M4 - min conflicts", demo_adversarial_csp),` và 1 dòng `CHANGELOG`.

### Bản đồ conflict (dự kiến)

| Vị trí | Ai đụng vào | Loại |
|---|---|---|
| `DEFAULT_SEED` | M1 vs M2 | cùng 1 dòng, khác giá trị |
| `DEFAULT_MAX_ITER` | M3 vs M4 | cùng 1 dòng, khác giá trị |
| `AUTHORS = [...]` | cả 4 member | cùng 1 dòng |
| cuối `REGISTRY` | cả 4 member | chèn kề nhau |
| cuối `CHANGELOG` | cả 4 member | chèn kề nhau |
| Phần (a) trong vùng riêng | từng người | **không** conflict |

---

## 4. Quy trình cho Member

```bash
# 0. Lần đầu: clone và vào nhánh develop
git clone https://github.com/hungdata/Group2-AI.git
cd Group2-AI
git checkout develop && git pull origin develop

# 1. Tạo nhánh riêng (thay bằng nhánh của mình)
git checkout -b feature/member1-uninformed

# 2. Sửa code trong ai_toolkit/ai_toolkit.py, rồi kiểm tra
python ai_toolkit/ai_toolkit.py --selftest      # phải "0 lỗi"

# 3. Commit (message rõ ràng, mỗi việc 1 commit càng tốt)
git add ai_toolkit/ai_toolkit.py
git commit -m "feat(m1): add bfs_all_shortest_paths and register demo"

# 4. Push nhánh lên GitHub
git push -u origin feature/member1-uninformed

# 5. Lên GitHub tạo Pull Request: feature/member1-... → develop, gán Leader review
```

Lưu ý: **không push thẳng lên `develop`**, **không `git push --force`**.

---

## 5. Quy trình cho Leader (merge + xử lý conflict)

```bash
git checkout develop
git pull origin develop
git fetch origin

# Merge lần lượt từng nhánh (hoặc bấm Merge trên GitHub PR)
git merge --no-ff origin/feature/member1-uninformed   # thường sạch
git merge --no-ff origin/feature/member2-informed      # CONFLICT: DEFAULT_SEED, AUTHORS, REGISTRY, CHANGELOG
```

Khi Git báo `CONFLICT`:

```bash
git status                    # xem file nào "both modified"
code ai_toolkit/ai_toolkit.py # mở file, tìm các dấu <<<<<<< ======= >>>>>>>
```

Mỗi vùng conflict có dạng:

```
<<<<<<< HEAD
DEFAULT_SEED = 7
=======
DEFAULT_SEED = 2026
>>>>>>> origin/feature/member2-informed
```

Cách xử lý (hỏi member liên quan khi cần quyết định):

| Conflict | Cách giải quyết gợi ý |
|---|---|
| `DEFAULT_SEED` | Chọn **một** giá trị (ví dụ `42` quay lại bản gốc), xóa 2 dòng còn lại |
| `DEFAULT_MAX_ITER` | Chọn **một** giá trị thống nhất của nhóm |
| `AUTHORS` | Gộp thành `["Leader", "Member1", "Member2", "Member3", "Member4"]` |
| `REGISTRY` | **Giữ cả hai** — giữ đủ các dòng của mọi member |
| `CHANGELOG` | **Giữ cả hai** — xếp theo thứ tự M1, M2, M3, M4 |

Sau khi sửa tay, **xóa hết dấu `<<<<<<<`, `=======`, `>>>>>>>`**, rồi:

```bash
python ai_toolkit/ai_toolkit.py --selftest     # bắt buộc 0 lỗi
python ai_toolkit/ai_toolkit.py --list         # thấy đủ demo của mọi member
git add ai_toolkit/ai_toolkit.py
git commit                                      # giữ message merge mặc định
git merge --no-ff origin/feature/member3-local-search   # tiếp tục nhánh kế
# ... lặp cho Member 4
git push origin develop
```

Muốn hủy giữa chừng: `git merge --abort`.

---

## 6. Checklist nghiệm thu

- [ ] Có đủ 4 nhánh feature trên GitHub, mỗi nhánh ≥ 1 commit của đúng member
- [ ] 4 Pull Request đã tạo, đã được Leader merge
- [ ] Đã gặp và xử lý ít nhất các conflict ở `DEFAULT_SEED`, `AUTHORS`, `REGISTRY`, `CHANGELOG`
- [ ] `python ai_toolkit.py --selftest` ra `0 lỗi` trên `develop`
- [ ] `python ai_toolkit.py --list` hiện đủ demo gốc + `m1_extra … m4_extra`
- [ ] Không còn dấu conflict `<<<<<<<` trong file

## 7. Quy ước commit

`feat(mX): …` thêm tính năng · `fix(mX): …` sửa lỗi · `docs: …` tài liệu · `merge: …` Leader merge.
