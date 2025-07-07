import { User, MatchCandidate, SwipeAction, GAParameters } from '../types';
import { database } from './database';

export class GeneticMatchingEngine {
  private swipeHistory: SwipeAction[] = [];
  private parameters: GAParameters = {
    populationSize: 50,
    mutationRate: 0.1,
    crossoverRate: 0.8,
    generations: 10,
    elitismRate: 0.2
  };

  constructor(parameters?: Partial<GAParameters>) {
    if (parameters) {
      this.parameters = { ...this.parameters, ...parameters };
    }
  }

  async loadSwipeHistory(userId: string): Promise<void> {
    this.swipeHistory = await database.getUserSwipes(userId);
  }

  // Calculate compatibility between two users
  calculateCompatibility(user1: User, user2: User): number {
    const personalityScore = this.calculatePersonalityCompatibility(user1, user2);
    const interestScore = this.calculateInterestCompatibility(user1, user2);
    const ageScore = this.calculateAgeCompatibility(user1, user2);
    const genderScore = this.calculateGenderCompatibility(user1, user2);
    
    // Weighted combination based on user preferences
    const personalityWeight = (user1.preferences.personalityImportance || 50) / 100;
    const interestWeight = (user1.preferences.interestImportance || 50) / 100;
    const ageWeight = 0.2;
    const genderWeight = 0.3;
    
    const totalWeight = personalityWeight + interestWeight + ageWeight + genderWeight;
    
    return (
      (personalityScore * personalityWeight + 
       interestScore * interestWeight + 
       ageScore * ageWeight +
       genderScore * genderWeight) / totalWeight
    );
  }

  private calculatePersonalityCompatibility(user1: User, user2: User): number {
    const traits = ['extroversion', 'openness', 'conscientiousness', 'agreeableness', 'neuroticism'] as const;
    let totalScore = 0;
    
    traits.forEach(trait => {
      const diff = Math.abs(user1.personality[trait] - user2.personality[trait]);
      // For some traits, similarity is good, for others, complementarity might be better
      let score;
      if (trait === 'neuroticism') {
        // Lower neuroticism difference is better
        score = Math.max(0, 100 - diff);
      } else if (trait === 'extroversion') {
        // Some complementarity can be good
        score = Math.max(0, 100 - diff * 0.7);
      } else {
        // Generally, similarity is good
        score = Math.max(0, 100 - diff);
      }
      totalScore += score;
    });
    
    return totalScore / traits.length;
  }

  private calculateInterestCompatibility(user1: User, user2: User): number {
    const commonInterests = user1.interests.filter(interest => 
      user2.interests.includes(interest)
    );
    
    if (user1.interests.length === 0 && user2.interests.length === 0) return 50;
    
    const totalUniqueInterests = new Set([...user1.interests, ...user2.interests]).size;
    const commonRatio = commonInterests.length / Math.max(user1.interests.length, user2.interests.length);
    const diversityBonus = Math.min(20, totalUniqueInterests * 2); // Bonus for having diverse interests
    
    return Math.min(100, (commonRatio * 80) + diversityBonus);
  }

  private calculateAgeCompatibility(user1: User, user2: User): number {
    const [minAge, maxAge] = user1.preferences.ageRange;
    if (user2.age >= minAge && user2.age <= maxAge) {
      const midPoint = (minAge + maxAge) / 2;
      const distance = Math.abs(user2.age - midPoint);
      const maxDistance = (maxAge - minAge) / 2;
      return Math.max(60, 100 - (distance / Math.max(1, maxDistance)) * 40);
    }
    
    // Penalty for being outside preferred range, but not complete elimination
    const distanceFromRange = Math.min(
      Math.abs(user2.age - minAge),
      Math.abs(user2.age - maxAge)
    );
    return Math.max(0, 60 - distanceFromRange * 5);
  }

  private calculateGenderCompatibility(user1: User, user2: User): number {
    if (user1.preferences.genderPreference === 'both') return 100;
    if (user1.preferences.genderPreference === user2.gender) return 100;
    return 0; // This should be filtered out in database query, but just in case
  }

  // Record user swipe action for learning
  async recordSwipe(swipe: Omit<SwipeAction, 'id'>): Promise<void> {
    const savedSwipe = await database.recordSwipe(swipe);
    this.swipeHistory.push(savedSwipe);
    this.adaptParameters();
  }

  // Adapt algorithm parameters based on user feedback
  private adaptParameters(): void {
    if (this.swipeHistory.length < 10) return;
    
    const recentSwipes = this.swipeHistory.slice(-20);
    const likeRatio = recentSwipes.filter(s => s.action === 'like').length / recentSwipes.length;
    const averageCompatibility = recentSwipes.reduce((sum, s) => sum + s.compatibility, 0) / recentSwipes.length;
    
    // Adjust mutation rate based on user satisfaction
    if (likeRatio < 0.3) {
      this.parameters.mutationRate = Math.min(0.3, this.parameters.mutationRate * 1.1);
    } else if (likeRatio > 0.7) {
      this.parameters.mutationRate = Math.max(0.05, this.parameters.mutationRate * 0.9);
    }
    
    // Adjust population size based on compatibility scores
    if (averageCompatibility < 60) {
      this.parameters.populationSize = Math.min(100, this.parameters.populationSize + 5);
    }
  }

  // Generate optimized matches using genetic algorithm
  async generateMatches(currentUser: User): Promise<MatchCandidate[]> {
    const candidateUsers = await database.getPotentialMatches(currentUser);
    
    if (candidateUsers.length === 0) {
      return [];
    }
    
    let population = this.initializePopulation(currentUser, candidateUsers);
    
    // Apply genetic algorithm evolution
    for (let generation = 0; generation < this.parameters.generations; generation++) {
      population = this.evolvePopulation(population, currentUser);
    }
    
    // Filter out users already swiped on
    const swipedUserIds = new Set(this.swipeHistory.map(s => s.targetUserId));
    const unswipedMatches = population.filter(match => !swipedUserIds.has(match.user.id));
    
    return unswipedMatches
      .sort((a, b) => b.compatibility - a.compatibility)
      .slice(0, 10);
  }

  private initializePopulation(currentUser: User, candidates: User[]): MatchCandidate[] {
    return candidates.map(candidate => {
      const compatibility = this.calculateCompatibility(currentUser, candidate);
      const commonInterests = currentUser.interests.filter(interest => 
        candidate.interests.includes(interest)
      );
      
      return {
        user: candidate,
        compatibility,
        commonInterests,
        personalityMatch: this.calculatePersonalityCompatibility(currentUser, candidate),
        distance: this.calculateDistance(currentUser.location, candidate.location)
      };
    });
  }

  private calculateDistance(location1: string, location2: string): number {
    // Simplified distance calculation based on city names
    const cityDistances: Record<string, Record<string, number>> = {
      'Jakarta, Indonesia': {
        'Jakarta, Indonesia': 0,
        'Bandung, Indonesia': 150,
        'Yogyakarta, Indonesia': 430,
        'Surabaya, Indonesia': 660
      },
      'Bandung, Indonesia': {
        'Jakarta, Indonesia': 150,
        'Bandung, Indonesia': 0,
        'Yogyakarta, Indonesia': 350,
        'Surabaya, Indonesia': 520
      },
      'Yogyakarta, Indonesia': {
        'Jakarta, Indonesia': 430,
        'Bandung, Indonesia': 350,
        'Yogyakarta, Indonesia': 0,
        'Surabaya, Indonesia': 320
      },
      'Surabaya, Indonesia': {
        'Jakarta, Indonesia': 660,
        'Bandung, Indonesia': 520,
        'Yogyakarta, Indonesia': 320,
        'Surabaya, Indonesia': 0
      }
    };

    return cityDistances[location1]?.[location2] || Math.random() * 100;
  }

  private evolvePopulation(population: MatchCandidate[], currentUser: User): MatchCandidate[] {
    const sorted = population.sort((a, b) => b.compatibility - a.compatibility);
    const eliteSize = Math.floor(population.length * this.parameters.elitismRate);
    const elite = sorted.slice(0, eliteSize);
    
    const newPopulation = [...elite];
    
    while (newPopulation.length < population.length) {
      const parent1 = this.tournamentSelection(sorted);
      const parent2 = this.tournamentSelection(sorted);
      
      if (Math.random() < this.parameters.crossoverRate) {
        const offspring = this.crossover(parent1, parent2, currentUser);
        if (Math.random() < this.parameters.mutationRate) {
          this.mutate(offspring);
        }
        newPopulation.push(offspring);
      } else {
        newPopulation.push(parent1);
      }
    }
    
    return newPopulation.slice(0, population.length);
  }

  private tournamentSelection(population: MatchCandidate[]): MatchCandidate {
    const tournamentSize = 3;
    const tournament = [];
    
    for (let i = 0; i < tournamentSize; i++) {
      const randomIndex = Math.floor(Math.random() * population.length);
      tournament.push(population[randomIndex]);
    }
    
    return tournament.sort((a, b) => b.compatibility - a.compatibility)[0];
  }

  private crossover(parent1: MatchCandidate, parent2: MatchCandidate, currentUser: User): MatchCandidate {
    // Create a hybrid user profile
    const hybridUser: User = {
      ...parent1.user,
      interests: [
        ...parent1.user.interests.slice(0, Math.floor(parent1.user.interests.length / 2)),
        ...parent2.user.interests.slice(Math.floor(parent2.user.interests.length / 2))
      ],
      personality: {
        extroversion: (parent1.user.personality.extroversion + parent2.user.personality.extroversion) / 2,
        openness: (parent1.user.personality.openness + parent2.user.personality.openness) / 2,
        conscientiousness: (parent1.user.personality.conscientiousness + parent2.user.personality.conscientiousness) / 2,
        agreeableness: (parent1.user.personality.agreeableness + parent2.user.personality.agreeableness) / 2,
        neuroticism: (parent1.user.personality.neuroticism + parent2.user.personality.neuroticism) / 2
      }
    };
    
    return {
      user: hybridUser,
      compatibility: this.calculateCompatibility(currentUser, hybridUser),
      commonInterests: currentUser.interests.filter(interest => 
        hybridUser.interests.includes(interest)
      ),
      personalityMatch: this.calculatePersonalityCompatibility(currentUser, hybridUser),
      distance: (parent1.distance + parent2.distance) / 2
    };
  }

  private mutate(candidate: MatchCandidate): void {
    // Randomly adjust personality traits
    const traits = Object.keys(candidate.user.personality) as (keyof typeof candidate.user.personality)[];
    const traitToMutate = traits[Math.floor(Math.random() * traits.length)];
    
    const mutation = (Math.random() - 0.5) * 20; // +/- 10 point mutation
    candidate.user.personality[traitToMutate] = Math.max(0, Math.min(100, 
      candidate.user.personality[traitToMutate] + mutation
    ));
    
    // Occasionally add/remove interests
    if (Math.random() < 0.3) {
      const allInterests = ['Reading', 'Travel', 'Music', 'Sports', 'Art', 'Technology', 'Food', 'Movies', 'Photography', 'Cooking', 'Gaming', 'Yoga', 'Dancing', 'Hiking'];
      const availableInterests = allInterests.filter(interest => !candidate.user.interests.includes(interest));
      
      if (availableInterests.length > 0 && Math.random() < 0.5) {
        const newInterest = availableInterests[Math.floor(Math.random() * availableInterests.length)];
        candidate.user.interests.push(newInterest);
      } else if (candidate.user.interests.length > 1) {
        const indexToRemove = Math.floor(Math.random() * candidate.user.interests.length);
        candidate.user.interests.splice(indexToRemove, 1);
      }
    }
  }

  getSwipeHistory(): SwipeAction[] {
    return this.swipeHistory;
  }

  getParameters(): GAParameters {
    return this.parameters;
  }

  updateParameters(newParameters: Partial<GAParameters>): void {
    this.parameters = { ...this.parameters, ...newParameters };
  }
}