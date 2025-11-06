export interface Asana {
  id: number;
  name: string;
  image: string;
  sanskritName?: string;
}

export interface Routine {
  id: number;
  name: string;
  description: string;
  asanas: Asana[];
  difficulty: 'beginner' | 'intermediate' | 'advanced';
}

export enum DetectionStatus {
  INITIALIZING = 'initializing',
  NO_POSE = 'no_pose',
  INCORRECT = 'incorrect',
  CORRECT = 'correct',
  PARTIAL = 'partial'
}

export interface DetectionResult {
  status: DetectionStatus;
  message: string;
  confidence?: number;
}
