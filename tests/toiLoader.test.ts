import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { TOILoader } from '../src/toiLoader';

describe('TOILoader', () => {
  let dir: string;

  beforeEach(() => {
    dir = fs.mkdtempSync(path.join(os.tmpdir(), 'swp-toi-'));
  });

  afterEach(() => {
    fs.rmSync(dir, { recursive: true, force: true });
  });

  it('returns the default TOI when no path is given', () => {
    const toi = new TOILoader().load();
    expect(toi.swp.active).toBe(true);
    expect(toi.swp.intervention_threshold).toBe('user_initiated_only');
  });

  it('returns the default TOI for a non-existent path', () => {
    const toi = new TOILoader(path.join(dir, 'non-existent.yaml')).load();
    expect(toi.swp.active).toBe(true);
  });

  it('loads a JSON TOI document', () => {
    const file = path.join(dir, 'toi.json');
    fs.writeFileSync(file, JSON.stringify({ swp: { active: false } }));
    const toi = new TOILoader(file).load();
    expect(toi.swp.active).toBe(false);
  });

  it('loads a YAML TOI document', () => {
    const file = path.join(dir, 'toi.yaml');
    fs.writeFileSync(
      file,
      'swp:\n  active: true\n  intervention_threshold: offer_support_without_pressure\n',
    );
    const toi = new TOILoader(file).load();
    expect(toi.swp.intervention_threshold).toBe('offer_support_without_pressure');
  });
});
