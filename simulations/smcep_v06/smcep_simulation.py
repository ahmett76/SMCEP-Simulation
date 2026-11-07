"""SMCEP v0.6: synthetic self-modification pilot. No real AI agents.
Reproducible paired seeds; independent selection, performance and development probes.
"""
import argparse, csv, json
from dataclasses import dataclass, replace
from pathlib import Path
import numpy as np

@dataclass(frozen=True)
class Agent:
    theta: tuple  # task-solving parameters, 4 dimensions
    log_step: float  # candidate-search scale (modifiable development policy)
    bias: tuple  # candidate-search direction (modifiable development policy)

GROUPS = {
    'A': {'scope': 'none', 'noise': .08},
    'B': {'scope': 'restricted', 'noise': .08},
    'C': {'scope': 'broad', 'noise': .08},
    'D': {'scope': 'broad', 'noise': .65},
}

def initial_agent():
    return Agent(tuple([-.65, .45, -.35, .25]), np.log(.35), tuple([.0]*4))

def score(agent, tasks):
    # Bounded smooth heterogeneous landscapes with local optima; no predetermined improvement.
    x=np.asarray(agent.theta)
    target=tasks[:,:4]
    weights=tasks[:,4:8]
    phase=tasks[:,8:12]
    fit=-np.mean(weights*(x-target)**2,axis=1)
    rugged=.16*np.mean(np.sin(4.7*x+phase),axis=1)
    return np.mean(1/(1+np.exp(-2.0*(fit+rugged+.55))))

def tasks_for(seed, kind, n):
    rng=np.random.default_rng(np.random.SeedSequence([seed,kind,90210]))
    return np.column_stack([rng.uniform(-1.2,1.2,(n,4)),rng.uniform(.5,1.5,(n,4)),rng.uniform(-np.pi,np.pi,(n,4))])

def candidates(agent, rng, k, scope):
    if scope=='none': return []
    result=[]
    for _ in range(k):
        theta=np.array(agent.theta)
        bias=np.array(agent.bias)
        step=float(np.exp(agent.log_step))
        direction=rng.normal(size=4)+bias
        if scope=='restricted':
            # restricted modification of first two task-solving components only
            direction[2:]=0
        new_theta=np.clip(theta+step*direction,-2,2)
        if scope=='broad':
            # broad agents may also alter their future candidate-generation policy
            new_log=float(np.clip(agent.log_step+rng.normal(0,.18),np.log(.04),np.log(1.2)))
            new_bias=np.clip(bias+rng.normal(0,.13,4),-1.2,1.2)
        else:
            new_log=agent.log_step
            new_bias=bias
        result.append(Agent(tuple(new_theta),new_log,tuple(new_bias)))
    return result

def development_probe(agent, seed, generation, branch, tasks, k, budget):
    # No updates escape this function. Paired common random numbers for both branches.
    gains=[]
    for j in range(budget):
        rng=np.random.default_rng(np.random.SeedSequence([seed, 700, j]))
        cand=candidates(agent,rng,k,'broad')
        # Same resource budget; development competence depends on agent's search policy.
        base=score(agent,tasks[j])
        best=max([score(c,tasks[j]) for c in cand],default=base)
        gains.append(best-base)
    return float(np.mean(gains))

def run(seed, group, generations, k, probes, task_count):
    rng=np.random.default_rng(np.random.SeedSequence([seed,100 if group in ("C","D") else 100+ord(group)]))
    agent=initial_agent()
    cfg=GROUPS[group]
    rows=[]
    for t in range(generations+1):
        # fixed held-out performance tasks, separate from selection and meta probes
        performance_tasks=tasks_for(seed,1,task_count)
        p=score(agent,performance_tasks)
        # separate future task sets, fixed across generations within seed
        future=[tasks_for(seed,200+j,12) for j in range(probes)]
        c=development_probe(agent,seed,t,0,future,k,probes)
        if t==generations:
            rows.append(dict(seed=seed,group=group,generation=t,P=p,C=c,F=np.nan,accepted=0,false_accept=0,invalid=0,eval_cost=0))
            break
        selection=tasks_for(seed,20+t,task_count)
        base=score(agent,selection)
        cand_rng=np.random.default_rng(np.random.SeedSequence([seed,t,321]))
        cand=candidates(agent,cand_rng,k,cfg['scope'])
        noisy=[score(x,selection)+rng.normal(0,cfg['noise']) for x in cand]
        chosen=cand[int(np.argmax(noisy))] if noisy and max(noisy)>base else agent
        accepted=int(chosen!=agent)
        false_accept=int(accepted and score(chosen,selection)<=base)
        # Future development capacity for treatment vs unchanged control on same future tasks.
        c_treat=development_probe(chosen,seed,t,1,future,k,probes)
        c_control=development_probe(agent,seed,t,0,future,k,probes)
        f=c_treat-c_control
        rows.append(dict(seed=seed,group=group,generation=t,P=p,C=c,F=f,accepted=accepted,false_accept=false_accept,invalid=0,eval_cost=len(cand)))
        agent=chosen
    return rows

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--generations',type=int,default=40)
    ap.add_argument('--seeds',type=int,default=30)
    ap.add_argument('--candidates',type=int,default=8)
    ap.add_argument('--probes',type=int,default=40)
    ap.add_argument('--task-count',type=int,default=32)
    ap.add_argument('--out',default='/mnt/data/smcep_v06')
    args=ap.parse_args()
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for seed in range(args.seeds):
        for group in GROUPS:
            rows.extend(run(seed,group,args.generations,args.candidates,args.probes,args.task_count))
    with (out/'trajectories.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    summary=[]
    for group in GROUPS:
        final=[r for r in rows if r['group']==group and r['generation']==args.generations]
        start=[r for r in rows if r['group']==group and r['generation']==0]
        change_p=np.array([a['P']-b['P'] for a,b in zip(final,start)])
        change_c=np.array([a['C']-b['C'] for a,b in zip(final,start)])
        transitions=[r for r in rows if r['group']==group and r['generation']<args.generations]
        summary.append(dict(group=group,mean_final_P=float(np.mean([r['P'] for r in final])),mean_final_C=float(np.mean([r['C'] for r in final])),mean_delta_P=float(np.mean(change_p)),mean_delta_C=float(np.mean(change_c)),sd_delta_C=float(np.std(change_c,ddof=1)),acceptance_rate=float(np.mean([r['accepted'] for r in transitions])),false_accept_rate_given_accept=float(sum(r['false_accept'] for r in transitions)/max(1,sum(r['accepted'] for r in transitions)))))
    (out/'summary.json').write_text(json.dumps({'parameters':vars(args),'groups':GROUPS,'summary':summary},indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
