import React, { useState, useEffect } from 'react';
import { User, MatchCandidate, SwipeAction, AuthUser } from './types';
import { GeneticMatchingEngine } from './utils/geneticAlgorithm';
import { authManager } from './utils/auth';
import { database } from './utils/database';
import SwipeCard from './components/SwipeCard';
import UserProfile from './components/UserProfile';
import Statistics from './components/Statistics';
import AuthForm from './components/AuthForm';
import { Heart, User as UserIcon, BarChart3, Shuffle, Zap, LogOut } from 'lucide-react';

function App() {
  const [authUser, setAuthUser] = useState<AuthUser | null>(null);
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [authMode, setAuthMode] = useState<'login' | 'register'>('login');
  const [authLoading, setAuthLoading] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);
  const [matchingEngine] = useState(() => new GeneticMatchingEngine());
  const [matches, setMatches] = useState<MatchCandidate[]>([]);
  const [currentMatchIndex, setCurrentMatchIndex] = useState(0);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showProfile, setShowProfile] = useState(false);
  const [showStats, setShowStats] = useState(false);
  const [swipeHistory, setSwipeHistory] = useState<SwipeAction[]>([]);

  useEffect(() => {
    initializeAuth();
  }, []);

  useEffect(() => {
    if (currentUser) {
      loadUserData();
      generateNewMatches();
    }
  }, [currentUser]);

  const initializeAuth = async () => {
    try {
      const user = authManager.getCurrentUser();
      if (user) {
        setAuthUser(user);
        const profile = await authManager.getCurrentUserProfile();
        setCurrentUser(profile);
      }
    } catch (error) {
      console.error('Error initializing auth:', error);
    }
  };

  const loadUserData = async () => {
    if (!currentUser) return;
    
    try {
      await matchingEngine.loadSwipeHistory(currentUser.id);
      const history = matchingEngine.getSwipeHistory();
      setSwipeHistory(history);
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const handleAuth = async (data: any) => {
    setAuthLoading(true);
    setAuthError(null);

    try {
      console.log('Attempting authentication with mode:', authMode);
      console.log('Auth data:', data);

      const result = authMode === 'login' 
        ? await authManager.login(data)
        : await authManager.register(data);

      console.log('Auth result:', result);

      if (result.success && result.user) {
        setAuthUser(result.user);
        const profile = await authManager.getCurrentUserProfile();
        setCurrentUser(profile);
        setAuthError(null);
        console.log('Authentication successful');
      } else {
        setAuthError(result.error || 'Authentication failed');
        console.error('Authentication failed:', result.error);
      }
    } catch (error) {
      console.error('Authentication error:', error);
      setAuthError('Terjadi kesalahan yang tidak terduga');
    } finally {
      setAuthLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await authManager.logout();
      setAuthUser(null);
      setCurrentUser(null);
      setMatches([]);
      setSwipeHistory([]);
    } catch (error) {
      console.error('Error during logout:', error);
    }
  };

  const generateNewMatches = async () => {
    if (!currentUser) return;
    
    setIsGenerating(true);
    
    try {
      // Simulate some processing time for the GA
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const newMatches = await matchingEngine.generateMatches(currentUser);
      setMatches(newMatches);
      setCurrentMatchIndex(0);
      console.log('Generated matches:', newMatches.length);
    } catch (error) {
      console.error('Error generating matches:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSwipe = async (action: 'like' | 'dislike') => {
    const currentMatch = matches[currentMatchIndex];
    if (!currentMatch || !currentUser) return;

    try {
      const swipeAction: Omit<SwipeAction, 'id'> = {
        userId: currentUser.id,
        targetUserId: currentMatch.user.id,
        action,
        compatibility: currentMatch.compatibility,
        timestamp: new Date()
      };

      await matchingEngine.recordSwipe(swipeAction);
      const updatedHistory = matchingEngine.getSwipeHistory();
      setSwipeHistory(updatedHistory);

      if (currentMatchIndex < matches.length - 1) {
        setCurrentMatchIndex(prev => prev + 1);
      } else {
        // Generate new matches when we run out
        generateNewMatches();
      }
    } catch (error) {
      console.error('Error recording swipe:', error);
    }
  };

  const handleUpdateUser = async (updatedUser: User) => {
    if (!currentUser) return;
    
    try {
      await database.updateUser(currentUser.id, updatedUser);
      setCurrentUser(updatedUser);
      setShowProfile(false);
    } catch (error) {
      console.error('Error updating user:', error);
    }
  };

  const handleUpdateParameters = (params: any) => {
    matchingEngine.updateParameters(params);
  };

  // Show auth form if not authenticated
  if (!authUser || !currentUser) {
    return (
      <AuthForm
        mode={authMode}
        onSubmit={handleAuth}
        onToggleMode={() => {
          setAuthMode(authMode === 'login' ? 'register' : 'login');
          setAuthError(null);
        }}
        loading={authLoading}
        error={authError}
      />
    );
  }

  const currentMatch = matches[currentMatchIndex];
  const hasMoreMatches = currentMatchIndex < matches.length - 1;

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-orange-400">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div className="flex items-center gap-3">
            <div className="bg-white/20 backdrop-blur-sm rounded-full p-3">
              <Heart className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-white">LoveGA</h1>
              <p className="text-white/80 text-sm">Welcome, {currentUser.name}</p>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setShowProfile(true)}
              className="bg-white/20 backdrop-blur-sm text-white p-3 rounded-full hover:bg-white/30 transition-colors"
            >
              <UserIcon className="h-5 w-5" />
            </button>
            <button
              onClick={() => setShowStats(true)}
              className="bg-white/20 backdrop-blur-sm text-white p-3 rounded-full hover:bg-white/30 transition-colors"
            >
              <BarChart3 className="h-5 w-5" />
            </button>
            <button
              onClick={generateNewMatches}
              disabled={isGenerating}
              className="bg-white/20 backdrop-blur-sm text-white p-3 rounded-full hover:bg-white/30 transition-colors disabled:opacity-50"
            >
              <Shuffle className="h-5 w-5" />
            </button>
            <button
              onClick={handleLogout}
              className="bg-white/20 backdrop-blur-sm text-white p-3 rounded-full hover:bg-white/30 transition-colors"
            >
              <LogOut className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="max-w-md mx-auto">
          {isGenerating ? (
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-4 border-white border-t-transparent mx-auto mb-4"></div>
              <p className="text-white text-lg font-medium">Finding your perfect matches...</p>
              <p className="text-white/70 text-sm mt-2">Genetic Algorithm is evolving compatibility</p>
            </div>
          ) : matches.length > 0 && currentMatch ? (
            <div className="relative h-[600px]">
              <SwipeCard
                candidate={currentMatch}
                onSwipe={handleSwipe}
                isTopCard={true}
              />
              {/* Preview next card */}
              {hasMoreMatches && (
                <div className="absolute inset-0 -z-10 scale-95 opacity-50">
                  <SwipeCard
                    candidate={matches[currentMatchIndex + 1]}
                    onSwipe={() => {}}
                    isTopCard={false}
                  />
                </div>
              )}
            </div>
          ) : (
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-8 text-center">
              <Zap className="h-12 w-12 text-white mx-auto mb-4" />
              <p className="text-white text-lg font-medium">No more matches right now</p>
              <p className="text-white/70 text-sm mt-2">Try adjusting your preferences or generating new matches</p>
              <button
                onClick={generateNewMatches}
                className="mt-4 bg-white/20 backdrop-blur-sm text-white px-6 py-2 rounded-full hover:bg-white/30 transition-colors"
              >
                Generate New Matches
              </button>
            </div>
          )}
        </div>

        {/* Status Bar */}
        <div className="max-w-md mx-auto mt-6">
          <div className="bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 text-center">
            <span className="text-white/90 text-sm">
              {matches.length > 0 ? `${currentMatchIndex + 1} / ${matches.length}` : 'No matches'}
            </span>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="max-w-md mx-auto mt-4 grid grid-cols-3 gap-2">
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 text-center">
            <div className="text-white text-lg font-semibold">
              {swipeHistory.filter(s => s.action === 'like').length}
            </div>
            <div className="text-white/70 text-xs">Likes</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 text-center">
            <div className="text-white text-lg font-semibold">
              {swipeHistory.length}
            </div>
            <div className="text-white/70 text-xs">Total Swipes</div>
          </div>
          <div className="bg-white/10 backdrop-blur-sm rounded-lg p-3 text-center">
            <div className="text-white text-lg font-semibold">
              {swipeHistory.length > 0 
                ? ((swipeHistory.filter(s => s.action === 'like').length / swipeHistory.length) * 100).toFixed(0)
                : 0}%
            </div>
            <div className="text-white/70 text-xs">Like Rate</div>
          </div>
        </div>
      </div>

      {/* Modals */}
      {showProfile && (
        <UserProfile
          user={currentUser}
          onUpdateUser={handleUpdateUser}
          onClose={() => setShowProfile(false)}
        />
      )}

      {showStats && (
        <Statistics
          swipeHistory={swipeHistory}
          parameters={matchingEngine.getParameters()}
          onUpdateParameters={handleUpdateParameters}
          onClose={() => setShowStats(false)}
        />
      )}
    </div>
  );
}

export default App;