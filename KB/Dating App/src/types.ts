export interface User {
  id: string;
  name: string;
  email: string;
  phone: string;
  phoneVerified: boolean;
  gender: 'male' | 'female' | 'other';
  age: number;
  bio: string;
  interests: string[];
  personality: PersonalityTraits;
  preferences: Preferences;
  photo: string;
  location: string;
  createdAt: Date;
}

export interface PersonalityTraits {
  extroversion: number; // 0-100
  openness: number; // 0-100
  conscientiousness: number; // 0-100
  agreeableness: number; // 0-100
  neuroticism: number; // 0-100
}

export interface Preferences {
  ageRange: [number, number];
  maxDistance: number;
  genderPreference: 'male' | 'female' | 'both';
  interests: string[];
  personalityImportance: number; // 0-100
  interestImportance: number; // 0-100
}

export interface MatchCandidate {
  user: User;
  compatibility: number;
  commonInterests: string[];
  personalityMatch: number;
  distance: number;
}

export interface SwipeAction {
  id?: string;
  userId: string;
  targetUserId: string;
  action: 'like' | 'dislike';
  compatibility: number;
  timestamp: Date;
}

export interface GAParameters {
  populationSize: number;
  mutationRate: number;
  crossoverRate: number;
  generations: number;
  elitismRate: number;
}

export interface AuthUser {
  id: string;
  email: string;
  name: string;
  isAuthenticated: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  phone: string;
  gender: 'male' | 'female' | 'other';
  genderPreference: 'male' | 'female' | 'both';
  password: string;
  confirmPassword: string;
  age: number;
  location: string;
}

export interface OTPVerification {
  phone: string;
  code: string;
  expiresAt: Date;
  verified: boolean;
}