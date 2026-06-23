/**
 * Temporal Continuity Management Module
 *
 * Maintains emotional state and boundary awareness across sessions.
 */

import * as crypto from 'crypto';
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

  /**
   * Resolve the storage file for a user — traversal-safe and collision-safe.
   *
   * `userId` becomes part of a filename, which raises two risks:
   *
   * - **Path traversal.** A raw value like `"../../etc/passwd"` must not read or
   *   write outside `storagePath`.
   * - **Collisions.** Simply stripping disallowed characters would map distinct
   *   ids onto the same file (`"a/b"` and `"ab"`, or `"alice@example.com"` and
   *   `"aliceexample.com"`), letting one user's continuity overwrite or leak
   *   into another's.
   *
   * We therefore key the file on a SHA-256 of the *full* id — deterministic,
   * collision-resistant, and filesystem-safe (hex only) — prefixed with a
   * sanitized, human-readable slug purely for debuggability. Mirrors the Python
   * `ContinuityManager._user_file`.
   */
  private userFile(userId: string): string {
    const raw = String(userId);
    const slug = (raw.match(/[A-Za-z0-9_-]/g) || []).join('').slice(0, 32) || 'user';
    // Full SHA-256 hex (the filename is the user-isolation boundary; the extra
    // length is free and maximizes separation between users).
    const digest = crypto.createHash('sha256').update(raw, 'utf-8').digest('hex');
    return path.join(this.storagePath, `${slug}-${digest}.json`);
  }

  saveSession(userId: string, sessionData: any): void {
    const userFile = this.userFile(userId);
    const existingData = this.loadUserData(userId);
    sessionData.timestamp = new Date().toISOString();
    existingData.lastSession = sessionData;
    existingData.sessionCount = (existingData.sessionCount || 0) + 1;
    // Preserve declared boundaries across sessions.
    if (sessionData.declaredBoundaries !== undefined) {
      existingData.declaredBoundaries = sessionData.declaredBoundaries;
    }
    fs.writeFileSync(userFile, JSON.stringify(existingData, null, 2));
  }

  getContext(userId: string): any {
    const userData = this.loadUserData(userId);
    if (Object.keys(userData).length === 0) {
      return { hasHistory: false, protectiveStateActive: false, declaredBoundaries: [] };
    }
    return {
      hasHistory: true,
      lastSessionState: userData.lastSession?.emotionalState || 'unknown',
      protectiveStateActive: userData.lastSession?.protectiveStateActive || false,
      declaredBoundaries: userData.declaredBoundaries || [],
      sessionCount: userData.sessionCount || 0,
    };
  }

  private loadUserData(userId: string): any {
    const userFile = this.userFile(userId);
    if (!fs.existsSync(userFile)) return {};
    try {
      return JSON.parse(fs.readFileSync(userFile, 'utf-8'));
    } catch {
      return {};
    }
  }
}
