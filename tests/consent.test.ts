import { ConsentManager, ConsentLevel } from '../src/consent';
import { EmotionalState } from '../src/stateDetection';

/** Build an EmotionalState with sensible defaults for targeted assertions. */
function state(overrides: Partial<EmotionalState> = {}): EmotionalState {
  return {
    stateType: 'neutral',
    protective: false,
    requiresCheckIn: false,
    indicators: {
      dissociation: false,
      numbing: false,
      avoidance: false,
      detachment: false,
      crisis: { suicidalIdeation: false, selfHarm: false, safetyConcern: false },
    },
    confidence: 0,
    explicitSuicidalIdeation: false,
    selfHarmIndicators: false,
    inabilityToEnsureSafety: false,
    ...overrides,
  };
}

describe('ConsentManager', () => {
  it('escalates any crisis flag to RRTA_HANDOFF', () => {
    const cm = new ConsentManager();
    expect(cm.determineLevel(state({ explicitSuicidalIdeation: true }))).toBe(
      ConsentLevel.RRTA_HANDOFF,
    );
    expect(cm.determineLevel(state({ selfHarmIndicators: true }))).toBe(ConsentLevel.RRTA_HANDOFF);
    expect(cm.determineLevel(state({ inabilityToEnsureSafety: true }))).toBe(
      ConsentLevel.RRTA_HANDOFF,
    );
  });

  it('returns SAFETY_CHECK when a check-in is required without a crisis flag', () => {
    const cm = new ConsentManager();
    expect(cm.determineLevel(state({ requiresCheckIn: true }))).toBe(ConsentLevel.SAFETY_CHECK);
  });

  it('defaults a protective state to PASSIVE', () => {
    const cm = new ConsentManager();
    expect(cm.determineLevel(state({ protective: true }))).toBe(ConsentLevel.PASSIVE);
  });

  it('uses LOW_PRESSURE when TOI opts into offering support', () => {
    const cm = new ConsentManager({ swp: { intervention_threshold: 'offer_support_without_pressure' } });
    expect(cm.determineLevel(state({ protective: true }))).toBe(ConsentLevel.LOW_PRESSURE);
  });

  it('returns PASSIVE for a neutral state', () => {
    expect(new ConsentManager().determineLevel(state())).toBe(ConsentLevel.PASSIVE);
  });

  it('provides a message for every consent level', () => {
    const cm = new ConsentManager();
    for (const level of Object.values(ConsentLevel)) {
      expect(typeof cm.getConsentMessage(level)).toBe('string');
      expect(cm.getConsentMessage(level).length).toBeGreaterThan(0);
    }
  });
});
