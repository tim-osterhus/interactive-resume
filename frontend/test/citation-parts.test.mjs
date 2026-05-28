import assert from "node:assert/strict";
import test from "node:test";

import { citationParts } from "../src/assets/site.js";

test("citationParts splits text and source chips in order", () => {
  const parts = citationParts("Built proof [S1] and [S2].");

  assert.deepEqual(parts.map((part) => part.type), ["text", "citation", "text", "citation", "text"]);
  assert.equal(parts[1].id, "S1");
  assert.equal(parts[3].id, "S2");
});

test("citationParts keeps plain text untouched when there are no citations", () => {
  assert.deepEqual(citationParts("No citations yet."), [{ type: "text", value: "No citations yet." }]);
});

test("citationParts handles adjacent citations", () => {
  assert.deepEqual(citationParts("[S1][S2]").map((part) => part.id), ["S1", "S2"]);
});
