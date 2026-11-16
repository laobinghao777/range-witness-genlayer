export function acceptedFinalReceipt(r) {
 return r.statusName==='FINALIZED' && r.resultName==='MAJORITY_AGREE' && r.lifecycle?.outcome==='accepted' && r.txExecutionResultName==='FINISHED_WITH_RETURN';
}
