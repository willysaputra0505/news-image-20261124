// Entry point for news-image-20261124.
// Copies the poster entry.png (built by generate.py) into the output
// directory and checks the result stays within the 1 MiB gate limit.
// Node 22, standard library only; no network, no randomness.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAX_BYTES = 1024 * 1024;

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  console.error(`missing source image: ${source}`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const size = statSync(target).size;
if (size > MAX_BYTES) {
  console.error(`output too large: ${size} bytes (limit ${MAX_BYTES})`);
  process.exit(1);
}

console.log(`wrote ${target} (${size} bytes)`);
