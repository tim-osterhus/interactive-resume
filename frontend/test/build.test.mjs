import assert from "node:assert/strict";
import { existsSync } from "node:fs";
import { rm } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { resolve } from "node:path";
import test from "node:test";

test("build copies the static frontend into dist", async () => {
  await rm(resolve("dist"), { recursive: true, force: true });

  const result = spawnSync(process.execPath, ["scripts/build.mjs"], {
    cwd: process.cwd(),
    encoding: "utf8",
  });

  assert.equal(result.status, 0, result.stderr);
  assert.ok(existsSync(resolve("dist", "index.html")));
  assert.ok(existsSync(resolve("dist", "assets", "site.js")));
});
