import { test } from 'node:test';
import assert from 'node:assert/strict';
import { classify } from './outcomes.mjs';
test('access blocker cannot become a pass', () => assert.equal(classify({status:'skipped',annotations:[{type:'access-blocker'}]}), 'BLOCKED'));
test('unexecuted case is not a pass', () => assert.equal(classify({status:'skipped',annotations:[]}), 'NOT RUN'));
test('assertion failure stays failure', () => assert.equal(classify({status:'failed',annotations:[]}), 'FAIL'));
test('executed success is pass', () => assert.equal(classify({status:'passed',annotations:[]}), 'PASS'));
test('missing browser is an environment blocker', () => assert.equal(classify({status:'failed',errors:[{message:"browserType.launch: Executable doesn't exist at /cache/chromium"}]}), 'BLOCKED'));
