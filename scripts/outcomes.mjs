export function classify(result) {
  if (result.errors?.some(e => /browserType\.launch: Executable doesn't exist/.test(e.message ?? ''))) return 'BLOCKED';
  if (result.annotations?.some(a => a.type === 'access-blocker' || a.type === 'environment-blocker')) return 'BLOCKED';
  if (result.status === 'passed') return 'PASS';
  if (result.status === 'failed' || result.status === 'timedOut' || result.status === 'interrupted') return 'FAIL';
  return 'NOT RUN';
}
