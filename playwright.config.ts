import { defineConfig, devices } from '@playwright/test';
export default defineConfig({
  testDir: './tests', fullyParallel: false, workers: 1, retries: 0,
  forbidOnly: true, timeout: 45000, maxFailures: 1,
  reporter: [['list'], ['html', { open: 'never' }], ['json', { outputFile: 'test-results/results.json' }]],
  use: { baseURL: 'https://demo.nopcommerce.com', ...devices['Desktop Chrome'],
    trace: 'retain-on-failure', screenshot: 'only-on-failure', video: 'off' },
});
