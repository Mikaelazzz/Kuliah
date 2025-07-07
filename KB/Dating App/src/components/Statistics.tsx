import React from 'react';
import { SwipeAction, GAParameters } from '../types';
import { TrendingUp, Users, Heart, X, Settings } from 'lucide-react';

interface StatisticsProps {
  swipeHistory: SwipeAction[];
  parameters: GAParameters;
  onUpdateParameters: (params: Partial<GAParameters>) => void;
  onClose: () => void;
}

const Statistics: React.FC<StatisticsProps> = ({ 
  swipeHistory, 
  parameters, 
  onUpdateParameters, 
  onClose 
}) => {
  const recentSwipes = swipeHistory.slice(-20);
  const likeCount = swipeHistory.filter(s => s.action === 'like').length;
  const dislikeCount = swipeHistory.filter(s => s.action === 'dislike').length;
  const likeRatio = swipeHistory.length > 0 ? (likeCount / swipeHistory.length) * 100 : 0;
  
  const averageCompatibility = swipeHistory.length > 0 
    ? swipeHistory.reduce((sum, s) => sum + s.compatibility, 0) / swipeHistory.length
    : 0;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Statistics & Settings</h2>
            <button
              onClick={onClose}
              className="p-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          <div className="space-y-6">
            {/* Statistics */}
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-blue-500" />
                Your Activity
              </h3>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-green-50 p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Heart className="h-5 w-5 text-green-500" />
                    <span className="text-sm font-medium text-green-700">Likes</span>
                  </div>
                  <div className="text-2xl font-bold text-green-600">{likeCount}</div>
                </div>
                <div className="bg-red-50 p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <X className="h-5 w-5 text-red-500" />
                    <span className="text-sm font-medium text-red-700">Dislikes</span>
                  </div>
                  <div className="text-2xl font-bold text-red-600">{dislikeCount}</div>
                </div>
                <div className="bg-blue-50 p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Users className="h-5 w-5 text-blue-500" />
                    <span className="text-sm font-medium text-blue-700">Total Swipes</span>
                  </div>
                  <div className="text-2xl font-bold text-blue-600">{swipeHistory.length}</div>
                </div>
                <div className="bg-purple-50 p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <TrendingUp className="h-5 w-5 text-purple-500" />
                    <span className="text-sm font-medium text-purple-700">Like Ratio</span>
                  </div>
                  <div className="text-2xl font-bold text-purple-600">{likeRatio.toFixed(1)}%</div>
                </div>
              </div>
              <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                <div className="text-sm font-medium text-gray-700 mb-2">Average Compatibility</div>
                <div className="flex items-center gap-2">
                  <div className="text-lg font-semibold text-gray-800">
                    {averageCompatibility.toFixed(1)}%
                  </div>
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-blue-500 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${averageCompatibility}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Algorithm Parameters */}
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Settings className="h-5 w-5 text-gray-500" />
                Algorithm Settings
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Population Size: {parameters.populationSize}
                  </label>
                  <input
                    type="range"
                    min="20"
                    max="100"
                    value={parameters.populationSize}
                    onChange={(e) => onUpdateParameters({ populationSize: parseInt(e.target.value) })}
                    className="w-full"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Higher values may find better matches but take longer to process
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Mutation Rate: {(parameters.mutationRate * 100).toFixed(1)}%
                  </label>
                  <input
                    type="range"
                    min="0.01"
                    max="0.5"
                    step="0.01"
                    value={parameters.mutationRate}
                    onChange={(e) => onUpdateParameters({ mutationRate: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Higher values increase diversity but may reduce match quality
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Crossover Rate: {(parameters.crossoverRate * 100).toFixed(1)}%
                  </label>
                  <input
                    type="range"
                    min="0.5"
                    max="1"
                    step="0.01"
                    value={parameters.crossoverRate}
                    onChange={(e) => onUpdateParameters({ crossoverRate: parseFloat(e.target.value) })}
                    className="w-full"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Controls how often the algorithm creates hybrid matches
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Generations: {parameters.generations}
                  </label>
                  <input
                    type="range"
                    min="5"
                    max="50"
                    value={parameters.generations}
                    onChange={(e) => onUpdateParameters({ generations: parseInt(e.target.value) })}
                    className="w-full"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    More generations improve match quality but increase processing time
                  </p>
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            {recentSwipes.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-4">Recent Activity</h3>
                <div className="space-y-2 max-h-40 overflow-y-auto">
                  {recentSwipes.slice().reverse().map((swipe, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <div className="flex items-center gap-2">
                        {swipe.action === 'like' ? (
                          <Heart className="h-4 w-4 text-green-500" />
                        ) : (
                          <X className="h-4 w-4 text-red-500" />
                        )}
                        <span className="text-sm text-gray-700">
                          {swipe.action === 'like' ? 'Liked' : 'Passed'}
                        </span>
                      </div>
                      <div className="text-sm text-gray-500">
                        {swipe.compatibility.toFixed(1)}% match
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Statistics;