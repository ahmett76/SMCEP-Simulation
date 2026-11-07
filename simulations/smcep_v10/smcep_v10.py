"""SMCEP v1.0 synthetic multi-generation policy-edit experiment; exploratory only.
Compare broad task-parameter edits with policy frozen versus policy mutable.
No claim of actual autonomous RSI or general causal identification.
"""
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'smcep_v09'))
from smcep_v09 import INIT,tasks,score,propose,probe,mean_sd
ARMS=('frozen','evolving')

def run(seed,arm,T,k,nprobe,policy_weight,noise):
    agent=INIT.copy(); rows=[]; held=tasks(seed,110000,64)
    for t in range(T+1):
        p=float(score(agent[:4],held)[0]); cid=probe(agent,seed,120000,k,nprobe); cood=probe(agent,seed,310000,k,nprobe)
        row=dict(seed=seed,arm=arm,generation=t,P=p,C_id=cid,C_ood=cood,accepted=0,false_accept=0,F_id=0.,F_ood=0.,policy_change=0.,task_gain=0.)
        if t<T:
            # Identical generation of candidate randomness across arms, conditioned on their agent state.
            candidates=propose(agent,seed,10000+t,k,'broad',arm=='evolving')
            sel=tasks(seed,130000+t,32)
            task_gain=score(candidates[:,:4],sel)-float(score(agent[:4],sel)[0])
            p_base=probe(agent,seed,140000+t*100,k,max(4,nprobe//3))
            p_candidate=np.array([probe(c,seed,140000+t*100,k,max(4,nprobe//3)) for c in candidates])
            utility=task_gain+policy_weight*(p_candidate-p_base)
            rng=np.random.default_rng(np.random.SeedSequence([seed,t,505]))
            observed=utility+rng.normal(0,noise,len(candidates))
            idx=int(np.argmax(observed))
            if observed[idx]>0:
                nxt=candidates[idx]
                row.update(accepted=1,false_accept=int(utility[idx]<=0),F_id=probe(nxt,seed,120000,k,nprobe)-cid,F_ood=probe(nxt,seed,310000,k,nprobe)-cood,policy_change=float(np.linalg.norm(nxt[4:]-agent[4:])),task_gain=float(task_gain[idx]))
                agent=nxt
        rows.append(row)
    return rows

def summarize(rows,seeds,T):
    lookup={(r['seed'],r['arm'],r['generation']):r for r in rows}
    out=[];pairs=[]
    for arm in ARMS:
        transitions=[lookup[(s,arm,t)] for s in range(seeds) for t in range(T)]
        accepted=[r for r in transitions if r['accepted']]
        out.append(dict(arm=arm,delta={m:mean_sd([lookup[(s,arm,T)][m]-lookup[(s,arm,0)][m] for s in range(seeds)]) for m in ('P','C_id','C_ood')},accept_rate=len(accepted)/len(transitions),false_accept_given_accept=sum(r['false_accept'] for r in accepted)/len(accepted) if accepted else None,mean_F_id_on_accept=float(np.mean([r['F_id'] for r in accepted])) if accepted else None,mean_F_ood_on_accept=float(np.mean([r['F_ood'] for r in accepted])) if accepted else None))
    for m in ('P','C_id','C_ood'):
        diffs=[(lookup[(s,'evolving',T)][m]-lookup[(s,'evolving',0)][m])-(lookup[(s,'frozen',T)][m]-lookup[(s,'frozen',0)][m]) for s in range(seeds)]
        pairs.append(dict(metric=m,contrast='evolving_minus_frozen',**mean_sd(diffs),per_seed=diffs))
    return out,pairs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',type=int,default=12);ap.add_argument('--generations',type=int,default=25);ap.add_argument('--candidates',type=int,default=6);ap.add_argument('--probes',type=int,default=12);ap.add_argument('--policy-weight',type=float,default=1.);ap.add_argument('--noise',type=float,default=.015);ap.add_argument('--out',default='/mnt/data/smcep_v10');a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    rows=[r for s in range(a.seeds) for arm in ARMS for r in run(s,arm,a.generations,a.candidates,a.probes,a.policy_weight,a.noise)]
    with (out/'trajectories.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    summaries,pairs=summarize(rows,a.seeds,a.generations)
    obj=dict(parameters=vars(a),summary=summaries,paired=pairs,limitations=['Researcher-designed synthetic landscape, not real autonomous agent RSI','Policy mutability contrast includes altered candidate space, not isolation of an intrinsic abstract capability','Policy meta-capacity evaluated on fixed reference tasks; not an unrestricted future-research capability','Paired seeds reduce noise but are not independent real-world interventions','Confidence intervals are descriptive, normal approximation, no preregistration or multiplicity correction','Held-out task families are synthetic and share the same landscape generator'])
    (out/'summary.json').write_text(json.dumps(obj,indent=2,ensure_ascii=False));print(json.dumps(dict(summary=summaries,paired=[{k:v for k,v in p.items() if k!='per_seed'} for p in pairs]),indent=2))
if __name__=='__main__':main()
