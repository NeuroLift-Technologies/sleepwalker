/**
 * Temporal Continuity Management Module
 */

import * as fs from 'fs';
import * as path from 'path';

export class ContinuityManager {
  private storagePath: string;

  constructor(storagePath: string = '.swp_storage') {
    this.storagePath = storagePath;
    if (!fs.existsSync(this.storagePath)) {
      fs.mkdirSync(this.storagePath, { recursive: true });
    }
  }

  saveSession(userId: string, sessionData: any): void {
    const userFile = path.join(this.storagePath, `${userId}.json`);
    const existingData = this.loadUserData(userId);
    sessionData.timestamp = new Date().toISOString();
    existingData.lastSession = sessionData;
    existingData.sessionCount = (existingData.sessionCount || 0) + 1;
    fs.writeFileSync(userFile, JSON.stringify(existingData, null, 2));
  }

  getContext(userId: string): any {
    const userData = this.loadUserData(userId);
    if (Object.keys(userData).length === 0) {
      return { hasHistory: false, protectiveStateActive: false };
    }
    return {
      hasHistory: true,
      lastSessionState: userData.lastSession?.emotionalState || 'unknown',
      protectiveStateActive: userData.lastSession?.protectiveStateActive || false,
    };
  }

  private loadUserData(userId: string): any {
    const userFile = path.join(this.storagePath, `${userId}.json`);
    if (!fs.existsSync(userFile)) return {};
    try {
      return JSON.parse(fs.readFileSync(userFile, 'utf-8'));
    } catch {
      return {};
    }
  }
}
