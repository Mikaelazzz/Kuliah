import React from 'react';
import { MatchCandidate } from '../types';
import { Heart, X, MapPin, Users, Zap } from 'lucide-react';

interface SwipeCardProps {
  candidate: MatchCandidate;
  onSwipe: (action: 'like' | 'dislike') => void;
  isTopCard: boolean;
}

const SwipeCard: React.FC<SwipeCardProps> = ({ candidate, onSwipe, isTopCard }) => {
  const { user, compatibility, commonInterests, personalityMatch } = candidate;

  const getCompatibilityColor = (score: number) => {
    if (score >= 80) return 'text-emerald-500';
    if (score >= 60) return 'text-amber-500';
    return 'text-red-500';
  };

  const getCompatibilityLabel = (score: number) => {
    if (score >= 90) return 'Excellent Match';
    if (score >= 80) return 'Great Match';
    if (score >= 60) return 'Good Match';
    return 'Fair Match';
  };

  return (
    <div className={`
      absolute inset-0 bg-white rounded-2xl shadow-2xl transition-all duration-300
      ${isTopCard ? 'z-10 scale-100' : 'z-0 scale-95 opacity-80'}
    `}>
      <div className="relative h-full flex flex-col">
        {/* Image Section */}
        <div className="relative h-3/5 overflow-hidden rounded-t-2xl">
          <img 
            src={user.photo} 
            alt={user.name}
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
          
          {/* Compatibility Badge */}
          <div className="absolute top-4 right-4 bg-white/90 backdrop-blur-sm rounded-full px-3 py-1">
            <div className="flex items-center gap-1">
              <Zap className="h-4 w-4 text-yellow-500" />
              <span className={`font-semibold ${getCompatibilityColor(compatibility)}`}>
                {Math.round(compatibility)}%
              </span>
            </div>
          </div>
          
          {/* Basic Info Overlay */}
          <div className="absolute bottom-4 left-4 text-white">
            <h3 className="text-2xl font-bold">{user.name}</h3>
            <p className="text-lg opacity-90">{user.age} years old</p>
            <div className="flex items-center gap-1 mt-1">
              <MapPin className="h-4 w-4" />
              <span className="text-sm">{user.location}</span>
            </div>
          </div>
        </div>

        {/* Details Section */}
        <div className="flex-1 p-6 space-y-4">
          {/* Compatibility Score */}
          <div className="text-center">
            <div className={`text-lg font-semibold ${getCompatibilityColor(compatibility)}`}>
              {getCompatibilityLabel(compatibility)}
            </div>
            <div className="text-sm text-gray-600">
              {Math.round(personalityMatch)}% personality match
            </div>
          </div>

          {/* Bio */}
          <p className="text-gray-700 text-sm leading-relaxed">{user.bio}</p>

          {/* Common Interests */}
          {commonInterests.length > 0 && (
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Users className="h-4 w-4 text-blue-500" />
                <span className="text-sm font-medium text-gray-700">Common Interests</span>
              </div>
              <div className="flex flex-wrap gap-2">
                {commonInterests.map((interest) => (
                  <span 
                    key={interest}
                    className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                  >
                    {interest}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* All Interests */}
          <div>
            <div className="text-sm font-medium text-gray-700 mb-2">Interests</div>
            <div className="flex flex-wrap gap-2">
              {user.interests.map((interest) => (
                <span 
                  key={interest}
                  className={`px-2 py-1 text-xs rounded-full ${
                    commonInterests.includes(interest)
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {interest}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center gap-6 p-6 bg-gray-50 rounded-b-2xl">
          <button
            onClick={() => onSwipe('dislike')}
            className="bg-red-500 hover:bg-red-600 text-white p-4 rounded-full shadow-lg transition-all duration-200 hover:scale-110"
          >
            <X className="h-6 w-6" />
          </button>
          <button
            onClick={() => onSwipe('like')}
            className="bg-green-500 hover:bg-green-600 text-white p-4 rounded-full shadow-lg transition-all duration-200 hover:scale-110"
          >
            <Heart className="h-6 w-6" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default SwipeCard;