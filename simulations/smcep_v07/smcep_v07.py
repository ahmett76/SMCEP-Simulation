"""SMCEP v0.7 synthetic agent experiment. Mechanism demonstration, not empirical AI evidence."""
import argparse, csv, json
from pathlib import Path
import numpy as np

GROUPS={
 'A':dict(scope='none',noise=0.015,policy=False),
 'B':dict(scope='restricted',noise=0.015,policy=False),
 'C':dict(scope='broad',noise=0.015,policy=True),
 'D':dict(scope='broad',noise=0.12,policy=True),
 'E_scope':dict(scope='broad',noise=0.015,policy=False),
 'E_policy':dict(scope='restricted',noise=0.015,policy=True),
}

def tasks(seed, tag, n):
 r=np.random.default_rng(np.random.SeedSequence([seed,tag,714]))
 return r.uniform(-1,1,(n,4)),r.uniform(.6,1.4,(n,4)),r.uniform(-3.14,3.14,(n,4))

def scores(theta,task):
 targets,w,phase=task
 theta=np.asarray(theta)
 fit=-np.mean(w[None,:,:]*(theta[:,None,:]-targets[None,:,:])**2,axis=2)
 rugged=.20*np.mean(np.sin(5.1*theta[:,None,:]+phase[None,:,:]),axis=2)
 return (1/(1+np.exp(-2*(fit+rugged+.65)))).mean(axis=1)

def generate(agent,seed,tag,k,scope,policy):
 if scope=='none':return np.empty((0,6))
 rng=np.random.default_rng(np.random.SeedSequence([seed,tag,991]))
 theta=agent[:4]; step=np.exp(agent[4]); bias=agent[5]
 delta=rng.normal(size=(k,4))+bias
 if scope=='restricted':delta[:,2:]=0
 t=np.clip(theta+step*delta,-2,2)
 logstep=np.full(k,agent[4]); bs=np.full(k,bias)
 if policy:
  logstep=np.clip(logstep+rng.normal(0,.18,k),np.log(.04),np.log(1.2))
  bs=np.clip(bs+rng.normal(0,.12,k),-1.2,1.2)
 return np.column_stack((t,logstep,bs))

def probe(agent,seed,probe_tasks,k):
 # Search-policy competence: score gain on future tasks, with identical draws for all branches.
 # Negative outcomes are reported separately; baseline 'best-of-k' cannot be negative by definition.
 gains=[]; downside=[]
 for j,task in enumerate(probe_tasks):
  cand=generate(agent,seed,200000+j,k,'broad',True)
  base=scores(agent[:4][None,:],task)[0]
  vals=scores(cand[:,:4],task)
  gains.append(max(0.,float(vals.max()-base)))
  downside.append(float(np.mean(vals<base)))
 return float(np.mean(gains)),float(np.mean(downside))

def experiment(seed,group,T,k,probes):
 cfg=GROUPS[group];agent=np.array([-.65,.45,-.35,.25,np.log(.35),0.])
 # Independent fixed hidden task family; never used in candidate selection.
 heldout=tasks(seed,10,64)
 probe_tasks=[tasks(seed,1000+j,12) for j in range(probes)]
 rows=[]
 for t in range(T+1):
  P=float(scores(agent[:4][None,:],heldout)[0]);C,risk=probe(agent,seed,probe_tasks,k)
  row=dict(seed=seed,group=group,generation=t,P=P,C=C,probe_downside=risk,F=0.,accepted=0,false_accept=0,selection_gain=0.,audit_gain=0.,candidates=0)
  if t<T:
   candidate=generate(agent,seed,10000+t,k,cfg['scope'],cfg['policy'])
   row['candidates']=len(candidate)
   if len(candidate):
    selection=tasks(seed,3000+t,32)
    base=float(scores(agent[:4][None,:],selection)[0])
    true=scores(candidate[:,:4],selection)
    # C and D share candidate proposals and all conditions except selection noise.
    noise_rng=np.random.default_rng(np.random.SeedSequence([seed,t, 505]))
    perceived=true+noise_rng.normal(0,cfg['noise'],len(candidate))
    idx=int(np.argmax(perceived))
    if perceived[idx]>base:
     selected=candidate[idx]
     row['accepted']=1
     row['false_accept']=int(true[idx]<=base)
     row['selection_gain']=float(true[idx]-base)
     row['audit_gain']=float(scores(selected[:4][None,:],heldout)[0]-P)
     Cnext,_=probe(selected,seed,probe_tasks,k)
     row['F']=Cnext-C
     agent=selected
  rows.append(row)
 return rows

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--seeds',type=int,default=12)
 ap.add_argument('--generations',type=int,default=25)
 ap.add_argument('--candidates',type=int,default=6)
 ap.add_argument('--probes',type=int,default=24)
 ap.add_argument('--out',default='/mnt/data/smcep_v07')
 args=ap.parse_args(); out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
 rows=[]
 for seed in range(args.seeds):
  for group in GROUPS: rows.extend(experiment(seed,group,args.generations,args.candidates,args.probes))
 with (out/'trajectories.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 summary=[]
 for g in GROUPS:
  g_rows=[r for r in rows if r['group']==g]
  initial={r['seed']:r for r in g_rows if r['generation']==0}
  final={r['seed']:r for r in g_rows if r['generation']==args.generations}
  dp=np.array([final[s]['P']-initial[s]['P'] for s in initial]);dc=np.array([final[s]['C']-initial[s]['C'] for s in initial])
  trans=[r for r in g_rows if r['generation']<args.generations]
  accepts=sum(r['accepted'] for r in trans)
  summary.append(dict(group=g,delta_P=float(dp.mean()),delta_C=float(dc.mean()),sd_delta_P=float(dp.std(ddof=1)),sd_delta_C=float(dc.std(ddof=1)),accept_rate=accepts/len(trans),false_accept_given_accept=sum(r['false_accept'] for r in trans)/max(1,accepts),mean_F_on_accept=float(np.mean([r['F'] for r in trans if r['accepted']])) if accepts else 0,mean_audit_gain_on_accept=float(np.mean([r['audit_gain'] for r in trans if r['accepted']])) if accepts else 0))
 by_group={r['group']:r for r in summary}
 paired=[]
 for g1,g0 in [('D','C'),('C','B'),('C','E_scope'),('C','E_policy')]:
  diffs=np.array([(next(r for r in rows if r['seed']==s and r['group']==g1 and r['generation']==args.generations)['P']-next(r for r in rows if r['seed']==s and r['group']==g0 and r['generation']==args.generations)['P']) for s in range(args.seeds)])
  paired.append(dict(comparison=f'{g1}-{g0}',mean_final_P_difference=float(diffs.mean()),sd=float(diffs.std(ddof=1))))
 data=dict(parameters=vars(args),groups=GROUPS,summary=summary,paired=paired,limitations=['Synthetic tasks, no LLM or real code edits','C is best-of-k improvement opportunity, not independent agent research success','F is local paired probe difference, not long-run causal recursion','A/B/C confound scope and policy; ablations are exploratory','No reward hacking mechanism, only evaluator noise','Pilot size; descriptive only, no preregistered confirmatory inference'])
 (out/'summary.json').write_text(json.dumps(data,indent=2))
 print(json.dumps(dict(summary=summary,paired=paired),indent=2))
if __name__=='__main__':main()
