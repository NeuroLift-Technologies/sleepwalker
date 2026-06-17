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
});
