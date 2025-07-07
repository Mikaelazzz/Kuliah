import { User } from '../types';

export const sampleUsers: User[] = [
  {
    id: '1',
    name: 'Emma Watson',
    age: 28,
    bio: 'Book lover, adventurer, and coffee enthusiast. Looking for someone who shares my passion for learning and exploring new places.',
    interests: ['Reading', 'Travel', 'Coffee', 'Hiking', 'Photography', 'Movies'],
    personality: {
      extroversion: 75,
      openness: 85,
      conscientiousness: 80,
      agreeableness: 90,
      neuroticism: 25
    },
    preferences: {
      ageRange: [25, 35],
      maxDistance: 50,
      interests: ['Travel', 'Reading', 'Outdoor Activities'],
      personalityImportance: 70,
      interestImportance: 60
    },
    photo: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'San Francisco, CA'
  },
  {
    id: '2',
    name: 'James Rodriguez',
    age: 30,
    bio: 'Software engineer by day, musician by night. Love creating things and exploring the intersection of technology and art.',
    interests: ['Programming', 'Music', 'Guitar', 'Gaming', 'Cooking', 'Tech'],
    personality: {
      extroversion: 60,
      openness: 90,
      conscientiousness: 85,
      agreeableness: 75,
      neuroticism: 30
    },
    preferences: {
      ageRange: [24, 32],
      maxDistance: 30,
      interests: ['Music', 'Technology', 'Creative Arts'],
      personalityImportance: 65,
      interestImportance: 75
    },
    photo: 'https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'San Francisco, CA'
  },
  {
    id: '3',
    name: 'Sofia Chen',
    age: 26,
    bio: 'Yoga instructor and wellness coach. Passionate about mindfulness, healthy living, and connecting with nature.',
    interests: ['Yoga', 'Meditation', 'Health', 'Nature', 'Cooking', 'Dancing'],
    personality: {
      extroversion: 70,
      openness: 80,
      conscientiousness: 75,
      agreeableness: 85,
      neuroticism: 20
    },
    preferences: {
      ageRange: [24, 34],
      maxDistance: 40,
      interests: ['Wellness', 'Outdoor Activities', 'Mindfulness'],
      personalityImportance: 80,
      interestImportance: 55
    },
    photo: 'https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'San Francisco, CA'
  },
  {
    id: '4',
    name: 'Michael Thompson',
    age: 32,
    bio: 'Adventure seeker and outdoor enthusiast. Weekend warrior who loves rock climbing, surfing, and exploring new trails.',
    interests: ['Rock Climbing', 'Surfing', 'Hiking', 'Photography', 'Travel', 'Fitness'],
    personality: {
      extroversion: 85,
      openness: 90,
      conscientiousness: 70,
      agreeableness: 80,
      neuroticism: 15
    },
    preferences: {
      ageRange: [25, 35],
      maxDistance: 60,
      interests: ['Adventure Sports', 'Outdoor Activities', 'Travel'],
      personalityImportance: 60,
      interestImportance: 80
    },
    photo: 'https://images.pexels.com/photos/1043471/pexels-photo-1043471.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'San Francisco, CA'
  },
  {
    id: '5',
    name: 'Isabella Martinez',
    age: 24,
    bio: 'Art student and creative soul. Love painting, gallery hopping, and finding beauty in everyday moments.',
    interests: ['Art', 'Painting', 'Museums', 'Photography', 'Wine', 'Culture'],
    personality: {
      extroversion: 65,
      openness: 95,
      conscientiousness: 70,
      agreeableness: 80,
      neuroticism: 35
    },
    preferences: {
      ageRange: [22, 30],
      maxDistance: 35,
      interests: ['Art', 'Culture', 'Creative Activities'],
      personalityImportance: 75,
      interestImportance: 70
    },
    photo: 'https://images.pexels.com/photos/1130626/pexels-photo-1130626.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'San Francisco, CA'
  },
  {
    id: '6',
    name: 'David Kim',
    age: 29,
    bio: 'Foodie and travel enthusiast. Always looking for the next great restaurant or planning the next adventure.',
    interests: ['Food', 'Travel', 'Culture', 'Languages', 'Photography', 'Wine'],
    personality: {
      extroversion: 80,
      openness: 85,
      conscientiousness: 75,
      agreeableness: 85,
      neuroticism: 25
    },
    preferences: {
      ageRange: [24, 34],
      maxDistance: 45,
      interests: ['Food', 'Travel', 'Cultural Experiences'],
      personalityImportance: 70,
      interestImportance: 65
    },
    photo: 'https://images.pexels.com/photos/1516680/pexels-photo-1516680.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'San Francisco, CA'
  }
];