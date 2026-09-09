# { "Depends": "genlayer:latest" }
import gl
from dataclasses import dataclass

@dataclass
class Claim:
    claimant: str
    title: str
    description: str
    period: str
    evidence: list[str]
    status: str
    verdict: str
    reasoning: str
    payout: int
    claimed: bool

class Aftercare:
    def __init__(self):
        self.round_count = 0
        self.claim_count = 0
        self.rounds = {}
        self.claims = {}

    @gl.public.write
    def create_round(self, title: str, description: str, closes_at: str) -> int:
        self.round_count += 1
        self.rounds[self.round_count] = {"title": title[:120], "description": description[:500], "closes_at": closes_at[:40], "pool": 0, "claims": 0, "status": "open"}
        return self.round_count

    @gl.public.write.payable
    def fund_round(self, round_id: int):
        if round_id not in self.rounds:
            raise gl.vm.UserError("round not found")
        self.rounds[round_id]["pool"] += int(gl.message.value)

    @gl.public.write
    def submit_claim(self, round_id: int, title: str, description: str, period: str, evidence: list[str]) -> int:
        if round_id not in self.rounds or len(evidence) < 2 or len(evidence) > 4:
            raise gl.vm.UserError("invalid round or evidence manifest")
        self.claim_count += 1
        self.rounds[round_id]["claims"] += 1
        self.claims[self.claim_count] = Claim(str(gl.message.sender_address), title[:120], description[:1000], period[:80], evidence, "submitted", "", "", 0, False)
        return self.claim_count

    @gl.public.write
    def assess_claim(self, claim_id: int):
        if claim_id not in self.claims or self.claims[claim_id].status in ("assessing", "finalized"):
            raise gl.vm.UserError("claim unavailable")
        claim = self.claims[claim_id]
        urls = list(claim.evidence)
        def leader():
            evidence_text = []
            for url in urls:
                evidence_text.append(gl.nondet.web.get(url)[:4000])
            return gl.eq_principle.prompt_comparative(
                lambda: gl.nondet.exec_prompt("Evaluate only the retrieved public evidence. Return JSON with verdict, reasoning. Verdict must be critical, high, moderate, low, no_material_effect, or insufficient_evidence. Abstain when evidence is unavailable or contradictory. Do not choose a payout." + "\n\n".join(evidence_text)),
                "Compare validators' semantic conclusions about intervention, relevance, deterioration risk, counterfactual, alternatives, and attribution. Exact wording may differ; the verdict category and evidence-grounded conclusion must agree."
            )
        result = leader()
        verdict = result.get("verdict", "insufficient_evidence")
        allowed = {"critical": 5, "high": 3, "moderate": 2, "low": 1, "no_material_effect": 0, "insufficient_evidence": 0}
        if verdict not in allowed:
            verdict = "insufficient_evidence"
        claim.status = "finalized"
        claim.verdict = verdict
        claim.reasoning = str(result.get("reasoning", "Consensus returned a bounded verdict."))[:1000]
        claim.payout = 0

    @gl.public.write
    def claim_payout(self, claim_id: int):
        if claim_id not in self.claims or self.claims[claim_id].claimed or self.claims[claim_id].payout <= 0:
            raise gl.vm.UserError("payout unavailable")
        self.claims[claim_id].claimed = True
