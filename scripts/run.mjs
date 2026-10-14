import { spawnSync } from 'node:child_process';
import { cpSync, mkdirSync, readFileSync, existsSync, renameSync, writeFileSync } from 'node:fs';
import { classify } from './outcomes.mjs';
const suite = process.argv[2];
if (!['smoke','sanity','regression'].includes(suite)) throw new Error('Select smoke, sanity, or regression');
const run = new Date().toISOString().replace(/[:.]/g,'-');
const dir = `evidence/${run}-${suite}`;
mkdirSync(dir, {recursive:true});
// Remove a previous report from consideration without deleting its evidence.
if (existsSync('test-results/results.json')) renameSync('test-results/results.json', `${dir}/previous-results.json`);
const execution = spawnSync(process.execPath, ['node_modules/@playwright/test/cli.js','test','--grep',`@${suite}`], {encoding:'utf8'});
writeFileSync(`${dir}/execution.log`, (execution.stdout ?? '') + (execution.stderr ?? '') + (execution.error ? String(execution.error) : ''));
process.stdout.write(execution.stdout ?? ''); process.stderr.write(execution.stderr ?? '');
const rows = [];
function walk(suites) {
  for (const s of suites ?? []) {
    for (const spec of s.specs ?? []) for (const test of spec.tests ?? []) {
      const result = test.results?.at(-1);
      rows.push({case:spec.title, status:classify({status:result?.status, annotations:test.annotations,errors:result?.errors}), annotations:test.annotations, errors:result?.errors ?? [], attachments:result?.attachments ?? []});
    }
    walk(s.suites);
  }
}
let report;
if (existsSync('test-results/results.json')) {
  report = JSON.parse(readFileSync('test-results/results.json','utf8'));
  walk(report.suites);
  writeFileSync(`${dir}/playwright.json`, JSON.stringify(report,null,2));
}
if (existsSync('test-results')) cpSync('test-results', `${dir}/test-results`, {recursive:true});
if (existsSync('playwright-report')) cpSync('playwright-report', `${dir}/html`, {recursive:true});
const status = rows.some(r=>r.status==='FAIL') ? 'FAIL' : rows.some(r=>r.status==='BLOCKED') ? 'BLOCKED' : execution.status !== 0 || report?.errors?.length || !rows.length || rows.some(r=>r.status==='NOT RUN') ? 'NOT RUN' : 'PASS';
writeFileSync(`${dir}/summary.json`,JSON.stringify({run,suite,status,exitCode:execution.status,errors:report?.errors ?? [],cases:rows},null,2));
console.log(`Governed result: ${status}; evidence: ${dir}`);
process.exitCode = status === 'PASS' ? 0 : status === 'BLOCKED' ? 2 : 1;
