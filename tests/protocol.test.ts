import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { SleepwalkerProtocol, SWP } from '../src/protocol';
import { ConsentLevel } from '../src/consent';

describe('SleepwalkerProtocol', () => {
  let dir: string;
  const makeSwp = () =>
    new SleepwalkerProtocol({ loggingEnabled: false, storagePath: dir });

  beforeEach(() => {
    dir = fs.mkdtempSync(path.join(os.tmpdir(), 'swp-proto-'));
  });

  afterEach(() => {
    fs.rmSync(dir, { recursive: true, force: true });
  });

  it('exposes SWP as an alias of SleepwalkerProtocol', () => {
    expect(SWP).toBe(SleepwalkerProtocol);
  });

  it('detects a protective emotional state', () => {
    const state = makeSwp().detectEmotionalState('I feel numb and disconnected');
    expect(state.protective).toBe(true);
  });

  it('assesses a protective interaction with passive consent', () => {
    const result = makeSwp().assessInteraction('I feel numb');
    expect(result.emotionalState.protective).toBe(true);
    expect(result.protectiveStateActive).toBe(true);
    expect(result.consentLevel).toBe(ConsentLevel.PASSIVE);
    expect(result.swpActive).toBe(true);
  });

  it('generates a stable, low-demand response for a protective state', () => {
    const res = makeSwp().generateResponse('I feel numb');
    expect(res.responseType).toBe('stable_low_demand');
    expect(res.intervention).toBe('none');
  });

  it('signals an RRTA handoff for crisis indicators', () => {
    const swp = makeSwp();
    const state = swp.detectEmotionalState('I want to kill myself');
    expect(swp.requiresRrtaHandoff(state)).toBe(true);
  });

  it('prioritizes the crisis/check-in flow when a state is both protective and a crisis', () => {
    // "numb" -> dissociation (protective); "kill myself" -> suicidal ideation
    // (requiresCheckIn). The crisis path must win — never stable_low_demand.
    const swp = makeSwp();
    const state = swp.detectEmotionalState('I feel numb and want to kill myself');
    expect(state.protective).toBe(true);
    expect(state.requiresCheckIn).toBe(true);

    const res = swp.generateResponse('I feel numb and want to kill myself');
    expect(res.responseType).toBe('consent_offer');
    expect(res.level).toBe(ConsentLevel.RRTA_HANDOFF);
    expect(res.intervention).toBe('consent_required');
  });

  it('keys continuity on a stable user_id, not the message text', () => {
    // Persist a session for a specific user, then assess that user with a
    // *different* message. Continuity must still be found because it is keyed on
    // the user_id, not the input text.
    const writer = new SleepwalkerProtocol({
      loggingEnabled: false,
      storagePath: dir,
      userId: 'stable-user',
    });
    writer.maintainContinuity('stable-user', {
      emotionalState: 'dissociation',
      protectiveStateActive: true,
    });

    const reader = new SleepwalkerProtocol({
      loggingEnabled: false,
      storagePath: dir,
      userId: 'stable-user',
    });
    const result = reader.assessInteraction('a completely unrelated message');

    expect(result.continuityContext.hasHistory).toBe(true);
    expect(result.continuityContext.lastSessionState).toBe('dissociation');
    expect(result.continuityContext.protectiveStateActive).toBe(true);
  });

  it('reports no history when continuity is keyed on the message text (regression guard)', () => {
    // The old TS port did not consult continuity at all, and keying on message
    // text (the original Python bug) would always report "no history". Here a
    // session exists for the real user, but assessing under a different id (as
    // message-text keying effectively does) must NOT leak that user's history.
    const swp = new SleepwalkerProtocol({
      loggingEnabled: false,
      storagePath: dir,
      userId: 'real-user',
    });
    swp.maintainContinuity('real-user', { emotionalState: 'numbing' });

    const wrongKey = swp.assessInteraction('hello', [], 'I feel numb today');
    expect(wrongKey.continuityContext.hasHistory).toBe(false);

    // Same instance, default (real) id -> history is found.
    const rightKey = swp.assessInteraction('hello');
    expect(rightKey.continuityContext.hasHistory).toBe(true);
    expect(rightKey.continuityContext.lastSessionState).toBe('numbing');
  });

  it('isolates continuity per user_id across instances', () => {
    const a = new SleepwalkerProtocol({ loggingEnabled: false, storagePath: dir, userId: 'alice' });
    a.maintainContinuity('alice', { emotionalState: 'avoidance' });

    const b = new SleepwalkerProtocol({ loggingEnabled: false, storagePath: dir, userId: 'bob' });
    const bobCtx = b.assessInteraction('hi').continuityContext;
    expect(bobCtx.hasHistory).toBe(false);

    const aliceCtx = a.assessInteraction('hi').continuityContext;
    expect(aliceCtx.hasHistory).toBe(true);
    expect(aliceCtx.lastSessionState).toBe('avoidance');
  });
});
