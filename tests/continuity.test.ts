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
    const stored = JSON.parse(fs.readFileSync(path.join(dir, 'user-1.json'), 'utf-8'));
    expect(stored.sessionCount).toBe(2);
    expect(stored.lastSession.emotionalState).toBe('numbing');
    // A different user is unaffected.
    expect(cm.getContext('user-2').hasHistory).toBe(false);
  });

  it('creates the storage directory if it does not exist', () => {
    const nested = path.join(dir, 'nested', 'store');
    new ContinuityManager(nested);
    expect(fs.existsSync(nested)).toBe(true);
  });
});
