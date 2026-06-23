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
  /**
   * Stable identifier for the user this instance serves. Used as the continuity
   * key when `assessInteraction` is called without an explicit `userId`. Falls
   * back to a `userId` declared in the TOI, or to `'default_user'` so a single
   * instance still maintains continuity across calls.
   */
  userId?: string;
}

export class SleepwalkerProtocol {
  private userToi: any;
  private userId: string;
  private stateDetector: StateDetector;
  private consentManager: ConsentManager;
  private continuityManager: ContinuityManager;
  private loggingEnabled: boolean;

  constructor(options: SWPOptions = {}) {
    this.loggingEnabled = options.loggingEnabled !== false;
    const toiLoader = new TOILoader(options.userToiPath);
    const loadedToi = options.userToiPath ? toiLoader.load() : {};
    // A malformed TOI can parse to a non-object; coerce so downstream `.swp`
    // lookups are always safe.
    this.userToi = loadedToi && typeof loadedToi === 'object' ? loadedToi : {};

    // Stable continuity identity for this instance. Never derive this from the
    // user's input text — doing so makes every interaction look like a brand new
    // user and continuity can never be retrieved. Accept an explicit id, then a
    // top-level or swp-nested TOI id. The id is hashed where it becomes a
    // filename (see ContinuityManager.userFile), so traversal is contained.
    const swpToi =
      this.userToi.swp && typeof this.userToi.swp === 'object' ? this.userToi.swp : {};
    this.userId = options.userId || this.userToi.user_id || swpToi.user_id || 'default_user';

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

  assessInteraction(userInput: string, sessionHistory: any[] = [], userId?: string): any {
    const emotionalState = this.detectEmotionalState(userInput, sessionHistory);
    const consentLevel = this.consentManager.determineLevel(emotionalState);
    // Get continuity context, keyed by the stable user identifier. Passing
    // `userInput` here (the previous behavior on the Python side) keyed
    // continuity on the message text, so it always reported "no history".
    const continuityContext = this.continuityManager.getContext(userId || this.userId);
    return {
      emotionalState,
      consentLevel,
      continuityContext,
      swpActive: this.userToi.swp?.active !== false,
      protectiveStateActive: emotionalState.protective,
    };
  }

  /**
   * Preserves emotional boundaries across sessions. Mirrors Python
   * `maintain_continuity`: the read (`assessInteraction`) and the write
   * (`maintainContinuity`) stay separate so that assessment never implicitly
   * writes to disk.
   */
  maintainContinuity(userId: string, sessionData: any): void {
    this.continuityManager.saveSession(userId, sessionData);
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
