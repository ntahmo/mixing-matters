"""Edge cases and explicit demonstrations of the broken naive formula."""
from pathlib import Path
import sys,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from mixing import proportionate,preferred,two_axis_affinity,diagnostics
random.seed(20261029)
groups=[('H','P'),('L','P'),('H','V'),('L','V')]
for _ in range(70):
 q=[random.uniform(3,600) for i in range(4)]
 for m in (proportionate(q),preferred(q,random.uniform(0,1)),two_axis_affinity(q,groups,random.uniform(0,2.8),random.uniform(0,2.8))):
  d=diagnostics(q,m)
  assert d['row_sum_max_error']<1e-9,d
  assert d['reciprocity_max_error']<1e-7,d
  assert d['nonnegative'],d
# Correlated four-group margins break the naive independent-marginal baseline.
q=[400,200,200,300];t=sum(q)
q_h=q[0]+q[2];q_p=q[0]+q[1]
assert abs(q[0]/t-(q_h/t)*(q_p/t))>.05
# When the two characteristics are associated, multiplying marginal preference kernels can fail reciprocity.
q=[400,200,200,300];t=sum(q);e=.5
activity=['H','L','H','L'];typology=['P','P','V','V']
qa={'H':600,'L':500};qm={'P':600,'V':500}
naive=[[ (e*int(activity[i]==activity[j])+(1-e)*qa[activity[j]]/t)*
 (e*int(typology[i]==typology[j])+(1-e)*qm[typology[j]]/t)
 for j in range(4)] for i in range(4)]
assert diagnostics(q,naive)['reciprocity_max_error']>1
print('PASS: 210 randomized valid matrices and two intentionally invalid constructions distinguished.')
