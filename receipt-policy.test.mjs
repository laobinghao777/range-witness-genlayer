import {test} from 'node:test';
import assert from 'node:assert/strict';
import {acceptedFinalReceipt} from './scripts/receipt-policy.mjs';
const accepted={statusName:'FINALIZED',resultName:'MAJORITY_AGREE',lifecycle:{outcome:'accepted'},txExecutionResultName:'FINISHED_WITH_RETURN'};
test('accepted final execution passes',()=>assert.equal(acceptedFinalReceipt(accepted),true));
test('finalized majority-disagree never counts as success',()=>assert.equal(acceptedFinalReceipt({...accepted,resultName:'MAJORITY_DISAGREE',lifecycle:{outcome:'undetermined'}}),false));
test('majority agreement on a VM error is not a successful call',()=>assert.equal(acceptedFinalReceipt({...accepted,txExecutionResultName:'USER_ERROR'}),false));
test('unfinalized or incomplete receipts are rejected',()=>{assert.equal(acceptedFinalReceipt({...accepted,statusName:'ACCEPTED'}),false);assert.equal(acceptedFinalReceipt({}),false);});
