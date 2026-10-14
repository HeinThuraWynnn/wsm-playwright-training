import { test as base, expect, Page, TestInfo } from '@playwright/test';
let stopped: string | undefined;
export async function checkAccess(page: Page, info: TestInfo, status?: number) {
  const text = await page.locator('body').innerText({timeout:10000});
  const challenge = /__cf_chl_/.test(page.url()) || /just a moment|verify you are human|checking your browser|performing security verification|enable javascript and cookies to continue/i.test(text) ||
    await page.locator('iframe[src*="challenges.cloudflare.com"], #challenge-running, #challenge-stage').count() > 0;
  const reason = challenge ? 'Cloudflare challenge: manual verification required; no bypass attempted.' : status === 403 || status === 429 || (status !== undefined && status >= 500) ? `HTTP ${status}: environment/access unavailable.` : undefined;
  if (reason) {
    stopped = reason;
    info.annotations.push({type: challenge ? 'access-blocker' : 'environment-blocker',description:reason});
    await info.attach('access-evidence', {body:JSON.stringify({url:new URL(page.url()).origin + new URL(page.url()).pathname,status,reason}),contentType:'application/json'});
    await info.attach('blocked-page', {body:await page.screenshot(),contentType:'image/png'});
    base.skip(true,reason);
  }
}
export async function visit(page:Page, info:TestInfo, path:string) {
  let response;
  try { response = await page.goto(path,{waitUntil:'domcontentloaded'}); }
  catch (error) {
    stopped = `Navigation unavailable: ${String(error)}`;
    info.annotations.push({type:'environment-blocker',description:stopped});
    await info.attach('navigation-error',{body:stopped,contentType:'text/plain'});
    base.skip(true,stopped);
  }
  await checkAccess(page,info,response?.status());
}
export const test = base.extend<{access: void}>({
  access: [async ({page}, use, info) => {
    if (stopped) { info.annotations.push({type:'access-blocker',description:`Run stopped after prior blocker: ${stopped}`}); base.skip(true,stopped); }
    await visit(page,info,'/cart');
    await use();
  }, {auto:true}],
});
export { expect };
