import { test, expect, visit, checkAccess } from './support/fixtures';
import type { Page, TestInfo } from '@playwright/test';
const product = '/htc-one-m8-android-l-50';
const row = (page:Page) => page.locator('.cart tbody tr').filter({has:page.locator('.product-name')});
async function addProduct(page:Page, info:TestInfo) {
  await visit(page,info,product);
  await page.locator('.add-to-cart-button').click();
  await checkAccess(page,info);
  await expect(page.locator('.bar-notification.success')).toBeVisible();
  await visit(page,info,'/cart');
  await expect(row(page)).toHaveCount(1);
  await expect(row(page).locator('.product-name')).toHaveText('HTC One M8 Android L 5.0');
  await expect(row(page).locator('.qty-input')).toHaveValue('1');
}
function amount(value:string) {
  const match = value.match(/^\s*\$([\d,]+\.\d{2})\s*$/);
  if (!match) throw new Error(`Expected USD display, received ${value}`);
  return Math.round(Number(match[1].replaceAll(',',''))*100);
}
test('CART-001 empty guest cart', {tag:['@smoke','@regression']}, async ({page}) => {
  await expect(page.getByRole('heading',{name:'Shopping cart',exact:true})).toBeVisible();
  await expect(page.locator('.order-summary-content')).toContainText('Your Shopping Cart is empty!');
  await expect(row(page)).toHaveCount(0);
});
test('CART-002 add one product', {tag:['@smoke','@sanity','@regression']}, async ({page},info) => {
  await addProduct(page,info);
});
test('CART-003 update quantity and line subtotal', {tag:['@sanity','@regression']}, async ({page},info) => {
  await addProduct(page,info);
  const unit = amount(await row(page).locator('.product-unit-price').innerText());
  await row(page).locator('.qty-input').fill('2');
  await page.getByRole('button',{name:'Update shopping cart',exact:true}).click();
  await checkAccess(page,info);
  await expect(row(page).locator('.qty-input')).toHaveValue('2');
  await expect.poll(async()=>amount(await row(page).locator('.product-subtotal').innerText())).toBe(unit*2);
});
test('CART-004 remove own item', {tag:['@sanity','@regression']}, async ({page},info) => {
  await addProduct(page,info);
  await row(page).locator('input[name="removefromcart"]').check();
  await page.getByRole('button',{name:'Update shopping cart',exact:true}).click();
  await checkAccess(page,info);
  await expect(row(page)).toHaveCount(0);
  await expect(page.locator('.order-summary-content')).toContainText('Your Shopping Cart is empty!');
});
test('CART-005 cart persists across reload', {tag:['@regression']}, async ({page},info) => {
  await addProduct(page,info);
  const response = await page.reload({waitUntil:'domcontentloaded'});
  await checkAccess(page,info,response?.status());
  await expect(row(page)).toHaveCount(1);
  await expect(row(page).locator('.product-name')).toHaveText('HTC One M8 Android L 5.0');
  await expect(row(page).locator('.qty-input')).toHaveValue('1');
});
