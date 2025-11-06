export enum DetectionStatus {
  INITIALIZING = 'initializing',
  NO_POSE = 'no_pose',
  INCORRECT = 'incorrect',
  CORRECT = 'correct',
  PARTIAL = 'partial',
  NEXT_POSE = 'next_pose',
  SEQUENCE_COMPLETE = 'sequence_complete'
}

export interface DetectionResult {
  status: DetectionStatus;
  message: string;
  confidence?: number;
  pose_name?: string;
}

export interface Asana {
  id: number;
  name: string;
  sanskritName: string;
  image: string;
}

export interface Routine {
  id: string;
  name: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  asanas: Asana[];
}
