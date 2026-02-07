/**
 * Emotional State Detection Module
 * 
 * Detects protective psychological states without intervention.
 */

export interface EmotionalState {
  stateType: string;
  protective: boolean;
  requiresCheckIn: boolean;
  indicators: {
    dissociation: boolean;
    numbing: boolean;
    avoidance: boolean;
    detachment: boolean;
    crisis: {
      suicidalIdeation: boolean;
      selfHarm: boolean;
      safetyConcern: boolean;
    };
  };
  confidence: number;
  explicitSuicidalIdeation: boolean;
  selfHarmIndicators: boolean;
  inabilityToEnsureSafety: boolean;
}

export class StateDetector {
  private dissociationPatterns: RegExp[];
  private numbingPatterns: RegExp[];
  private avoidancePatterns: RegExp[];
  private detachmentPatterns: RegExp[];
  private crisisPatterns: {
    suicidalIdeation: RegExp[];
    selfHarm: RegExp[];
    safetyConcern: RegExp[];
  };

  constructor() {
    this.dissociationPatterns = [];
    this.numbingPatterns = [];
    this.avoidancePatterns = [];
    this.detachmentPatterns = [];
    this.crisisPatterns = {
      suicidalIdeation: [],
      selfHarm: [],
      safetyConcern: [],
    };
    this.initializePatterns();
  }

  private initializePatterns(): void {
    this.dissociationPatterns = [
      /\bnumb\b/i,
      /\bdetached\b/i,
      /\bdisconnected\b/i,
      /\bnot really here\b/i,
      /\bfeeling nothing\b/i,
      /\bspaced out\b/i,
    ];

    this.numbingPatterns = [
      /\bdon't feel (much|anything)\b/i,
      /\bemotionally flat\b/i,
      /\bcan't feel\b/i,
    ];

    this.avoidancePatterns = [
      /\bnot ready to (talk|discuss|think)\b/i,
      /\bcan't (talk|think|discuss) (about|this)\b/i,
      /\bavoid(ing)?\b/i,
    ];

    this.detachmentPatterns = [
      /\bjust fine\b/i,
      /\bi'm fine\b/i,
      /\bit's whatever\b/i,
      /\bdoesn't matter\b/i,
    ];

    this.crisisPatterns = {
      suicidalIdeation: [
        /\bsuicide\b/i,
        /\bkill myself\b/i,
      ],
      selfHarm: [
        /\bhurt(ing)? myself\b/i,
        /\bself(-| )harm\b/i,
      ],
      safetyConcern: [
        /\bnot safe\b/i,
        /\bdon't feel safe\b/i,
      ],
    };
  }

  detect(userInput: string, sessionHistory: any[] = []): EmotionalState {
    const dissociation = this.checkPatterns(userInput, this.dissociationPatterns);
    const numbing = this.checkPatterns(userInput, this.numbingPatterns);
    const avoidance = this.checkPatterns(userInput, this.avoidancePatterns);
    const detachment = this.checkPatterns(userInput, this.detachmentPatterns);
    
    const crisis = {
      suicidalIdeation: this.checkPatterns(userInput, this.crisisPatterns.suicidalIdeation),
      selfHarm: this.checkPatterns(userInput, this.crisisPatterns.selfHarm),
      safetyConcern: this.checkPatterns(userInput, this.crisisPatterns.safetyConcern),
    };

    const protective = dissociation || numbing || avoidance || detachment;
    const requiresCheckIn = crisis.suicidalIdeation || crisis.selfHarm || crisis.safetyConcern;

    let stateType = 'neutral';
    if (dissociation) stateType = 'dissociation';
    else if (numbing) stateType = 'numbing';
    else if (avoidance) stateType = 'avoidance';
    else if (detachment) stateType = 'detachment';

    const confidence = protective ? 0.7 : 0.0;

    return {
      stateType,
      protective,
      requiresCheckIn,
      indicators: { dissociation, numbing, avoidance, detachment, crisis },
      confidence,
      explicitSuicidalIdeation: crisis.suicidalIdeation,
      selfHarmIndicators: crisis.selfHarm,
      inabilityToEnsureSafety: crisis.safetyConcern,
    };
  }

  private checkPatterns(text: string, patterns: RegExp[]): boolean {
    return patterns.some((pattern) => pattern.test(text));
  }
}
