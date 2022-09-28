#!/bin/bash
#SBATCH --mem=48G
#SBATCH --export=ALL
#SBATCH --cpus-per-task=24
#SBATCH --time=0:30:00
#SBATCH --job-name=polyglot-eval
#SBATCH --partition=express
#SBATCH --exclusive
source ~/.bashrc
source ~a.guha/bin/activate_conda
set -e
module load R gcc/9.2.0
conda activate polyglot
PATH=/home/a.guha/scala/bin:/work/arjunguha-research-group/software/bin:$PATH
eval `/home/a.guha/repos/spack/bin/spack load --sh dmd`
LIST_FILES=files.txt
# Go seems to happily cache everything it ever builds in here, and not
# in object files in the same directory. How clean! But we will run out
# of quota without this.
GOCACHE=/tmp/arjunguha_research_group_go_cache 

if [ $# -eq 1 ]; then
  LIST_FILES=$1
fi

LUA_PATH="${PWD}/luaunit.lua"
echo "$LIST_FILES[$SLURM_ARRAY_TASK_ID]"
hostname
lscpu | sed -nr '/Model name/ s/.*:\s*(.*) @ .*/\1/p'

python3 problem_evaluator.py --job-file $LIST_FILES --job-file-line $SLURM_ARRAY_TASK_ID --max-workers 23

