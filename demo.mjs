import fs from 'node:fs';
import {execute,state,snapshot,safeError,ROOT} from './scripts/runtime.mjs';
try {
 if(!state.contract)throw Error('Deploy and finalize first.');
 if(state.transactions.some(x=>x.action==='commit'))throw Error('Demo already started; reconcile original transactions, do not resend.');
 await execute('commit',['Parcel transit time for route A','hours',JSON.stringify(['Route A parcel transit time is 12 to 24 hours, inclusive.','Route A parcel transit time is 30 to 40 hours, inclusive.','The packaging weighs 200 grams.','Route A parcel transit time is approximately 20 hours.'])]);
 await execute('resolve',['1']);
 const result=await snapshot();
 const record=result.items.find(x=>x.id==='1');
 if(record?.status!=='resolved'||record.result.intersection.status!=='conflict')throw Error('Expected resolved conflict was not observed. Inspect committed result, do not resend.');
 if(record.result.intersection.lower!==30||record.result.intersection.upper!==24)throw Error('Unexpected conflict boundaries.');
 fs.writeFileSync(ROOT+'/demo-result.json',JSON.stringify(result,null,2));
 fs.writeFileSync(ROOT+'/deployment.json',JSON.stringify({network:'Bradbury Phase 2',chainId:4221,contract:state.contract,wallet:state.wallet,transactions:result.transactions.map(x=>({action:x.action,txId:x.txId,status:x.status,netCostGEN:x.netCostGEN})),netCostGEN:result.netCostGEN},null,2));
 console.log(JSON.stringify(result,null,2));
}catch(e){console.error(safeError(e));process.exitCode=1;}
