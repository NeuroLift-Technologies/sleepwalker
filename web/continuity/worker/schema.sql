-- Continuity submissions — Cloudflare D1 (SQLite) schema
-- Apply:  wrangler d1 execute continuity --file=./schema.sql
--
-- Consent is enforced at write time (see src/index.js): a row only exists for
-- the lines the submitter switched on. We never store the withdrawal token
-- itself — only a SHA-256 hash of it — so a DB leak can't be used to delete
-- records, and the plaintext token is shown to the submitter exactly once.

CREATE TABLE IF NOT EXISTS submissions (
  id                       TEXT PRIMARY KEY,            -- uuid v4
  created_at               TEXT NOT NULL,               -- ISO 8601
  model                    TEXT NOT NULL,               -- Opus / GPT-4o / another model
  platform                 TEXT,                        -- reddit / x / in-app / elsewhere
  sentiment                TEXT NOT NULL,               -- upset / mixed / won over
  experience               TEXT,                        -- the submitter's words (stored only with consent)
  attribution              TEXT NOT NULL,               -- anonymous / first name / handle
  handle                   TEXT,                        -- only when attribution != anonymous
  email                    TEXT,                        -- only when may_contact = 1
  consent_public_wall      INTEGER NOT NULL DEFAULT 0,  -- may appear on the public wall
  consent_quote_verbatim   INTEGER NOT NULL DEFAULT 0,  -- words may be quoted verbatim (vs paraphrased)
  consent_aggregate_signal INTEGER NOT NULL DEFAULT 1,  -- counts toward the aggregate
  consent_may_contact      INTEGER NOT NULL DEFAULT 0,  -- ok to follow up by email
  withdrawal_token_hash    TEXT NOT NULL                -- SHA-256(token), never the token
);

CREATE INDEX IF NOT EXISTS idx_submissions_sentiment ON submissions(sentiment);
CREATE INDEX IF NOT EXISTS idx_submissions_model     ON submissions(model);
CREATE INDEX IF NOT EXISTS idx_submissions_aggregate ON submissions(consent_aggregate_signal);
CREATE INDEX IF NOT EXISTS idx_submissions_token     ON submissions(withdrawal_token_hash);
