import { database } from './database';
import { AuthUser, LoginCredentials, RegisterData, User } from '../types';

class AuthManager {
  private currentUser: AuthUser | null = null;
  private sessionId: string | null = null;

  constructor() {
    this.initializeAuth();
  }

  private async initializeAuth(): Promise<void> {
    const sessionId = localStorage.getItem('lovega_session');
    if (sessionId) {
      const userId = await database.validateSession(sessionId);
      if (userId) {
        const user = await database.getUserById(userId);
        if (user) {
          this.currentUser = {
            id: user.id,
            email: user.email,
            name: user.name,
            isAuthenticated: true
          };
          this.sessionId = sessionId;
        }
      }
    }
  }

  async login(credentials: LoginCredentials): Promise<{ success: boolean; user?: AuthUser; error?: string }> {
    try {
      const user = await database.getUserByEmail(credentials.email);
      
      if (!user) {
        return { success: false, error: 'Email tidak ditemukan' };
      }

      // For demo purposes, we'll use a simple password check
      // In production, use proper password hashing
      const storedPassword = localStorage.getItem(`password_${user.id}`) || 'password123';
      
      if (credentials.password !== storedPassword) {
        return { success: false, error: 'Password salah' };
      }

      if (!user.phoneVerified) {
        return { success: false, error: 'Nomor HP belum diverifikasi' };
      }

      const sessionId = await database.createSession(user.id);
      localStorage.setItem('lovega_session', sessionId);
      
      this.currentUser = {
        id: user.id,
        email: user.email,
        name: user.name,
        isAuthenticated: true
      };
      this.sessionId = sessionId;

      return { success: true, user: this.currentUser };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'Login gagal' };
    }
  }

  async register(data: RegisterData): Promise<{ success: boolean; user?: AuthUser; error?: string }> {
    try {
      console.log('Starting registration with data:', data);

      // Validate required fields
      if (!data.name || !data.email || !data.phone || !data.password || !data.location) {
        return { success: false, error: 'Semua field wajib diisi' };
      }

      if (data.password !== data.confirmPassword) {
        return { success: false, error: 'Password tidak cocok' };
      }

      if (data.password.length < 6) {
        return { success: false, error: 'Password minimal 6 karakter' };
      }

      if (data.age < 18 || data.age > 100) {
        return { success: false, error: 'Umur harus antara 18-100 tahun' };
      }

      // Check if email already exists
      const existingUser = await database.getUserByEmail(data.email);
      if (existingUser) {
        return { success: false, error: 'Email sudah terdaftar' };
      }

      // Check if phone already exists
      const existingPhone = await database.getUserByPhone(data.phone);
      if (existingPhone) {
        return { success: false, error: 'Nomor HP sudah terdaftar' };
      }

      console.log('Creating new user...');

      // Create new user
      const newUser = await database.createUser({
        name: data.name.trim(),
        email: data.email.toLowerCase().trim(),
        phone: data.phone.trim(),
        phoneVerified: true, // Assuming OTP was verified in the form
        gender: data.gender,
        age: data.age,
        location: data.location,
        bio: `Halo! Saya ${data.name}. Senang berkenalan dengan Anda!`,
        interests: this.getDefaultInterests(data.gender),
        personality: {
          extroversion: 50 + Math.floor(Math.random() * 30) - 15, // 35-65
          openness: 50 + Math.floor(Math.random() * 30) - 15,
          conscientiousness: 50 + Math.floor(Math.random() * 30) - 15,
          agreeableness: 50 + Math.floor(Math.random() * 30) - 15,
          neuroticism: 30 + Math.floor(Math.random() * 20) // 30-50
        },
        preferences: {
          ageRange: [Math.max(18, data.age - 5), Math.min(100, data.age + 10)] as [number, number],
          maxDistance: 50,
          genderPreference: data.genderPreference,
          interests: [],
          personalityImportance: 70,
          interestImportance: 60
        },
        photo: this.getRandomPhoto(data.gender)
      });

      console.log('User created successfully:', newUser.id);

      // Store password (in production, hash properly)
      localStorage.setItem(`password_${newUser.id}`, data.password);

      // Create session
      const sessionId = await database.createSession(newUser.id);
      localStorage.setItem('lovega_session', sessionId);

      this.currentUser = {
        id: newUser.id,
        email: newUser.email,
        name: newUser.name,
        isAuthenticated: true
      };
      this.sessionId = sessionId;

      console.log('Registration completed successfully');
      return { success: true, user: this.currentUser };
    } catch (error) {
      console.error('Registration error:', error);
      return { success: false, error: 'Registrasi gagal. Silakan coba lagi.' };
    }
  }

  private getDefaultInterests(gender: string): string[] {
    const commonInterests = ['Music', 'Movies', 'Travel', 'Food', 'Photography'];
    const maleInterests = ['Gaming', 'Sports', 'Technology', 'Cars', 'Fitness'];
    const femaleInterests = ['Fashion', 'Art', 'Reading', 'Cooking', 'Yoga'];
    
    const genderSpecific = gender === 'female' ? femaleInterests : maleInterests;
    const selected = [...commonInterests.slice(0, 3), ...genderSpecific.slice(0, 2)];
    
    return selected;
  }

  private getRandomPhoto(gender: string): string {
    const malePhotos = [
      'https://images.pexels.com/photos/1222271/pexels-photo-1222271.jpeg?auto=compress&cs=tinysrgb&w=400',
      'https://images.pexels.com/photos/1043471/pexels-photo-1043471.jpeg?auto=compress&cs=tinysrgb&w=400',
      'https://images.pexels.com/photos/1516680/pexels-photo-1516680.jpeg?auto=compress&cs=tinysrgb&w=400',
      'https://images.pexels.com/photos/1300402/pexels-photo-1300402.jpeg?auto=compress&cs=tinysrgb&w=400',
      'https://images.pexels.com/photos/1681010/pexels-photo-1681010.jpeg?auto=compress&cs=tinysrgb&w=400'
    ];
    
    const femalePhotos = [
      'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=400',
      'https://images.pexels.com/photos/1239291/pexels-photo-1239291.jpeg?auto=compress&cs=tinysrgb&w=400',
      'https://images.pexels.com/photos/1130626/pexels-photo-1130626.jpeg?auto=compress&cs=tinysrgb&w=400',
      'https://images.pexels.com/photos/1858175/pexels-photo-1858175.jpeg?auto=compress&cs=tinysrgb&w=400',
      'https://images.pexels.com/photos/1036623/pexels-photo-1036623.jpeg?auto=compress&cs=tinysrgb&w=400'
    ];

    const photos = gender === 'female' ? femalePhotos : malePhotos;
    return photos[Math.floor(Math.random() * photos.length)];
  }

  async logout(): Promise<void> {
    if (this.sessionId) {
      await database.deleteSession(this.sessionId);
      localStorage.removeItem('lovega_session');
    }
    
    this.currentUser = null;
    this.sessionId = null;
  }

  getCurrentUser(): AuthUser | null {
    return this.currentUser;
  }

  isAuthenticated(): boolean {
    return this.currentUser?.isAuthenticated || false;
  }

  async getCurrentUserProfile(): Promise<User | null> {
    if (!this.currentUser) return null;
    return await database.getUserById(this.currentUser.id);
  }
}

export const authManager = new AuthManager();