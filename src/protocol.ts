/**
 * Core Sleepwalker Protocol Implementation
 */

import { StateDetector, EmotionalState } from './stateDetection';
import { ConsentManager, ConsentLevel } from './consent';
import { ContinuityManager } from './continuity';
import { TOILoader } from './toiLoader';

export interface SWPOptions {
  userToiPath?: string;
  privacyMode?: string;
  loggingEnabled?: boolean;
  storagePath?: string;
}

export class SleepwalkerProtocol {
  private userToi: any;
  private stateDetector: StateDetector;
  private consentManager: ConsentManager;
  private continuityManager: ContinuityManager;
  private loggingEnabled: boolean;

  constructor(options: SWPOptions = {}) {
    this.loggingEnabled = options.loggingEnabled !== false;
    const toiLoader = new TOILoader(options.userToiPath);
    this.userToi = options.userToiPath ? toiLoader.load() : {};
    this.stateDetector = new StateDetector();
    this.consentManager = new ConsentManager(this.userToi);
    this.continuityManager = new ContinuityManager(options.storagePath || '.swp_storage');
    if (this.loggingEnabled) console.log('Sleepwalker Protocol initialized');
  }

  detectEmotionalState(userInput: string, sessionHistory: any[] = []): EmotionalState {
    const state = this.stateDetector.detect(userInput, sessionHistory);
    if (this.loggingEnabled) {
      console.log(`SWP: State=${state.stateType}, Protective=${state.protective}`);
    }
    return state;
  }

  assessInteraction(userInput: string, sessionHistory: any[] = []): any {
    const emotionalState = this.detectEmotionalState(userInput, sessionHistory);
    const consentLevel = this.consentManager.determineLevel(emotionalState);
    return {
      emotionalState,
      consentLevel,
      swpActive: this.userToi.swp?.active !== false,
      protectiveStateActive: emotionalState.protective,
    };
  }

  generateResponse(userInput: string, detectedState?: EmotionalState): any {
    const state = detectedState || this.detectEmotionalState(userInput);
    if ((this.userToi.swp?.active !== false) && state.protective) {
      return {
        responseType: 'stable_low_demand',
        guidance: 'Maintain stable, task-focused interaction',
        intervention: 'none',
      };
    }
    if (state.requiresCheckIn) {
      const level = this.consentManager.determineLevel(state);
      return {
        responseType: 'consent_offer',
        level,
        guidance: this.consentManager.getConsentMessage(level),
        intervention: 'consent_required',
      };
    }
    return {
      responseType: 'neutral',
      guidance: 'Provide task-focused support',
      intervention: 'none',
    };
  }

  requiresRrtaHandoff(userState: EmotionalState): boolean {
    return userState.explicitSuicidalIdeation || userState.selfHarmIndicators || userState.inabilityToEnsureSafety;
  }
}

export const SWP = SleepwalkerProtocol;
