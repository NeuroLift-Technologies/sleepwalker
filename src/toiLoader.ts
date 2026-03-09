/**
 * TOI Loader Module
 */

import * as fs from 'fs';
import * as yaml from 'js-yaml';

export class TOILoader {
  private toiPath?: string;

  constructor(toiPath?: string) {
    this.toiPath = toiPath;
  }

  load(): any {
    if (!this.toiPath || !fs.existsSync(this.toiPath)) {
      return this.getDefaultToi();
    }
    try {
      const content = fs.readFileSync(this.toiPath, 'utf-8');
      if (this.toiPath.endsWith('.json')) {
        return JSON.parse(content);
      }
      return yaml.load(content) || this.getDefaultToi();
    } catch {
      return this.getDefaultToi();
    }
  }

  private getDefaultToi(): any {
    return {
      swp: {
        active: true,
        intervention_threshold: 'user_initiated_only',
        processing_consent: false,
        protected_topics: [],
      },
    };
  }
}
