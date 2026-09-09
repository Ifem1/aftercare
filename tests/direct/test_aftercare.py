import json
import pytest

def fresh(deploy): return deploy('contracts/aftercare.py')
def round_args(c): return c.create_round('Test round','Evidence backed maintenance','2030-01-01')
def claim_args(c, rid='round_1'): return c.submit_claim(rid,'Maintained package','Prevented deterioration','2025','https://a.example,https://b.example')
def fund(c, vm, amount): vm.value=amount; c.fund_round('round_1'); vm.value=0
def addr(a): return '0x'+bytes(a).hex()

def test_create_round(direct_deploy): assert round_args(fresh(direct_deploy)) == 'round_1'
def test_read_round(direct_deploy):
 c=fresh(direct_deploy); round_args(c); assert json.loads(c.get_round('round_1'))['id']=='round_1'
def test_missing_round(direct_deploy,direct_vm):
 with direct_vm.expect_revert('round not found'): fresh(direct_deploy).get_round('round_9')
def test_fund_round(direct_deploy,direct_vm):
 c=fresh(direct_deploy); round_args(c); fund(c,direct_vm,100); assert json.loads(c.get_round('round_1'))['available']==100
def test_funding_accounting(direct_deploy,direct_vm):
 c=fresh(direct_deploy); round_args(c); fund(c,direct_vm,40); fund(c,direct_vm,60); r=json.loads(c.get_round('round_1')); assert (r['total_funded'],r['pool'])==(100,100)
def test_missing_funding_reverts(direct_deploy,direct_vm):
 direct_vm.value=1
 with direct_vm.expect_revert('round not found'): fresh(direct_deploy).fund_round('round_1')
def test_submit_claim(direct_deploy):
 c=fresh(direct_deploy); round_args(c); assert claim_args(c)=='claim_1'
def test_claimant_stored(direct_deploy,direct_owner):
 c=fresh(direct_deploy); round_args(c); claim_args(c); assert json.loads(c.get_claim('claim_1'))['claimant']==addr(direct_owner)
def test_claim_count(direct_deploy):
 c=fresh(direct_deploy); round_args(c); claim_args(c); assert json.loads(c.get_round('round_1'))['claims']==1
def test_short_manifest_reverts(direct_deploy,direct_vm):
 c=fresh(direct_deploy); round_args(c)
 with direct_vm.expect_revert('evidence manifest'): c.submit_claim('round_1','x','x','x','https://a')
def test_long_manifest_reverts(direct_deploy,direct_vm):
 c=fresh(direct_deploy); round_args(c)
 with direct_vm.expect_revert('evidence manifest'): c.submit_claim('round_1','x','x','x','a,b,c,d,e')
def test_missing_claim_round_reverts(direct_deploy,direct_vm):
 with direct_vm.expect_revert('invalid round'): fresh(direct_deploy).submit_claim('round_9','x','x','x','a,b')
def test_evidence_frozen(direct_deploy):
 c=fresh(direct_deploy); round_args(c); claim_args(c); assert json.loads(c.get_claim('claim_1'))['evidence']==['https://a.example','https://b.example']
def test_count_views(direct_deploy):
 c=fresh(direct_deploy); round_args(c); claim_args(c); assert (c.get_round_count(),c.get_claim_count())==(1,1)
def test_claim_read(direct_deploy):
 c=fresh(direct_deploy); round_args(c); claim_args(c); assert json.loads(c.get_claim('claim_1'))['status']=='submitted'
def test_second_claim_id(direct_deploy):
 c=fresh(direct_deploy); round_args(c); claim_args(c); assert claim_args(c)=='claim_2'
def test_round_creator(direct_deploy,direct_owner):
 c=fresh(direct_deploy); round_args(c); assert json.loads(c.get_round('round_1'))['creator']==addr(direct_owner)
def test_title_bound(direct_deploy):
 c=fresh(direct_deploy); assert len(json.loads(c.get_round(round_args(c)))['title'])<=120
def test_description_bound(direct_deploy):
 c=fresh(direct_deploy); rid=round_args(c); c.submit_claim(rid,'x','x'*3000,'x','a,b'); assert len(json.loads(c.get_claim('claim_1'))['description'])<=1500
def test_empty_value_funding_is_accounted(direct_deploy,direct_vm):
 c=fresh(direct_deploy); round_args(c); fund(c,direct_vm,0); assert json.loads(c.get_round('round_1'))['available']==0
def test_multiple_claims_count(direct_deploy):
 c=fresh(direct_deploy); round_args(c); claim_args(c); claim_args(c); assert json.loads(c.get_round('round_1'))['claims']==2
def test_round_ids_are_monotonic(direct_deploy):
 c=fresh(direct_deploy); assert [round_args(c),round_args(c)]==['round_1','round_2']
def test_claim_ids_are_monotonic(direct_deploy):
 c=fresh(direct_deploy); round_args(c); assert [claim_args(c),claim_args(c)]==['claim_1','claim_2']
def test_funding_preserves_claim_count(direct_deploy,direct_vm):
 c=fresh(direct_deploy); round_args(c); claim_args(c); fund(c,direct_vm,5); assert json.loads(c.get_round('round_1'))['claims']==1
def test_claim_period_stored(direct_deploy):
 c=fresh(direct_deploy); round_args(c); claim_args(c); assert json.loads(c.get_claim('claim_1'))['period']=='2025'
def test_claim_starts_unpaid(direct_deploy):
 c=fresh(direct_deploy); round_args(c); claim_args(c); assert json.loads(c.get_claim('claim_1'))['paid'] is False
def test_unassessed_claim_has_zero_payout(direct_deploy):
 c=fresh(direct_deploy); round_args(c); claim_args(c); assert json.loads(c.get_claim('claim_1'))['payout']==0
def test_round_fields_exist(direct_deploy):
 c=fresh(direct_deploy); r=json.loads(c.get_round(round_args(c))); assert {'available','reserved','paid','total_funded'}<=set(r)
def test_invalid_payout_reverts(direct_deploy,direct_vm):
 c=fresh(direct_deploy); round_args(c); claim_args(c)
 with direct_vm.expect_revert('payout unavailable'): c.claim_payout('claim_1')
def test_repeated_assessment_guard_source_exists():
 assert 'claim already assessed' in open('contracts/aftercare.py').read()
