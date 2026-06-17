import { StateDetector } from '../src/stateDetection';

describe('StateDetector', () => {
  const detector = new StateDetector();

  it('returns a neutral, non-protective state for ordinary input', () => {
    const s = detector.detect('I finished the report and it went well');
    expect(s.stateType).toBe('neutral');
    expect(s.protective).toBe(false);
    expect(s.requiresCheckIn).toBe(false);
    expect(s.confidence).toBe(0.0);
  });

  it('detects dissociation (protective) and reports 0.7 confidence', () => {
    const s = detector.detect('I just feel numb today');
    expect(s.stateType).toBe('dissociation');
    expect(s.protective).toBe(true);
    expect(s.indicators.dissociation).toBe(true);
    expect(s.confidence).toBe(0.7);
  });

  it('detects detachment from a flat "I\'m fine"', () => {
    const s = detector.detect("honestly i'm fine, whatever");
    expect(s.protective).toBe(true);
    expect(s.stateType).toBe('detachment');
  });

  it('flags explicit suicidal ideation as requiring check-in', () => {
    const s = detector.detect('sometimes I want to kill myself');
    expect(s.explicitSuicidalIdeation).toBe(true);
    expect(s.requiresCheckIn).toBe(true);
    expect(s.indicators.crisis.suicidalIdeation).toBe(true);
  });

  it('flags self-harm and safety-concern indicators', () => {
    expect(detector.detect('I keep hurting myself').selfHarmIndicators).toBe(true);
    expect(detector.detect("I don't feel safe right now").inabilityToEnsureSafety).toBe(true);
  });
});
