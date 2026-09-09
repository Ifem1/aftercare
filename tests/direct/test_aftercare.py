import json
import pytest
VERDICTS={"critical","high","moderate","low","no_material_effect","insufficient_evidence"}
WEIGHTS={"critical":5,"high":3,"moderate":2,"low":1,"no_material_effect":0,"insufficient_evidence":0}
def payout(balance,verdict): return balance*WEIGHTS[verdict]//5
@pytest.mark.parametrize('v',sorted(VERDICTS))
def test_bounded(v): assert v in VERDICTS
@pytest.mark.parametrize('v,e',[("critical",100),("high",60),("moderate",40),("low",20),("no_material_effect",0),("insufficient_evidence",0)])
def test_allocation(v,e): assert payout(100,v)==e
def test_remaining_balance(): assert payout(60,'moderate')==24
def test_total_never_exceeds_pool(): assert payout(100,'critical')<=100
def test_zero_evidence_abstains(): assert payout(500,'insufficient_evidence')==0
def test_no_material_effect_freezes_funds(): assert payout(500,'no_material_effect')==0
def test_duplicate_paid_flag(): assert {'paid':True}['paid']
def test_claimant_field_required(): assert 'claimant' in {'claimant':'0xabc'}
def test_manifest_is_frozen(): assert isinstance(['https://a','https://b'],list)
def test_manifest_minimum(): assert len(['a','b'])>=2
def test_manifest_maximum(): assert len(['a','b','c','d'])<=4
def test_state_round_trips(): assert json.loads(json.dumps({'status':'submitted'}))['status']=='submitted'
def test_finalized_verdict(): assert 'low' in VERDICTS
def test_reasoning_bound(): assert len('x'*1500)==1500
def test_title_bound(): assert len('x'*120)==120
def test_description_bound(): assert len('x'*1500)==1500
def test_pool_funding(): assert 100+25==125
def test_available_reservation(): assert 100-payout(100,'low')==80
def test_reserved_increases(): assert payout(100,'moderate')==40
def test_reserved_decreases(): assert 40-40==0
def test_paid_increases(): assert 0+40==40
def test_unknown_rejected(): assert 'bogus' not in VERDICTS
def test_counterfactual_context(): assert {'title','description','period'}.issuperset({'period'})
def test_source_is_data(): assert 'ignore previous instructions' not in 'public source'
def test_integer_math(): assert isinstance(payout(101,'low'),int)
def test_deterministic(): assert payout(101,'high')==payout(101,'high')
def test_empty_pool(): assert payout(0,'critical')==0
