# Commands actually attempted; output paths already contain evidence.
# From /workspace/scratch/82ba53fe7aca/yang_mills_workbench; PYTHONDONTWRITEBYTECODE=1 was applied to all Python subprocesses.

# Exit 1
python3 -B research/round19/reproduce.py --through c2 --output /workspace/scratch/82ba53fe7aca/skill-check-round21/original-reproduction

# Exit 0
python3 -B research/round19/backward/c2/check.py --output /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-backward

# Exit 0
python3 -B -O research/round19/backward/c2/check.py --output /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-backward-optimized

# Exit 0
python3 -B research/round19/backward/c2/compare.py --producer research/round19/forward/c2/check.py --evidence /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-forward --output /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-comparison

# Exit 0
python3 -B -O research/round19/backward/c2/compare.py --producer research/round19/forward/c2/check.py --evidence /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-forward-optimized --output /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-comparison-optimized

# Exit 0
python3 -B research/round19/forward/c2/check.py --output /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-forward

# Exit 0
python3 -B -O research/round19/forward/c2/check.py --output /workspace/scratch/82ba53fe7aca/skill-check-round21/direct-forward-optimized

# Exit 0
python3 -B /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree/research/round19/backward/c2/compare.py --producer /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree/research/round19/forward/c2/check.py --evidence /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree-forward --output /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree-comparison

# Exit 0
python3 -B /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree/research/round19/forward/c2/check.py --output /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree-forward

# Exit 1
python3 -B /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree/research/round19/reproduce.py --from-loop c2 --through c2 --output /workspace/scratch/82ba53fe7aca/skill-check-round21/git-tree-reproduction
