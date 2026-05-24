
import { TechnicalDepth, TechnicalProfile } from './types';

export const DEFAULT_PROFILE: TechnicalProfile = {
  depth: TechnicalDepth.ENGINEER,
  focusAreas: ['LLM Architectures', 'Edge AI', 'RAG Optimizations'],
  digestInterval: '24h',
  notificationEnabled: true,
};

export const APP_STORAGE_KEY = 'nexus_ai_state';

export const CATEGORIES = [
  'LLM Architectures',
  'Multimodal Models',
  'Robotics',
  'AI Policy & Ethics',
  'Compute & Infrastructure',
  'Open Source Releases',
  'Enterprise AI',
  'Agentic Frameworks'
];
