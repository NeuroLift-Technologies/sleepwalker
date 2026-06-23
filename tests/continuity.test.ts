import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { ContinuityManager } from '../src/continuity';

describe('ContinuityManager', () => {
  let dir: string;

  beforeEach(() => {
    dir = fs.mkdtempSync(path.join(os.tmpdir(), 'swp-test-'));
  });

  afterEach(() => {
    fs.rmSync(dir, { recursive: true, force: true });
  });

  it('reports no history for an unknown user', () => {
    const cm = new ContinuityManager(dir);
    const ctx = cm.getContext('nobody');
    expect(ctx.hasHistory).toBe(false);
    expect(ctx.protectiveStateActive).toBe(false);
  });

  it('round-trips a saved session into context', () => {
    const cm = new ContinuityManager(dir);
    cm.saveSession('user-1', { emotionalState: 'dissociation', protectiveStateActive: true });
    const ctx = cm.getContext('user-1');
    expect(ctx.hasHistory).toBe(true);
    expect(ctx.lastSessionState).toBe('dissociation');
    expect(ctx.protectiveStateActive).toBe(true);
  });

  it('increments the session count and isolates users by id', () => {
    const cm = new ContinuityManager(dir);
    cm.saveSession('user-1', { emotionalState: 'neutral', protectiveStateActive: false });
    cm.saveSession('user-1', { emotionalState: 'numbing', protectiveStateActive: true });
    // Filenames are SHA-256 hashed (traversal/collision safe), so read back
    // through the public API rather than guessing the on-disk name.
    const ctx = cm.getContext('user-1');
    expect(ctx.sessionCount).toBe(2);
    expect(ctx.lastSessionState).toBe('numbing');
    // A different user is unaffected.
    expect(cm.getContext('user-2').hasHistory).toBe(false);
  });

  it('creates the storage directory if it does not exist', () => {
    const nested = path.join(dir, 'nested', 'store');
    new ContinuityManager(nested);
    expect(fs.existsSync(nested)).toBe(true);
  });

  it('contains a "../"-style user_id inside the storage dir (hashed filename)', () => {
    // Storage root lives one level below `dir` so that a successful "../" escape
    // would land a file in a sibling location we can detect.
    const storage = path.join(dir, 'store');
    const cm = new ContinuityManager(storage);

    const maliciousId = '../../etc/passwd';
    cm.saveSession(maliciousId, { emotionalState: 'neutral' });

    const storageRoot = fs.realpathSync(storage);

    // Nothing escaped: no `etc/passwd` was written next to the storage root, and
    // the would-be traversal target does not exist.
    expect(fs.existsSync(path.join(path.dirname(storageRoot), 'etc', 'passwd'))).toBe(false);
    expect(fs.existsSync(path.join(dir, 'etc'))).toBe(false);

    // Exactly one JSON file was written, and it sits directly inside the storage
    // root (the filename is the SHA-256 hash, not the raw traversal string).
    const entries = fs.readdirSync(storageRoot);
    const jsonFiles = entries.filter((f) => f.endsWith('.json'));
    expect(jsonFiles.length).toBe(1);
    expect(jsonFiles[0]).not.toContain('..');
    expect(jsonFiles[0]).not.toContain('/');

    // The hashed id still round-trips through the same hashing on read.
    expect(cm.getContext(maliciousId).hasHistory).toBe(true);
  });

  it('keeps distinct ids that sanitize to the same slug in separate files', () => {
    const cm = new ContinuityManager(dir);
    // Same stripped characters, different real ids.
    cm.saveSession('a/b', { emotionalState: 'numbing' });
    cm.saveSession('ab', { emotionalState: 'neutral' });
    expect(cm.getContext('a/b').lastSessionState).toBe('numbing');
    expect(cm.getContext('ab').lastSessionState).toBe('neutral');

    // Two emails that strip to identical characters stay separate.
    cm.saveSession('alice@example.com', { emotionalState: 'avoidance' });
    cm.saveSession('aliceexample.com', { emotionalState: 'dissociation' });
    expect(cm.getContext('alice@example.com').lastSessionState).toBe('avoidance');
    expect(cm.getContext('aliceexample.com').lastSessionState).toBe('dissociation');

    // Four ids -> four distinct files.
    const jsonFiles = fs.readdirSync(dir).filter((f) => f.endsWith('.json'));
    expect(jsonFiles.length).toBe(4);
  });
});
