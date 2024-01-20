import numpy as np
import ramda as R
from sklearn.cluster import KMeans, DBSCAN
import fp

_1 = int; _4 = int; N = int; Vec2 = tuple[float, float]

def angle(line: np.ndarray[_1, _4]) -> float:
    """Angle in `[-pi/2, pi/2]`"""
    [[x1, y1, x2, y2]] = line
    dx = x2 - x1
    dy = y2 - y1
    return np.arctan(dy/dx) if dx != 0 else np.pi/2

def midpoint(line: np.ndarray[_1, _4]) -> Vec2:
    [[x1, y1, x2, y2]] = line
    p = np.array([x1, y1])
    q = np.array([x2, y2])
    return (p+q)/2

@R.curry
def yintersect(line: np.ndarray[_1, _4], y: float) -> float:
    """Returns `x` s.t. `(x, y)` belongs to `line`"""
    [[x1, y1, x2, y2]] = line
    p = np.array([x1, y1])
    q = np.array([x2, y2])
    t = q-p
    return p[0] + (y-p[1])*t[0]/t[1]

@R.curry
def xintersect(line: np.ndarray[_1, _4], x: float) -> float:
    """Returns `y` s.t. `(x, y)` belongs to `line`"""
    [[x1, y1, x2, y2]] = line
    p = np.array([x1, y1])
    q = np.array([x2, y2])
    t = q-p
    return p[1] + (x-p[0])*t[1]/t[0]

@R.curry
def hexpand(line: np.ndarray[_1, _4], width: int) -> np.ndarray[_1, _4]:
    y0 = xintersect(line, x=0)
    y1 = xintersect(line, x=width-1)
    return np.array([[0, y0, width-1, y1]])

@R.curry
def vexpand(line: np.ndarray[_1, _4], height: int) -> np.ndarray[_1, _4]:
    x0 = yintersect(line, y=0)
    x1 = yintersect(line, y=height-1)
    return np.array([[x0, 0, x1, height-1]])

def vh_cluster2(
    lines: np.ndarray[N, tuple[_1, _4]],
    eps = np.pi/180, min_samples = 15
) -> tuple[np.ndarray[N, tuple[_1, _4]], np.ndarray[N, tuple[_1, _4]]]:
    """Returns `(vlines, hlines)`"""
    angles = np.array(R.map(angle, lines))
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labs = dbscan.fit_predict(np.abs(angles)[:, None])
    classes, counts = np.unique(labs.clip(0), return_counts=True)
    vh_indices = np.argsort(counts)[-2:]
    vh_classes = classes[vh_indices]
    mean_angles = np.array([
        np.mean(np.abs(angles)[np.where(labs == c)], axis=0)
        for c in vh_classes
    ])
    h_lab = np.argmin(np.abs(mean_angles))
    h_angle = np.abs(np.median(angles[labs == h_lab]))
    v_angle = np.abs(np.median(angles[labs == 1-h_lab]))
    hlines = lines[(labs == h_lab) & np.isclose(np.abs(angles), h_angle, atol=4*np.pi/180)]
    hlines = np.array(sorted(hlines, key=xintersect(x=0)))
    vlines = lines[(labs == 1-h_lab) & np.isclose(np.abs(angles), v_angle, atol=8*np.pi/180)]
    vlines = np.array(sorted(vlines, key=yintersect(y=0)))
    return vlines, hlines

def vh_cluster(
    lines: np.ndarray[N, tuple[_1, _4]]
) -> tuple[np.ndarray[N, tuple[_1, _4]], np.ndarray[N, tuple[_1, _4]]]:
    """Returns `(vlines, hlines)`"""
    angles = np.array(R.map(angle, lines))
    kmeans = KMeans(n_clusters=2, max_iter=5000, n_init=100)
    labs = kmeans.fit_predict(np.abs(angles[:, None]))
    [[alpha], [beta]] = kmeans.cluster_centers_
    h_lab = np.argmin([np.abs(alpha), np.abs(beta)])
    h_angle = np.abs(np.median(angles[labs == h_lab]))
    v_angle = np.abs(np.median(angles[labs == 1-h_lab]))
    hlines = lines[(labs == h_lab) & np.isclose(np.abs(angles), h_angle, atol=4*np.pi/180)]
    hlines = np.array(sorted(hlines, key=xintersect(x=0)))
    vlines = lines[(labs == 1-h_lab) & np.isclose(np.abs(angles), v_angle, atol=8*np.pi/180)]
    vlines = np.array(sorted(vlines, key=yintersect(y=0)))
    return vlines, hlines

N = int; M = int; _1 = int; _4 = int
@R.curry
def cluster(hlines: np.ndarray[N, tuple[_1, _4]], eps = 25, min_samples = 1) -> np.ndarray[M, tuple[_1, _4]]:
    """Cluster lines by midpoint"""
    ps = np.array(R.map(midpoint, hlines))
    labs = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(ps)
    classes = np.unique(labs.clip(0)) # unlabeled are -1
    centers = np.array([
        np.mean(hlines[np.where(labs == c)], axis=0, dtype=np.int32)
        for c in classes
    ])
    return centers

def hcluster(hlines: np.ndarray[N, tuple[_1, _4]], eps = 25, min_samples = 1) -> np.ndarray[M, tuple[_1, _4]]:
    # ys = hlines[:, 0, 1] # each line = [[_, y0, _, _]]
    ys = hlines[:, 0, 1]
    labs = DBSCAN(eps=eps, min_samples=min_samples).fit_predict(ys[:, None])
    classes = np.unique(labs.clip(0)) # unlabeled are -1
    centers = np.array([
        np.mean(hlines[np.where(labs == c)], axis=0, dtype=np.int32)
        for c in classes
    ])
    return centers

def vcluster(vlines: np.ndarray[N, tuple[_1, _4]]) -> np.ndarray[M, tuple[_1, _4]]:
    xs = vlines[:, 0, 0] # each line = [[x0, _, _, _]]
    labs = DBSCAN(eps=10, min_samples=1).fit_predict(xs[:, None])
    classes = np.unique(labs.clip(0)) # unlabeled are -1
    centers = np.array([
        np.mean(vlines[np.where(labs == c)], axis=0, dtype=np.int32)
        for c in classes
    ])
    return centers

def intersect(l1: np.ndarray[_1, _4], l2: np.ndarray[_1, _4]) -> Vec2:
    [[x1, y1, a1, b1]] = l1
    p1 = np.array([x1, y1])
    q1 = np.array([a1, b1])
    [[x2, y2, a2, b2]] = l2
    p2 = np.array([x2, y2])
    q2 = np.array([a2, b2])
    t1 = q1 - p1
    t2 = q2 - p2
    # L1: p1 + alpha*t1 for alpha in [0, 1]
    # L2: p2 + beta*t2  for beta in [0, 1]
    # we solve for alpha and beta s.t. L1 = L2
    # [t1x -t2x] [alpha] = [p2x - p1x]
    # [t1y -t2y] [beta]  = [p2y - p1y]
    A = np.array([t1, -t2]).T
    b = p2 - p1
    result = fp.safe(lambda: np.linalg.solve(A, b))
    match result:
        case None: return None
        case _: ...
    alpha, beta = result
    if 0 <= alpha <= 1 and 0 <= beta <= 1:
        return p1 + alpha*t1

@R.curry
def extend(segment: np.ndarray[_1, _4], px: int) -> np.ndarray[_1, _4]:
    [[x1, y1, x2, y2]] = segment
    p = np.array([x1, y1])
    q = np.array([x2, y2])
    t = q - p
    t = t / np.linalg.norm(t)
    p2 = p - px*t
    q2 = q + px*t
    return np.array([[*p2, *q2]])

def pq(line: np.ndarray[_1, _4]) -> tuple[Vec2, Vec2]:
    """Line endpoints (generally refered to as `p` and `q`)"""
    [[x1, y1, x2, y2]] = line
    return np.array([x1, y1]), np.array([x2, y2])

@R.curry
def pq_sort(line: np.ndarray[_1, _4], axis: int) -> np.ndarray[_1, _4]:
    """Sort line endpoints `(p, q)` by a given `axis` (`0 = x, 1 = y`)"""
    p, q = pq(line)
    return line if p[axis] < q[axis] else np.array([[*q, *p]])

@R.curry
def fill(row: list[np.ndarray[_1, _4]], Xmin: float, Xmax: float) -> list[np.ndarray[_1, _4]]:
    """Extend lines in `row` to fill all `x`s in `[Xmin, Xmax]` exactly once"""
    srow = sorted(row, key=lambda l: l[0][0])
    [l1, *_] = srow
    p1 = [Xmin, xintersect(l1, Xmin)]
    points = [p1]
    
    for l1, l2 in fp.pairwise(srow):
        _, q1 = pq(l1)
        p2, _ = pq(l2)
        if q1[0] < p2[0]: # a) non-overlapping
            points += [q1, p2]
        elif (x := intersect(l1, l2)) is not None:
            points += [x]
        else:
            x1 = [p2[0], xintersect(l1, p2[0])]
            x2 = [q1[0], xintersect(l2, q1[0])]
            points += [x1, x2]
    
    l = srow[-1]
    p = [Xmax, xintersect(l, Xmax)]
    points += [p]
    lines = [
        [[*p, *q]]
        for p, q in fp.pairwise(points)
    ]
    return np.int32(lines)



@R.curry
def fill_old(row: list[np.ndarray[_1, _4]], Xmin: float, Xmax: float) -> list[np.ndarray[_1, _4]]:
    """Extend lines in `row` to fill all `x`s in `[Xmin, Xmax]` exactly once"""
    lines = []
    srow = sorted(row, key=lambda l: l[0][0])
    left = Xmin
    for l1, l2 in fp.pairwise(srow):
        p1, q1 = pq(l1)
        p2, q2 = pq(l2)
        t1 = q1 - p1
        t1 = t1 / np.linalg.norm(t1)
        y1 = xintersect(l1, left)
        pp1 = [left, y1]
        if q1[0] < p2[0]: # not roughly superposed
            d = p2[0] - q1[0]
            qq1 = q1 + t1*d/2
            lines += [[[*pp1, *qq1]]]
            left = qq1[0]+1
        else:
            lines += [[[*pp1, *q1]]]
            left = q1[0]
    
    l = srow[-1]
    y1 = xintersect(l, left)
    y2 = xintersect(l, Xmax)
    lines += [[[left, y1, Xmax, y2]]]
    return lines