
export enum TechnicalDepth {
  HOBBYIST = 'Hobbyist',
  ENGINEER = 'Software Engineer',
  RESEARCHER = 'ML Researcher',
  EXECUTIVE = 'Strategic Executive'
}

export interface TechnicalProfile {
  depth: TechnicalDepth;
  focusAreas: string[];
  digestInterval: '4h' | '12h' | '24h';
  notificationEnabled: boolean;
}

export interface GroundingSource {
  title: string;
  uri: string;
}

export interface DigestItem {
  id: string;
  timestamp: number;
  title: string;
  summary: string;
  keyTakeaways: string[];
  technicalAnalysis: string;
  sources: GroundingSource[];
  impactScore: number; // 1-10
}

export interface PipelineState {
  isProcessing: boolean;
  lastRun: number | null;
  history: DigestItem[];
  profile: TechnicalProfile;
}
