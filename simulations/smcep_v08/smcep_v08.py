"""SMCEP v0.8: anchored synthetic policy-capacity pilot. Not evidence of real-world RSI."""
import argparse,csv,json
from pathlib import Path
import numpy as np

GROUPS={
 'A':dict(scope='none',policy=False,noise=0.015),
 'B':dict(scope='restricted',policy=False,noise=0.015),
 'C':dict(scope='broad',policy=True,noise=0.015),
 'D':dict(scope='broad',policy=True,noise=0.12),
 'E_scope':dict(scope='broad',policy=False,noise=0.015),
 'E_policy':dict(scope='restricted',policy=True,noise=0.015),
}
REFERENCE=np.array([-.65,.45,-.35,.25])
INIT=np.r_[REFERENCE,np.log(.35),0.]

def task(seed,tag,n):
 rng=np.random.default_rng(np.random.SeedSequence([seed,tag,714]))
 return rng.uniform(-1,1,(n,4)),rng.uniform(.6,1.4,(n,4)),rng.uniform(-3.14,3.14,(n,4))

def score(theta,taskset):
 target,w,phase=taskset;theta=np.atleast_2d(theta)
 fit=-np.mean(w[None,:,:]*(theta[:,None,:]-target[None,:,:])**2,axis=2)
 rugged=.20*np.mean(np.sin(5.1*theta[:,None,:]+phase[None,:,:]),axis=2)
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

def anchored_probe(agent,seed,tag,k,nprobe,scope='broad'):
 """All developers start from same REFERENCE theta; only policy params vary.
    Evaluates fixed task families with common random numbers, independently of selection.
    Returns best-of-k opportunity and mean raw proposal gain (both relative to reference).
 """
 gains=[];raw=[]
 for j in range(nprobe):
  t=task(seed,tag+j,10)
  base=float(score(REFERENCE,t)[0])
  developer=np.r_[REFERENCE,agent[4:6]]
  cand=propose(developer,seed,tag+50000+j,k,scope,False)
  vals=score(cand[:,:4],t)-base
  gains.append(max(0.,float(vals.max())))
  raw.append(float(vals.mean()))
 return float(np.mean(gains)),float(np.mean(raw))

def run(seed,group,T,k,nprobe,policy_weight):
 cfg=GROUPS[group];agent=INIT.copy();out=[]
 held=task(seed,10,64)
 for gen in range(T+1):
  P=float(score(agent[:4],held)[0]); C,raw=anchored_probe(agent,seed,1000,k,nprobe)
  row=dict(seed=seed,group=group,generation=gen,P=P,C_anchor=C,proposal_raw=raw,accepted=0,false_accept=0,F_anchor=0.,selection_gain=0.,audit_gain=0.)
  if gen<T:
   cand=propose(agent,seed,10000+gen,k,cfg['scope'],cfg['policy'])
   if len(cand):
    selection=task(seed,3000+gen,32)
    base=float(score(agent[:4],selection)[0]);true=score(cand[:,:4],selection)-base
    # Development-policy selection test uses separate fixed reference tasks;
    # neither held-out task performance nor anchored C test is visible here.
    policy_dev=np.array([anchored_probe(x,seed,7000+gen*100,k,max(4,nprobe//2))[0] for x in cand])
    base_policy=anchored_probe(agent,seed,7000+gen*100,k,max(4,nprobe//2))[0]
    true_util=true+policy_weight*(policy_dev-base_policy)
    rng=np.random.default_rng(np.random.SeedSequence([seed,gen,505]))
    observed=true_util+rng.normal(0,cfg['noise'],len(cand))
    idx=int(np.argmax(observed))
    if observed[idx]>0:
     new=cand[idx];newC,_=anchored_probe(new,seed,1000,k,nprobe)
     row.update(accepted=1,false_accept=int(true_util[idx]<=0),F_anchor=float(newC-C),selection_gain=float(true_util[idx]),audit_gain=float(score(new[:4],held)[0]-P))
     agent=new
  out.append(row)
 return out

def summarize(rows,T,seeds):
 summary=[]
 for g in GROUPS:
  gr=[r for r in rows if r['group']==g]
  initial={r['seed']:r for r in gr if r['generation']==0}
  final={r['seed']:r for r in gr if r['generation']==T}
  dp=np.array([final[s]['P']-initial[s]['P'] for s in range(seeds)])
  dc=np.array([final[s]['C_anchor']-initial[s]['C_anchor'] for s in range(seeds)])
  trans=[r for r in gr if r['generation']<T];acc=[r for r in trans if r['accepted']]
  summary.append(dict(group=g,delta_P=float(dp.mean()),delta_C_anchor=float(dc.mean()),sd_P=float(dp.std(ddof=1)) if seeds>1 else None,sd_C=float(dc.std(ddof=1)) if seeds>1 else None,accept_rate=len(acc)/len(trans),false_accept_given_accept=sum(r['false_accept'] for r in acc)/len(acc) if acc else None,mean_F_on_accept=float(np.mean([r['F_anchor'] for r in acc])) if acc else None))
 paired=[]
 for a,b in [('D','C'),('C','B'),('C','E_scope'),('C','E_policy')]:
  for metric in ('P','C_anchor'):
   diffs=np.array([next(r[metric] for r in rows if r['group']==a and r['seed']==s and r['generation']==T)-next(r[metric] for r in rows if r['group']==b and r['seed']==s and r['generation']==T) for s in range(seeds)])
   paired.append(dict(comparison=f'{a}-{b}',metric=metric,mean=float(diffs.mean()),sd=float(diffs.std(ddof=1)) if seeds>1 else None))
 return summary,paired

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--seeds',type=int,default=12);ap.add_argument('--generations',type=int,default=25);ap.add_argument('--candidates',type=int,default=6);ap.add_argument('--probes',type=int,default=16);ap.add_argument('--policy-weight',type=float,default=1.0);ap.add_argument('--out',default='/mnt/data/smcep_v08')
 a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 rows=[r for seed in range(a.seeds) for g in GROUPS for r in run(seed,g,a.generations,a.candidates,a.probes,a.policy_weight)]
 with (out/'trajectories.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary,paired=summarize(rows,a.generations,a.seeds)
 result=dict(parameters=vars(a),groups=GROUPS,summary=summary,paired=paired,limitations=['Anchored C measures synthetic proposal-search opportunity, not actual independent AI research success','Policy development selection is explicitly optimized; improvement can arise by construction of the search/selection task, not guaranteed by equations','Common reference removes changing baseline headroom but does not remove task-distribution dependence','Synthetic environment only; descriptive pilot; no preregistered confirmatory inference','F_anchor is a local branch contrast, not proof of persistent recursion','D and C differ by evaluator noise; A/B/C scope-policy comparisons require ablations'])
 (out/'summary.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(dict(summary=summary,paired=paired),indent=2))
if __name__=='__main__':main()
