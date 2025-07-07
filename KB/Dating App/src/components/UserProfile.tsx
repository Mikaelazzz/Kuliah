import React, { useState } from 'react';
import { User } from '../types';
import { Edit, Save, X, Users, Heart } from 'lucide-react';

interface UserProfileProps {
  user: User;
  onUpdateUser: (updatedUser: User) => void;
  onClose: () => void;
}

const UserProfile: React.FC<UserProfileProps> = ({ user, onUpdateUser, onClose }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState(user);

  const handleSave = () => {
    onUpdateUser(editedUser);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditedUser(user);
    setIsEditing(false);
  };

  const updatePersonality = (trait: keyof typeof user.personality, value: number) => {
    setEditedUser({
      ...editedUser,
      personality: {
        ...editedUser.personality,
        [trait]: value
      }
    });
  };

  const updatePreferences = (key: string, value: any) => {
    setEditedUser({
      ...editedUser,
      preferences: {
        ...editedUser.preferences,
        [key]: value
      }
    });
  };

  const addInterest = (interest: string) => {
    if (interest && !editedUser.interests.includes(interest)) {
      setEditedUser({
        ...editedUser,
        interests: [...editedUser.interests, interest]
      });
    }
  };

  const removeInterest = (interest: string) => {
    setEditedUser({
      ...editedUser,
      interests: editedUser.interests.filter(i => i !== interest)
    });
  };

  const getGenderLabel = (gender: string) => {
    switch (gender) {
      case 'male': return 'Laki-laki';
      case 'female': return 'Perempuan';
      case 'other': return 'Lainnya';
      default: return gender;
    }
  };

  const getGenderPreferenceLabel = (preference: string) => {
    switch (preference) {
      case 'male': return 'Laki-laki';
      case 'female': return 'Perempuan';
      case 'both': return 'Keduanya';
      default: return preference;
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-gray-800">Pengaturan Profil</h2>
            <div className="flex gap-2">
              {isEditing ? (
                <>
                  <button
                    onClick={handleSave}
                    className="p-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                  >
                    <Save className="h-5 w-5" />
                  </button>
                  <button
                    onClick={handleCancel}
                    className="p-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </>
              ) : (
                <button
                  onClick={() => setIsEditing(true)}
                  className="p-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
                >
                  <Edit className="h-5 w-5" />
                </button>
              )}
              <button
                onClick={onClose}
                className="p-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 transition-colors"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
          </div>

          <div className="space-y-6">
            {/* Basic Info */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Informasi Dasar</h3>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Nama</label>
                  <input
                    type="text"
                    value={editedUser.name}
                    onChange={(e) => setEditedUser({...editedUser, name: e.target.value})}
                    disabled={!isEditing}
                    className="w-full p-2 border border-gray-300 rounded-lg disabled:bg-gray-100"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Umur</label>
                  <input
                    type="number"
                    value={editedUser.age}
                    onChange={(e) => setEditedUser({...editedUser, age: parseInt(e.target.value)})}
                    disabled={!isEditing}
                    className="w-full p-2 border border-gray-300 rounded-lg disabled:bg-gray-100"
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4 mt-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Jenis Kelamin</label>
                  <div className="flex items-center gap-2">
                    <Users className="h-4 w-4 text-gray-500" />
                    <span className="text-gray-700">{getGenderLabel(editedUser.gender)}</span>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Nomor HP</label>
                  <div className="text-gray-700">
                    {editedUser.phone} {editedUser.phoneVerified && <span className="text-green-500">✓</span>}
                  </div>
                </div>
              </div>
              
              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
                <textarea
                  value={editedUser.bio}
                  onChange={(e) => setEditedUser({...editedUser, bio: e.target.value})}
                  disabled={!isEditing}
                  rows={3}
                  className="w-full p-2 border border-gray-300 rounded-lg disabled:bg-gray-100"
                  placeholder="Ceritakan tentang diri Anda..."
                />
              </div>
            </div>

            {/* Personality Traits */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Kepribadian</h3>
              <div className="space-y-4">
                {Object.entries(editedUser.personality).map(([trait, value]) => {
                  const traitLabels: Record<string, string> = {
                    extroversion: 'Ekstrovert',
                    openness: 'Keterbukaan',
                    conscientiousness: 'Kehati-hatian',
                    agreeableness: 'Keramahan',
                    neuroticism: 'Neurotisisme'
                  };
                  
                  return (
                    <div key={trait}>
                      <div className="flex justify-between items-center mb-2">
                        <label className="text-sm font-medium text-gray-700">
                          {traitLabels[trait] || trait}
                        </label>
                        <span className="text-sm text-gray-600">{value}/100</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={value}
                        onChange={(e) => updatePersonality(trait as keyof typeof user.personality, parseInt(e.target.value))}
                        disabled={!isEditing}
                        className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer disabled:cursor-not-allowed"
                      />
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Interests */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Minat & Hobi</h3>
              <div className="flex flex-wrap gap-2 mb-3">
                {editedUser.interests.map((interest) => (
                  <span 
                    key={interest}
                    className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full flex items-center gap-1"
                  >
                    {interest}
                    {isEditing && (
                      <button
                        onClick={() => removeInterest(interest)}
                        className="ml-1 text-red-500 hover:text-red-700"
                      >
                        <X className="h-3 w-3" />
                      </button>
                    )}
                  </span>
                ))}
              </div>
              {isEditing && (
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="Tambah minat baru"
                    className="flex-1 p-2 border border-gray-300 rounded-lg"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        addInterest(e.currentTarget.value);
                        e.currentTarget.value = '';
                      }
                    }}
                  />
                </div>
              )}
            </div>

            {/* Preferences */}
            <div>
              <h3 className="text-lg font-semibold mb-3">Preferensi Pencarian</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <Heart className="h-4 w-4 text-pink-500" />
                    <label className="text-sm font-medium text-gray-700">
                      Mencari: {getGenderPreferenceLabel(editedUser.preferences.genderPreference)}
                    </label>
                  </div>
                  {isEditing && (
                    <select
                      value={editedUser.preferences.genderPreference}
                      onChange={(e) => updatePreferences('genderPreference', e.target.value)}
                      className="w-full p-2 border border-gray-300 rounded-lg"
                    >
                      <option value="male">Laki-laki</option>
                      <option value="female">Perempuan</option>
                      <option value="both">Keduanya</option>
                    </select>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Rentang Umur: {editedUser.preferences.ageRange[0]} - {editedUser.preferences.ageRange[1]}
                  </label>
                  <div className="flex gap-4">
                    <input
                      type="range"
                      min="18"
                      max="80"
                      value={editedUser.preferences.ageRange[0]}
                      onChange={(e) => updatePreferences('ageRange', [parseInt(e.target.value), editedUser.preferences.ageRange[1]])}
                      disabled={!isEditing}
                      className="flex-1"
                    />
                    <input
                      type="range"
                      min="18"
                      max="80"
                      value={editedUser.preferences.ageRange[1]}
                      onChange={(e) => updatePreferences('ageRange', [editedUser.preferences.ageRange[0], parseInt(e.target.value)])}
                      disabled={!isEditing}
                      className="flex-1"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Pentingnya Kepribadian: {editedUser.preferences.personalityImportance}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={editedUser.preferences.personalityImportance}
                    onChange={(e) => updatePreferences('personalityImportance', parseInt(e.target.value))}
                    disabled={!isEditing}
                    className="w-full"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Pentingnya Minat: {editedUser.preferences.interestImportance}%
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    value={editedUser.preferences.interestImportance}
                    onChange={(e) => updatePreferences('interestImportance', parseInt(e.target.value))}
                    disabled={!isEditing}
                    className="w-full"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserProfile;