import React, { useState } from 'react';
import { LoginCredentials, RegisterData } from '../types';
import { smsService } from '../utils/smsService';
import { Heart, Mail, Lock, User, MapPin, Calendar, Eye, EyeOff, Phone, Shield, Users } from 'lucide-react';

interface AuthFormProps {
  mode: 'login' | 'register';
  onSubmit: (data: LoginCredentials | RegisterData) => Promise<void>;
  onToggleMode: () => void;
  loading: boolean;
  error: string | null;
}

const AuthForm: React.FC<AuthFormProps> = ({ mode, onSubmit, onToggleMode, loading, error }) => {
  const [formData, setFormData] = useState<RegisterData>({
    name: '',
    email: '',
    phone: '',
    gender: 'male',
    genderPreference: 'female',
    password: '',
    confirmPassword: '',
    age: 25,
    location: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [otpStep, setOtpStep] = useState(false);
  const [otpCode, setOtpCode] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [otpLoading, setOtpLoading] = useState(false);
  const [otpError, setOtpError] = useState<string | null>(null);
  const [phoneVerified, setPhoneVerified] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (mode === 'login') {
      await onSubmit({
        email: formData.email,
        password: formData.password
      });
    } else {
      // For register, check if phone is verified
      if (!phoneVerified) {
        setOtpError('Silakan verifikasi nomor HP terlebih dahulu');
        return;
      }
      
      // Validate passwords match
      if (formData.password !== formData.confirmPassword) {
        setOtpError('Password tidak cocok');
        return;
      }
      
      if (formData.password.length < 6) {
        setOtpError('Password minimal 6 karakter');
        return;
      }
      
      await onSubmit(formData);
    }
  };

  const handleChange = (field: keyof RegisterData, value: string | number) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Clear errors when user starts typing
    if (otpError) setOtpError(null);
  };

  const handleSendOTP = async () => {
    if (!formData.phone) {
      setOtpError('Silakan masukkan nomor HP');
      return;
    }

    setOtpLoading(true);
    setOtpError(null);

    try {
      const result = await smsService.sendOTP(formData.phone);
      if (result.success) {
        setOtpSent(true);
        setOtpStep(true);
        setOtpError(null);
      } else {
        setOtpError(result.message);
      }
    } catch (error) {
      setOtpError('Gagal mengirim OTP');
    } finally {
      setOtpLoading(false);
    }
  };

  const handleVerifyOTP = async () => {
    if (!otpCode || otpCode.length !== 6) {
      setOtpError('Silakan masukkan kode OTP 6 digit');
      return;
    }

    setOtpLoading(true);
    setOtpError(null);

    try {
      const result = await smsService.verifyOTP(formData.phone, otpCode);
      if (result.success) {
        setPhoneVerified(true);
        setOtpStep(false);
        setOtpCode('');
        setOtpError(null);
        setOtpSent(false);
      } else {
        setOtpError(result.message);
      }
    } catch (error) {
      setOtpError('Gagal memverifikasi OTP');
    } finally {
      setOtpLoading(false);
    }
  };

  const handleResendOTP = async () => {
    setOtpCode('');
    setOtpError(null);
    await handleSendOTP();
  };

  const handleCancelOTP = () => {
    setOtpStep(false);
    setOtpCode('');
    setOtpError(null);
    setOtpSent(false);
  };

  const formatPhoneNumber = (phone: string) => {
    return smsService.formatPhoneNumber(phone);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-500 to-orange-400 flex items-center justify-center p-4">
      <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 w-full max-w-md shadow-2xl border border-white/20">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="bg-white/20 backdrop-blur-sm rounded-full p-4 w-16 h-16 mx-auto mb-4 flex items-center justify-center">
            <Heart className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-white mb-2">LoveGA</h1>
          <p className="text-white/80 text-sm">
            {otpStep 
              ? 'Verifikasi Nomor HP' 
              : mode === 'login' 
                ? 'Selamat datang kembali!' 
                : 'Temukan pasangan ideal dengan AI'
            }
          </p>
        </div>

        {/* Error Message */}
        {(error || otpError) && (
          <div className="bg-red-500/20 border border-red-500/30 rounded-lg p-3 mb-6">
            <p className="text-red-100 text-sm text-center">{error || otpError}</p>
          </div>
        )}

        {/* Success Message for Phone Verification */}
        {phoneVerified && !otpStep && mode === 'register' && (
          <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-3 mb-6">
            <p className="text-green-100 text-sm text-center">✓ Nomor HP berhasil diverifikasi!</p>
          </div>
        )}

        {/* OTP Verification Step */}
        {otpStep && (
          <div className="space-y-6">
            <div className="text-center">
              <Shield className="h-12 w-12 text-white mx-auto mb-4" />
              <h3 className="text-white font-semibold text-lg mb-2">Masukkan Kode OTP</h3>
              <p className="text-white/80 text-sm">
                Kode OTP telah dikirim ke<br />
                <span className="font-medium">{formatPhoneNumber(formData.phone)}</span>
              </p>
            </div>
            
            <div className="space-y-4">
              <div>
                <input
                  type="text"
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                  className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-4 text-white text-center text-xl tracking-widest placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent"
                  placeholder="000000"
                  maxLength={6}
                  autoFocus
                />
                <p className="text-white/60 text-xs mt-2 text-center">
                  Masukkan 6 digit kode yang dikirim via SMS
                </p>
              </div>
              
              <div className="space-y-3">
                <button
                  type="button"
                  onClick={handleVerifyOTP}
                  disabled={otpLoading || otpCode.length !== 6}
                  className="w-full bg-green-500/80 hover:bg-green-500 disabled:bg-white/10 disabled:text-white/50 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 disabled:cursor-not-allowed"
                >
                  {otpLoading ? (
                    <div className="flex items-center justify-center gap-2">
                      <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                      Memverifikasi...
                    </div>
                  ) : (
                    'Verifikasi OTP'
                  )}
                </button>
                
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={handleResendOTP}
                    disabled={otpLoading}
                    className="flex-1 bg-blue-500/80 hover:bg-blue-500 disabled:bg-white/10 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 disabled:cursor-not-allowed text-sm"
                  >
                    {otpLoading ? 'Mengirim...' : 'Kirim Ulang'}
                  </button>
                  <button
                    type="button"
                    onClick={handleCancelOTP}
                    disabled={otpLoading}
                    className="flex-1 bg-gray-500/80 hover:bg-gray-500 disabled:bg-white/10 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 disabled:cursor-not-allowed text-sm"
                  >
                    Batal
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Main Form - Only show when not in OTP step */}
        {!otpStep && (
          <>
            <form onSubmit={handleSubmit} className="space-y-4">
              {mode === 'register' && (
                <>
                  <div>
                    <label className="block text-white/90 text-sm font-medium mb-2">
                      Nama Lengkap
                    </label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white/60" />
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => handleChange('name', e.target.value)}
                        className="w-full bg-white/10 border border-white/20 rounded-lg pl-10 pr-4 py-3 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent"
                        placeholder="Masukkan nama lengkap"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-white/90 text-sm font-medium mb-2">
                      Jenis Kelamin
                    </label>
                    <div className="relative">
                      <Users className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white/60" />
                      <select
                        value={formData.gender}
                        onChange={(e) => handleChange('gender', e.target.value)}
                        className="w-full bg-white/10 border border-white/20 rounded-lg pl-10 pr-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent appearance-none"
                        required
                      >
                        <option value="male" className="bg-gray-800">Laki-laki</option>
                        <option value="female" className="bg-gray-800">Perempuan</option>
                        <option value="other" className="bg-gray-800">Lainnya</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-white/90 text-sm font-medium mb-2">
                      Mencari
                    </label>
                    <div className="relative">
                      <Heart className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white/60" />
                      <select
                        value={formData.genderPreference}
                        onChange={(e) => handleChange('genderPreference', e.target.value)}
                        className="w-full bg-white/10 border border-white/20 rounded-lg pl-10 pr-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent appearance-none"
                        required
                      >
                        <option value="male" className="bg-gray-800">Laki-laki</option>
                        <option value="female" className="bg-gray-800">Perempuan</option>
                        <option value="both" className="bg-gray-800">Keduanya</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-white/90 text-sm font-medium mb-2">
                      Nomor HP
                    </label>
                    <div className="flex gap-2">
                      <div className="relative flex-1">
                        <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white/60" />
                        <input
                          type="tel"
                          value={formData.phone}
                          onChange={(e) => handleChange('phone', e.target.value)}
                          className="w-full bg-white/10 border border-white/20 rounded-lg pl-10 pr-4 py-3 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent"
                          placeholder="08123456789"
                          required
                          disabled={phoneVerified}
                        />
                      </div>
                      <button
                        type="button"
                        onClick={handleSendOTP}
                        disabled={otpLoading || !formData.phone || phoneVerified}
                        className="bg-blue-500/80 hover:bg-blue-500 disabled:bg-white/10 text-white px-4 py-3 rounded-lg transition-all duration-200 disabled:cursor-not-allowed whitespace-nowrap font-medium"
                      >
                        {phoneVerified ? (
                          <span className="text-green-300">✓ Verified</span>
                        ) : otpLoading ? (
                          <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                        ) : (
                          'Kirim OTP'
                        )}
                      </button>
                    </div>
                    {phoneVerified && (
                      <p className="text-green-300 text-xs mt-1 flex items-center gap-1">
                        <Shield className="h-3 w-3" />
                        Nomor HP terverifikasi
                      </p>
                    )}
                  </div>
                </>
              )}

              <div>
                <label className="block text-white/90 text-sm font-medium mb-2">
                  Email
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white/60" />
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleChange('email', e.target.value)}
                    className="w-full bg-white/10 border border-white/20 rounded-lg pl-10 pr-4 py-3 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent"
                    placeholder="Masukkan email"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-white/90 text-sm font-medium mb-2">
                  Password
                </label>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white/60" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={formData.password}
                    onChange={(e) => handleChange('password', e.target.value)}
                    className="w-full bg-white/10 border border-white/20 rounded-lg pl-10 pr-12 py-3 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent"
                    placeholder="Masukkan password"
                    required
                    minLength={6}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/60 hover:text-white/80"
                  >
                    {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                  </button>
                </div>
              </div>

              {mode === 'register' && (
                <>
                  <div>
                    <label className="block text-white/90 text-sm font-medium mb-2">
                      Konfirmasi Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white/60" />
                      <input
                        type={showConfirmPassword ? 'text' : 'password'}
                        value={formData.confirmPassword}
                        onChange={(e) => handleChange('confirmPassword', e.target.value)}
                        className="w-full bg-white/10 border border-white/20 rounded-lg pl-10 pr-12 py-3 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent"
                        placeholder="Konfirmasi password"
                        required
                        minLength={6}
                      />
                      <button
                        type="button"
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-white/60 hover:text-white/80"
                      >
                        {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                      </button>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-white/90 text-sm font-medium mb-2">
                        Umur
                      </label>
                      <div className="relative">
                        <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white/60" />
                        <input
                          type="number"
                          value={formData.age}
                          onChange={(e) => handleChange('age', parseInt(e.target.value))}
                          className="w-full bg-white/10 border border-white/20 rounded-lg pl-10 pr-4 py-3 text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent"
                          placeholder="Umur"
                          min="18"
                          max="100"
                          required
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-white/90 text-sm font-medium mb-2">
                        Lokasi
                      </label>
                      <div className="relative">
                        <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-white/60" />
                        <select
                          value={formData.location}
                          onChange={(e) => handleChange('location', e.target.value)}
                          className="w-full bg-white/10 border border-white/20 rounded-lg pl-10 pr-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-white/30 focus:border-transparent appearance-none"
                          required
                        >
                          <option value="" className="bg-gray-800">Pilih Kota</option>
                          <option value="Jakarta, Indonesia" className="bg-gray-800">Jakarta</option>
                          <option value="Bandung, Indonesia" className="bg-gray-800">Bandung</option>
                          <option value="Yogyakarta, Indonesia" className="bg-gray-800">Yogyakarta</option>
                          <option value="Surabaya, Indonesia" className="bg-gray-800">Surabaya</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </>
              )}

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading || (mode === 'register' && !phoneVerified)}
                className="w-full bg-white/20 hover:bg-white/30 disabled:bg-white/10 text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 backdrop-blur-sm border border-white/30 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <div className="flex items-center justify-center gap-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent"></div>
                    {mode === 'login' ? 'Masuk...' : 'Membuat Akun...'}
                  </div>
                ) : (
                  mode === 'login' ? 'Masuk' : 'Daftar'
                )}
              </button>
            </form>

            {/* Toggle Mode */}
            <div className="mt-6 text-center">
              <p className="text-white/80 text-sm">
                {mode === 'login' ? "Belum punya akun?" : 'Sudah punya akun?'}
                <button
                  onClick={onToggleMode}
                  className="ml-2 text-white font-semibold hover:text-white/80 transition-colors"
                >
                  {mode === 'login' ? 'Daftar' : 'Masuk'}
                </button>
              </p>
            </div>

            {/* Demo Credentials */}
            {mode === 'login' && (
              <div className="mt-4 p-3 bg-white/10 rounded-lg border border-white/20">
                <p className="text-white/80 text-xs text-center mb-2">Akun Demo:</p>
                <p className="text-white/70 text-xs text-center">
                  Email: sari.dewi@example.com<br />
                  Password: password123
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default AuthForm;