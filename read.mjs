// Public, read-only verification. No private key, signer or transaction submission.
import fs from 'node:fs';
import {createClient} from 'genlayer-js';
import {testnetBradbury} from 'genlayer-js/chains';
import {NODE_RPC} from './scripts/rpc.mjs';
const published=JSON.parse(fs.readFileSync(new URL('./deployment.json',import.meta.url),'utf8').replace(/^\uFEFF/,''));
const address=process.argv[2]??published.contract;
if(!/^0x[0-9a-fA-F]{40}$/.test(address))throw Error('Invalid contract address');
const client=createClient({chain:testnetBradbury,endpoint:NODE_RPC});
const result=JSON.parse(await client.readContract({address,functionName:'list_cases',args:[0,50],account:{address:published.wallet}}));
console.log(JSON.stringify({contract:address,chainId:4221,...result},null,2));
