// Contract tests for the short contact / Briefing form: email is required, the one-line message is optional.
import assert from "node:assert/strict";
import { validate } from "../../site/functions/api/contact.js";

let n = 0;
const t = (name, fn) => { fn(); n++; };

t("email alone is a valid Briefing or Teardown request", () => {
  for (const topic of ["Briefing invitation", "Margin Teardown"]) {
    const { v, e } = validate({ email: "ops@example.com", topic });
    assert.deepEqual(e, {});
    assert.equal(v.email, "ops@example.com");
    assert.equal(v.topic, topic);
    assert.equal(v.name, "Not given");
    assert.equal(v.message, "Not given");
  }
});

t("a one-line message is kept when provided", () => {
  const { v, e } = validate({ email: "ops@example.com", topic: "Margin Teardown", message: "Debit routing in the US" });
  assert.deepEqual(e, {});
  assert.equal(v.message, "Debit routing in the US");
});

t("blank or whitespace-only messages are stored as Not given", () => {
  const { v, e } = validate({ email: "ops@example.com", topic: "Something else", message: "   " });
  assert.deepEqual(e, {});
  assert.equal(v.message, "Not given");
});

t("missing or invalid email is rejected", () => {
  const missing = validate({ topic: "Briefing invitation" });
  assert.equal(missing.e.email, "Please enter your email address.");
  const bad = validate({ email: "not-an-email", topic: "Briefing invitation" });
  assert.match(bad.e.email, /^Please enter a valid email address/);
});

t("unknown topic is rejected", () => {
  const { e } = validate({ email: "ops@example.com", topic: "Not a topic" });
  assert.equal(e.topic, "Please choose a topic.");
});

console.log(`contact: ${n} local tests passed`);
