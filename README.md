# SmartAging Full-Loop Synthetic Demo Dataset

100 synthetic participants, six visits (Baseline, M1, M3, M6, M9, M12), four domains.

This version adds:
- transparent demo issue scores per domain;
- explicit product-design weights;
- overall demo prioritization flag;
- top two issues;
- simple action recommendations;
- follow-up/re-measure instruction;
- simulated Month 6 action-plan marker for the Intervention Response group.

**Critical limitation:** all trajectories, scores, weights and post-action improvements are synthetic demonstration constructs. They are not validated clinical thresholds, risk scores, treatment effects, or evidence that AI improves outcomes.

The intended MVP loop is:
MEASURE -> DETECT -> PRIORITIZE -> RECOMMEND -> RE-MEASURE -> ASSESS RESPONSE.
