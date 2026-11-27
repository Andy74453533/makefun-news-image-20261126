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
const outPath = join(outDir, 'entry.png');
writeFileSync(outPath, bytes);
// Verify the copy landed whole: the grader runs the program twice and both
// runs must write the same bytes, so a short write must fail loudly here.
const written = readFileSync(outPath);
if (!written.equals(bytes)) {
  throw new Error(`entry.png copy mismatch: wrote ${written.length} of ${bytes.length} bytes`);
}
console.log(`wrote ${bytes.length} bytes to ${outPath}`);
