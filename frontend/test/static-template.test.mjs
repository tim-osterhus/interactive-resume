import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

test("homepage stays generic and public-template safe", async () => {
  const html = await readFile(resolve("src", "index.html"), "utf8");

  assert.match(html, /Your Name/);
  assert.match(html, /Evidence-backed interactive resume/);
  assert.match(html, /roleSelect/);
  assert.match(html, /profileSelect/);
  assert.match(html, /sourceDrawer/);
  assert.match(html, /What has this person built\?/);
  assert.doesNotMatch(html, /Tim Osterhus|Millrace|Maui|tim@millrace\.ai/i);
  assert.doesNotMatch(html, /F:\\|\/Users\/|\/home\//);
  assert.doesNotMatch(html, /Ã/);
});

test("frontend script uses DOM-safe rendering for answers and sources", async () => {
  const js = await readFile(resolve("src", "assets", "site.js"), "utf8");

  assert.match(js, /document\.createTextNode/);
  assert.match(js, /textContent/);
  assert.match(js, /replaceChildren/);
  assert.doesNotMatch(js, /answerPanel\.innerHTML\s*=\s*data\.answer/);
  assert.doesNotMatch(js, /drawerBody\.innerHTML/);
});
