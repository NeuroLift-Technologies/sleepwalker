/**
 * Consent Management Module
 */

import { EmotionalState } from './stateDetection';

export enum ConsentLevel {
  PASSIVE = 'PASSIVE',
  LOW_PRESSURE = 'LOW_PRESSURE',
  SAFETY_CHECK = 'SAFETY_CHECK',
  RRTA_HANDOFF = 'RRTA_HANDOFF',
}

export class ConsentManager {
  private userToi: any;
  private swpConfig: any;

  constructor(userToi: any = {}) {
    this.userToi = userToi;
    this.swpConfig = userToi.swp || {};
  }

  determineLevel(emotionalState: EmotionalState): ConsentLevel {
    if (
      emotionalState.explicitSuicidalIdeation ||
      emotionalState.selfHarmIndicators ||
      emotionalState.inabilityToEnsureSafety
    ) {
      return ConsentLevel.RRTA_HANDOFF;
    }

    if (emotionalState.requiresCheckIn) {
      return ConsentLevel.SAFETY_CHECK;
    }

    if (emotionalState.protective) {
      const threshold = this.swpConfig.intervention_threshold || 'user_initiated_only';
      if (threshold === 'offer_support_without_pressure') {
        return ConsentLevel.LOW_PRESSURE;
      }
      return ConsentLevel.PASSIVE;
    }

    return ConsentLevel.PASSIVE;
  }

  getConsentMessage(level: ConsentLevel): string {
    const messages = {
      [ConsentLevel.PASSIVE]: "I'm here if you need anything. No pressure.",
      [ConsentLevel.LOW_PRESSURE]: "I can provide support if you'd like. Your choice.",
      [ConsentLevel.SAFETY_CHECK]: "I want to check in: Are you safe right now?",
      [ConsentLevel.RRTA_HANDOFF]: "I'm concerned about your safety. Can I provide crisis resources?",
    };
    return messages[level];
  }
}
