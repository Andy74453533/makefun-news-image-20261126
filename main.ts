// News-image entry for 26 November 2026 (Node 22, standard library only).
// The front page was composed in this repository (see compose.py) and saved
// as entry.png; this program writes that exact file to the output directory.
// Run locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(here, 'entry.png'));
writeFileSync(join(outDir, 'entry.png'), bytes);
console.log(`wrote ${bytes.length} bytes to ${join(outDir, 'entry.png')}`);
