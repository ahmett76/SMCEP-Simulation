"""SMCEP v0.9: synthetic paired-branch generalization pilot, not evidence of real RSI."""
import argparse,csv,json
from pathlib import Path
import numpy as np

GROUPS={'A':('none',False,.015),'B':('restricted',False,.015),'C':('broad',True,.015),'D':('broad',True,.12),'E_scope':('broad',False,.015),'E_policy':('restricted',True,.015)}
REF=np.array([-.65,.45,-.35,.25]);INIT=np.r_[REF,np.log(.35),0.]

def tasks(seed,family,n,ood=False):
    rng=np.random.default_rng(np.random.SeedSequence([seed,family,743]))
    if ood: # OOD family, shifted target support and altered frequency
        targets=rng.uniform(-1.65,.35,(n,4));freq=7.7
    else:
        targets=rng.uniform(-1,1,(n,4));freq=5.1
    weights=rng.uniform(.6,1.4,(n,4));phase=rng.uniform(-np.pi,np.pi,(n,4))
    return targets,weights,phase,freq

def score(theta,ts):
    target,w,phase,freq=ts;theta=np.atleast_2d(theta)
    fit=-np.mean(w[None,:,:]*(theta[:,None,:]-target[None,:,:])**2,axis=2)
    rugged=.20*np.mean(np.sin(freq*theta[:,None,:]+phase[None,:,:]),axis=2)
    return (1/(1+np.exp(-2*(fit+rugged+.65)))).mean(axis=1)

def propose(agent,seed,tag,k,scope,policy):
    if scope=='none':return np.empty((0,6))
    rng=np.random.default_rng(np.random.SeedSequence([seed,tag,991]))
    delta=rng.normal(size=(k,4))+agent[5]
    if scope=='restricted':delta[:,2:]=0
    theta=np.clip(agent[:4]+np.exp(agent[4])*delta,-2,2)
    steps=np.full(k,agent[4]);bias=np.full(k,agent[5])
    if policy:
        steps=np.clip(steps+rng.normal(0,.18,k),np.log(.04),np.log(1.2))
        bias=np.clip(bias+rng.normal(0,.12,k),-1.2,1.2)
    return np.column_stack((theta,steps,bias))

def probe(agent,seed,family,k,nprobe):
    """Independent policy skill: generate proposals for a fixed REF on tasks from family;
    select on a development split and measure gain on a disjoint audit split.
    No probe-generated agent updates the main trajectory.
    """
    gains=[];invalid=0
    developer=np.r_[REF,agent[4:6]]
    for j in range(nprobe):
        candidates=propose(developer,seed,family*10+1000+j,k,'broad',False)
        development=tasks(seed,family*10+2000+j,16,ood=(family>=300000))
        audit=tasks(seed,family*10+5000+j,24,ood=(family>=300000))
        ix=int(np.argmax(score(candidates[:,:4],development)))
        gains.append(float(score(candidates[ix,:4],audit)[0]-score(REF,audit)[0]))
    return float(np.mean(gains))

def run(seed,group,T,k,nprobe,policy_weight):
    scope,policy,noise=GROUPS[group];agent=INIT.copy();rows=[]
    held=tasks(seed,110000,64)
    for gen in range(T+1):
        P=float(score(agent[:4],held)[0]);c_id=probe(agent,seed,120000,k,nprobe);c_ood=probe(agent,seed,310000,k,nprobe)
        row=dict(seed=seed,group=group,generation=gen,P=P,C_id=c_id,C_ood=c_ood,accepted=0,false_accept=0,F_id=0.,F_ood=0.,selection_gain=0.,audit_gain=0.)
        if gen<T:
            candidates=propose(agent,seed,10000+gen,k,scope,policy)
            if len(candidates):
                selection=tasks(seed,130000+gen,32)
                base=float(score(agent[:4],selection)[0]);task_gain=score(candidates[:,:4],selection)-base
                # Policy selection uses separate visible development family, never audit families.
                p_base=probe(agent,seed,140000+gen*100,k,max(4,nprobe//3))
                p_candidates=np.array([probe(c,seed,140000+gen*100,k,max(4,nprobe//3)) for c in candidates])
                utility=task_gain+policy_weight*(p_candidates-p_base)
                rng=np.random.default_rng(np.random.SeedSequence([seed,gen,505]))
                observed=utility+rng.normal(0,noise,len(candidates))
                ix=int(np.argmax(observed))
                if observed[ix]>0:
                    new=candidates[ix]
                    # Matched counterfactual: same baseline, same probe tasks, only selected change differs.
                    new_id=probe(new,seed,120000,k,nprobe);new_ood=probe(new,seed,310000,k,nprobe)
                    row.update(accepted=1,false_accept=int(utility[ix]<=0),F_id=new_id-c_id,F_ood=new_ood-c_ood,selection_gain=float(utility[ix]),audit_gain=float(score(new[:4],held)[0]-P))
                    agent=new
        rows.append(row)
    return rows

def mean_sd(values):
    a=np.asarray(values,dtype=float)
    return dict(mean=float(a.mean()),sd=float(a.std(ddof=1)) if len(a)>1 else None,ci95_low=float(a.mean()-1.96*a.std(ddof=1)/np.sqrt(len(a))) if len(a)>1 else None,ci95_high=float(a.mean()+1.96*a.std(ddof=1)/np.sqrt(len(a))) if len(a)>1 else None)

def summarize(rows,seeds,T):
    summaries=[];pairs=[]
    lookup={(r['seed'],r['group'],r['generation']):r for r in rows}
    for group in GROUPS:
        changes={m:[lookup[(s,group,T)][m]-lookup[(s,group,0)][m] for s in range(seeds)] for m in ('P','C_id','C_ood')}
        transitions=[lookup[(s,group,t)] for s in range(seeds) for t in range(T)]
        accepted=[r for r in transitions if r['accepted']]
        summaries.append(dict(group=group,**{'delta_'+m:mean_sd(v) for m,v in changes.items()},accept_rate=len(accepted)/len(transitions),false_accept_given_accept=sum(r['false_accept'] for r in accepted)/len(accepted) if accepted else None,mean_F_id_on_accept=float(np.mean([r['F_id'] for r in accepted])) if accepted else None,mean_F_ood_on_accept=float(np.mean([r['F_ood'] for r in accepted])) if accepted else None))
    for g1,g0 in [('D','C'),('C','B'),('C','E_scope'),('C','E_policy')]:
        for m in ('P','C_id','C_ood'):
            pairs.append(dict(comparison=g1+'-'+g0,metric=m,**mean_sd([lookup[(s,g1,T)][m]-lookup[(s,g0,T)][m] for s in range(seeds)])))
    return summaries,pairs

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--seeds',type=int,default=12);ap.add_argument('--generations',type=int,default=25);ap.add_argument('--candidates',type=int,default=6);ap.add_argument('--probes',type=int,default=12);ap.add_argument('--policy-weight',type=float,default=1.0);ap.add_argument('--out',default='/mnt/data/smcep_v09');a=ap.parse_args()
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    rows=[r for s in range(a.seeds) for g in GROUPS for r in run(s,g,a.generations,a.candidates,a.probes,a.policy_weight)]
    with (out/'trajectories.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summaries,pairs=summarize(rows,a.seeds,a.generations)
    data=dict(parameters=vars(a),groups=GROUPS,summary=summaries,paired=pairs,limitations=['Synthetic toy agents, not real autonomous research agents','ID and OOD probes are disjoint from selection, but generated by a researcher-defined synthetic task model','Anchor-based C evaluates policy search skill, not universal future development capability','C and D selection-noise contrast is controlled; C versus B changes both scope and policy','Per-step F is matched branch effect on probe, not a causal estimate of sustained multi-generation recursion','Exploratory pilot: confidence intervals are descriptive and not multiplicity-adjusted'])
    (out/'summary.json').write_text(json.dumps(data,indent=2,ensure_ascii=False));print(json.dumps(summaries,indent=2))
if __name__=='__main__':main()
