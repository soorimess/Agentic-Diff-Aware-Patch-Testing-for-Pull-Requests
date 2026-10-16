import json,os,sys
root=sys.argv[1]
for d in sorted(os.listdir(root)):
    p=os.path.join(root,d)
    if not os.path.exists(p+'/result.json'): continue
    r=json.load(open(p+'/result.json')); log=json.load(open(p+'/tool_log.json'))
    inj=json.load(open(p+'/injected_messages.json')) if os.path.exists(p+'/injected_messages.json') else []
    cov=r.get('changed_line_coverage') or {}; mut=(r.get('mutation') or {}).get('agent') or {}
    print(f"\n## {d} {r['f2p']} act={r['actions']} ${r['usage']['cost_usd']:.2f} cov={cov.get('percent')} ({cov.get('executable_changed_lines')} lines) mut={mut.get('killed')}/{(r.get('mutation') or {}).get('total')} | {r['why'][:90]}")
    seq=[]
    for i,e in enumerate(log):
        t=e.get('tool')
        if t=='verify':
            still=[n for n,v in (e.get('after') or {}).items() if v in ('FAILED','ERROR')]
            seq.append(f"{i}:V{'+' if e.get('flipped') and not still else ('~' if e.get('flipped') else '-')}")
        elif t=='coverage': seq.append(f"{i}:C{'x' if 'error' in e else (e.get('result') or {}).get('percent')}")
        elif t=='mutation': seq.append(f"{i}:M{'x' if 'error' in e else str(e.get('killed'))+'/'+str(e.get('total'))}")
    print('  ', ' '.join(seq)[:700])
    print('   refusals:', [(m.get('at_tool'), m.get('reason')) for m in inj])
