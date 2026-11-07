SMCEP v1.0 synthetic multi-generation experiment

Run from the same extracted project tree as smcep_v09:
  python smcep_v10/smcep_v10.py --seeds 12 --generations 25 --candidates 6 --probes 12 --out smcep_v10

The Python script imports the synthetic landscape and probe functions from smcep_v09/smcep_v09.py; both folders are included in the ZIP. The code is not a simulation of a real autonomous AI research agent. The LaTeX document includes author-year citations via \cite and a reference list. No claims of experimental validation of TMGA are made.

The frozen arm can edit task parameters but not proposal-policy parameters. The evolving arm can edit both. Their policy capacity is evaluated against a fixed reference agent on ID/OOD synthetic task families. Frozen-arm C is therefore constant by design. This is a deliberately narrow test and should not be used to infer general impossibility of recursive self-improvement.
