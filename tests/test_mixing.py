import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'code'))
from mixing import proportionate, preferred, two_axis_affinity, diagnostics

q_vectors = [[400, 200, 200, 300], [800, 200, 200, 800], [3, 700, 21, 40]]
groups = [('H','P'),('L','P'),('H','V'),('L','V')]
for q in q_vectors:
    cases = [proportionate(q), preferred(q, 0), preferred(q, .4),
             preferred(q, 1), two_axis_affinity(q, groups, 0, 0),
             two_axis_affinity(q, groups, .8, 1.2),
             two_axis_affinity(q, groups, 2.5, 0.3)]
    for m in cases:
        d = diagnostics(q, m)
        assert d['row_sum_max_error'] < 1e-9, d
        assert d['reciprocity_max_error'] < 1e-7, d
        assert d['nonnegative'], d
    for a,b in zip(proportionate(q),two_axis_affinity(q,groups,0,0)):
        assert max(abs(x-y) for x,y in zip(a,b)) < 1e-9
print('All 21 matrix scenarios passed row-sum, reciprocity, and positivity tests.')
