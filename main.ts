// Entry program for gta6-meme-x-01 (Node 22, standard library only).
//
// The real entry is the X post named in POST.json. This program has one
// small job: place a copy of that file where the grader expects to find
// it. It reads the source and destination folders from the environment
// so the same code works inside the grading container and in a local
// checkout.
//
// Local run:
//   MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=/tmp/out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const sourceDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const destinationDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(destinationDir, { recursive: true });

const sourcePath = join(sourceDir, "POST.json");
const destinationPath = join(destinationDir, "POST.json");

try {
  copyFileSync(sourcePath, destinationPath);
} catch (error) {
  const reason = error instanceof Error ? error.message : String(error);
  console.error(`Failed to copy POST.json from ${sourcePath} to ${destinationPath}: ${reason}`);
  process.exit(1);
}
