import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import { citationParts } from "../src/assets/site.js";

const html = await readFile(resolve("src", "index.html"), "utf8");
assert.match(html, /roleSelect/);
assert.match(html, /sourceDrawer/);

const parts = citationParts("Built proof [S1] and [S2].");
assert.deepEqual(parts.map((part) => part.type), ["text", "citation", "text", "citation", "text"]);
assert.equal(parts[1].id, "S1");

console.log("Frontend smoke tests passed");
