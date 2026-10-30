"""Mixing Matters: reproducible mixing matrices (no third-party dependencies)."""
import math


def proportionate(q):
    """Return a row-stochastic reciprocal matrix for positive opportunities q."""
    assert q and all(x > 0 for x in q)
    return [[x / sum(q) for x in q] for _ in q]


def preferred(q, epsilon):
    """Standard joint-group preferred mixing for 0 <= epsilon <= 1."""
    assert 0 <= epsilon <= 1
    p = proportionate(q)
    return [[epsilon * (i == j) + (1 - epsilon) * p[i][j]
             for j in range(len(q))] for i in range(len(q))]


def two_axis_affinity(q, groups, theta_r=0.0, theta_m=0.0, tol=1e-12):
    """Symmetrically balance positive edge affinities to group opportunity totals.

    groups: iterable of (activity, typology) pairs, e.g. [('H','P'),...].
    theta values are log-affinities, NOT preferred-mixing epsilon values.
    """
    assert len(q) == len(groups) and all(x > 0 for x in q)
    total = sum(q)
    w = [[q[i] * q[j] / total * math.exp(
        theta_r * (groups[i][0] == groups[j][0]) +
        theta_m * (groups[i][1] == groups[j][1]))
        for j in range(len(q))] for i in range(len(q))]
    a = [1.0] * len(q)
    for _ in range(30000):
        rows = [a[i] * sum(w[i][j] * a[j] for j in range(len(q)))
                for i in range(len(q))]
        if max(abs(rows[i] - q[i]) / q[i] for i in range(len(q))) < tol:
            break
        a = [a[i] * math.sqrt(q[i] / rows[i]) for i in range(len(q))]
    else:
        raise RuntimeError('Balancing did not converge')
    f = [[a[i] * w[i][j] * a[j] for j in range(len(q))]
         for i in range(len(q))]
    return [[f[i][j] / q[i] for j in range(len(q))]
            for i in range(len(q))]


def diagnostics(q, m):
    assert len(q) == len(m) and all(len(row) == len(q) for row in m)
    return {
        'row_sum_max_error': max(abs(sum(row) - 1) for row in m),
        'reciprocity_max_error': max(abs(q[i] * m[i][j] - q[j] * m[j][i])
                                     for i in range(len(q)) for j in range(len(q))),
        'nonnegative': all(x >= 0 for row in m for x in row),
    }


if __name__ == '__main__':
    q = [400, 200, 200, 300]
    groups = [('H', 'P'), ('L', 'P'), ('H', 'V'), ('L', 'V')]
    for name, m in [('proportionate', proportionate(q)),
                    ('preferred', preferred(q, 0.4)),
                    ('two-axis', two_axis_affinity(q, groups, 0.8, 1.2))]:
        print(name, diagnostics(q, m))
        for row in m:
            print(' '.join(f'{x:.3f}' for x in row))
