import { User, SwipeAction } from '../types';

// Sample users with diverse profiles for better matching
const sampleUsers = [
  {
    name: 'Sari Dewi',
    email: 'sari.dewi@example.com',
    phone: '+6281234567890',
    phoneVerified: true,
    gender: 'female' as const,
    age: 26,
    bio: 'Pecinta kopi dan buku. Suka traveling dan fotografi. Mencari seseorang yang bisa diajak diskusi tentang hal-hal menarik.',
    interests: ['Reading', 'Coffee', 'Photography', 'Travel', 'Movies', 'Art'],
    personality: {
      extroversion: 70,
      openness: 85,
      conscientiousness: 80,
      agreeableness: 90,
      neuroticism: 25
    },
    preferences: {
      ageRange: [24, 32] as [number, number],
      maxDistance: 50,
      genderPreference: 'male' as const,
      interests: ['Travel', 'Reading', 'Coffee'],
      personalityImportance: 70,
      interestImportance: 60
    },
    photo: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'Jakarta, Indonesia'
  },
  {
    name: 'Budi Santoso',
    email: 'budi.santoso@example.com',
    phone: '+6281234567891',
    phoneVerified: true,
    gender: 'male' as const,
    age: 28,
    bio: 'Software engineer yang suka musik dan olahraga. Weekend biasanya main futsal atau nonton konser. Cari yang bisa jadi partner hidup.',
    interests: ['Programming', 'Music', 'Football', 'Gaming', 'Technology', 'Cooking'],
    personality: {
      extroversion: 65,
      openness: 80,
      conscientiousness: 85,
      agreeableness: 75,
      neuroticism: 30
    },
    preferences: {
      ageRange: [22, 30] as [number, number],
      maxDistance: 40,
      genderPreference: 'female' as const,
      interests: ['Music', 'Technology', 'Sports'],
      personalityImportance: 65,
      interestImportance: 75
    },
    photo: 'https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'Jakarta, Indonesia'
  },
  {
    name: 'Maya Putri',
    email: 'maya.putri@example.com',
    phone: '+6281234567892',
    phoneVerified: true,
    gender: 'female' as const,
    age: 24,
    bio: 'Yoga instructor dan food blogger. Passionate tentang healthy lifestyle dan mindfulness. Suka masak dan explore tempat makan baru.',
    interests: ['Yoga', 'Cooking', 'Health', 'Food', 'Meditation', 'Nature'],
    personality: {
      extroversion: 75,
      openness: 90,
      conscientiousness: 70,
      agreeableness: 85,
      neuroticism: 20
    },
    preferences: {
      ageRange: [25, 35] as [number, number],
      maxDistance: 35,
      genderPreference: 'male' as const,
      interests: ['Health', 'Food', 'Nature'],
      personalityImportance: 80,
      interestImportance: 55
    },
    photo: 'https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'Bandung, Indonesia'
  },
  {
    name: 'Andi Rahman',
    email: 'andi.rahman@example.com',
    phone: '+6281234567893',
    phoneVerified: true,
    gender: 'male' as const,
    age: 30,
    bio: 'Adventure seeker dan outdoor enthusiast. Suka hiking, diving, dan explore alam Indonesia. Cari partner yang sama-sama suka petualangan.',
    interests: ['Hiking', 'Diving', 'Photography', 'Travel', 'Adventure', 'Nature'],
    personality: {
      extroversion: 85,
      openness: 95,
      conscientiousness: 70,
      agreeableness: 80,
      neuroticism: 15
    },
    preferences: {
      ageRange: [24, 32] as [number, number],
      maxDistance: 60,
      genderPreference: 'female' as const,
      interests: ['Adventure', 'Travel', 'Nature'],
      personalityImportance: 60,
      interestImportance: 80
    },
    photo: 'https://images.pexels.com/photos/1043471/pexels-photo-1043471.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'Yogyakarta, Indonesia'
  },
  {
    name: 'Rina Sari',
    email: 'rina.sari@example.com',
    phone: '+6281234567894',
    phoneVerified: true,
    gender: 'female' as const,
    age: 27,
    bio: 'Graphic designer dan art enthusiast. Suka ke gallery, nonton film indie, dan ngopi sambil sketching. Cari yang bisa appreciate seni.',
    interests: ['Art', 'Design', 'Movies', 'Coffee', 'Photography', 'Culture'],
    personality: {
      extroversion: 60,
      openness: 95,
      conscientiousness: 75,
      agreeableness: 80,
      neuroticism: 35
    },
    preferences: {
      ageRange: [25, 33] as [number, number],
      maxDistance: 45,
      genderPreference: 'male' as const,
      interests: ['Art', 'Culture', 'Movies'],
      personalityImportance: 75,
      interestImportance: 70
    },
    photo: 'https://images.pexels.com/photos/1130626/pexels-photo-1130626.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'Jakarta, Indonesia'
  },
  {
    name: 'Dimas Pratama',
    email: 'dimas.pratama@example.com',
    phone: '+6281234567895',
    phoneVerified: true,
    gender: 'male' as const,
    age: 29,
    bio: 'Entrepreneur di bidang F&B. Foodie sejati yang suka explore kuliner nusantara. Weekend biasanya hunting makanan atau masak eksperimen.',
    interests: ['Food', 'Business', 'Cooking', 'Travel', 'Culture', 'Music'],
    personality: {
      extroversion: 80,
      openness: 85,
      conscientiousness: 80,
      agreeableness: 85,
      neuroticism: 25
    },
    preferences: {
      ageRange: [23, 31] as [number, number],
      maxDistance: 50,
      genderPreference: 'female' as const,
      interests: ['Food', 'Travel', 'Culture'],
      personalityImportance: 70,
      interestImportance: 65
    },
    photo: 'https://images.pexels.com/photos/1516680/pexels-photo-1516680.jpeg?auto=compress&cs=tinysrgb&w=400',
    location: 'Surabaya, Indonesia'
  }
];

// Simulated database using localStorage for WebContainer compatibility
class DatabaseManager {
  private dbName = 'lovega_db';

  constructor() {
    this.initializeDatabase();
  }

  private initializeDatabase(): void {
    try {
      if (!localStorage.getItem(`${this.dbName}_users`)) {
        // Initialize with sample users
        const usersWithIds = sampleUsers.map(user => ({
          ...user,
          id: this.generateId(),
          createdAt: new Date()
        }));
        localStorage.setItem(`${this.dbName}_users`, JSON.stringify(usersWithIds));
        console.log('Database initialized with sample users');
      }
      if (!localStorage.getItem(`${this.dbName}_swipes`)) {
        localStorage.setItem(`${this.dbName}_swipes`, JSON.stringify([]));
      }
      if (!localStorage.getItem(`${this.dbName}_sessions`)) {
        localStorage.setItem(`${this.dbName}_sessions`, JSON.stringify({}));
      }
    } catch (error) {
      console.error('Failed to initialize database:', error);
    }
  }

  // User management
  async createUser(userData: Omit<User, 'id' | 'createdAt'>): Promise<User> {
    try {
      console.log('Creating user with data:', userData);
      
      const users = this.getUsers();
      const newUser: User = {
        ...userData,
        id: this.generateId(),
        createdAt: new Date()
      };
      
      console.log('Generated new user:', newUser);
      
      users.push(newUser);
      localStorage.setItem(`${this.dbName}_users`, JSON.stringify(users));
      
      console.log('User saved to localStorage');
      return newUser;
    } catch (error) {
      console.error('Error creating user:', error);
      throw new Error('Failed to create user');
    }
  }

  async getUserById(id: string): Promise<User | null> {
    try {
      const users = this.getUsers();
      return users.find(user => user.id === id) || null;
    } catch (error) {
      console.error('Error getting user by ID:', error);
      return null;
    }
  }

  async getUserByEmail(email: string): Promise<User | null> {
    try {
      const users = this.getUsers();
      const normalizedEmail = email.toLowerCase().trim();
      return users.find(user => user.email.toLowerCase().trim() === normalizedEmail) || null;
    } catch (error) {
      console.error('Error getting user by email:', error);
      return null;
    }
  }

  async getUserByPhone(phone: string): Promise<User | null> {
    try {
      const users = this.getUsers();
      const cleanPhone = phone.replace(/\D/g, '');
      return users.find(user => {
        const userPhone = user.phone.replace(/\D/g, '');
        return userPhone === cleanPhone;
      }) || null;
    } catch (error) {
      console.error('Error getting user by phone:', error);
      return null;
    }
  }

  async updateUser(id: string, updates: Partial<User>): Promise<User | null> {
    try {
      const users = this.getUsers();
      const userIndex = users.findIndex(user => user.id === id);
      
      if (userIndex === -1) return null;
      
      users[userIndex] = { ...users[userIndex], ...updates };
      localStorage.setItem(`${this.dbName}_users`, JSON.stringify(users));
      return users[userIndex];
    } catch (error) {
      console.error('Error updating user:', error);
      return null;
    }
  }

  async getAllUsers(): Promise<User[]> {
    return this.getUsers();
  }

  // Get potential matches based on preferences
  async getPotentialMatches(currentUser: User): Promise<User[]> {
    try {
      const allUsers = this.getUsers();
      
      return allUsers.filter(user => {
        // Exclude self
        if (user.id === currentUser.id) return false;
        
        // Check gender preference
        if (currentUser.preferences.genderPreference !== 'both' && 
            user.gender !== currentUser.preferences.genderPreference) {
          return false;
        }
        
        // Check age range
        const [minAge, maxAge] = currentUser.preferences.ageRange;
        if (user.age < minAge || user.age > maxAge) {
          return false;
        }
        
        // Check if user is verified
        if (!user.phoneVerified) {
          return false;
        }
        
        return true;
      });
    } catch (error) {
      console.error('Error getting potential matches:', error);
      return [];
    }
  }

  // Swipe actions
  async recordSwipe(swipe: Omit<SwipeAction, 'id'>): Promise<SwipeAction> {
    try {
      const swipes = this.getSwipes();
      const newSwipe: SwipeAction = {
        ...swipe,
        id: this.generateId()
      };
      
      swipes.push(newSwipe);
      localStorage.setItem(`${this.dbName}_swipes`, JSON.stringify(swipes));
      return newSwipe;
    } catch (error) {
      console.error('Error recording swipe:', error);
      throw new Error('Failed to record swipe');
    }
  }

  async getUserSwipes(userId: string): Promise<SwipeAction[]> {
    try {
      const swipes = this.getSwipes();
      return swipes.filter(swipe => swipe.userId === userId);
    } catch (error) {
      console.error('Error getting user swipes:', error);
      return [];
    }
  }

  // Session management
  async createSession(userId: string): Promise<string> {
    try {
      const sessionId = this.generateId();
      const sessions = this.getSessions();
      sessions[sessionId] = {
        userId,
        createdAt: new Date().toISOString(),
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours
      };
      
      localStorage.setItem(`${this.dbName}_sessions`, JSON.stringify(sessions));
      return sessionId;
    } catch (error) {
      console.error('Error creating session:', error);
      throw new Error('Failed to create session');
    }
  }

  async validateSession(sessionId: string): Promise<string | null> {
    try {
      const sessions = this.getSessions();
      const session = sessions[sessionId];
      
      if (!session) return null;
      
      const now = new Date();
      const expiresAt = new Date(session.expiresAt);
      
      if (now > expiresAt) {
        delete sessions[sessionId];
        localStorage.setItem(`${this.dbName}_sessions`, JSON.stringify(sessions));
        return null;
      }
      
      return session.userId;
    } catch (error) {
      console.error('Error validating session:', error);
      return null;
    }
  }

  async deleteSession(sessionId: string): Promise<void> {
    try {
      const sessions = this.getSessions();
      delete sessions[sessionId];
      localStorage.setItem(`${this.dbName}_sessions`, JSON.stringify(sessions));
    } catch (error) {
      console.error('Error deleting session:', error);
    }
  }

  // Helper methods
  private getUsers(): User[] {
    try {
      const data = localStorage.getItem(`${this.dbName}_users`);
      if (!data) return [];
      
      const users = JSON.parse(data);
      // Ensure dates are properly parsed
      return users.map((user: any) => ({
        ...user,
        createdAt: new Date(user.createdAt)
      }));
    } catch (error) {
      console.error('Error parsing users from localStorage:', error);
      return [];
    }
  }

  private getSwipes(): SwipeAction[] {
    try {
      const data = localStorage.getItem(`${this.dbName}_swipes`);
      if (!data) return [];
      
      const swipes = JSON.parse(data);
      return swipes.map((swipe: any) => ({
        ...swipe,
        timestamp: new Date(swipe.timestamp)
      }));
    } catch (error) {
      console.error('Error parsing swipes from localStorage:', error);
      return [];
    }
  }

  private getSessions(): Record<string, any> {
    try {
      const data = localStorage.getItem(`${this.dbName}_sessions`);
      return data ? JSON.parse(data) : {};
    } catch (error) {
      console.error('Error parsing sessions from localStorage:', error);
      return {};
    }
  }

  private generateId(): string {
    return Math.random().toString(36).substr(2, 9) + Date.now().toString(36);
  }
}

export const database = new DatabaseManager();