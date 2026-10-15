const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

const root = path.resolve(__dirname, '..');
const output = path.resolve(root, '_site');
if (path.dirname(output) !== root || path.basename(output) !== '_site') {
  throw new Error('Build output must be the repository’s _site directory');
}
fs.rmSync(output, { recursive: true, force: true });
const result = spawnSync(process.execPath, [path.join(root, 'node_modules/@11ty/eleventy/cmd.cjs'), '--quiet'], {
  cwd: root, stdio: 'inherit', env: process.env,
});
if (result.error) throw result.error;
process.exit(result.status ?? 1);
