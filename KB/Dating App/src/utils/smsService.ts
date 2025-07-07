// SMS Service for OTP verification
class SMSService {
  private otpStorage: Map<string, { code: string; expiresAt: Date; attempts: number }> = new Map();

  // Generate 6-digit OTP
  generateOTP(): string {
    return Math.floor(100000 + Math.random() * 900000).toString();
  }

  // Send OTP to phone number (simulated)
  async sendOTP(phoneNumber: string): Promise<{ success: boolean; message: string }> {
    try {
      // Clean phone number
      const cleanPhone = phoneNumber.replace(/\D/g, '');
      
      // Validate Indonesian phone number format
      if (!this.isValidIndonesianPhone(cleanPhone)) {
        return { success: false, message: 'Format nomor HP tidak valid. Gunakan format Indonesia (+62)' };
      }

      const otp = this.generateOTP();
      const expiresAt = new Date(Date.now() + 5 * 60 * 1000); // 5 minutes

      // Store OTP
      this.otpStorage.set(cleanPhone, {
        code: otp,
        expiresAt,
        attempts: 0
      });

      // Simulate SMS sending (in production, integrate with SMS provider like Twilio, Nexmo, etc.)
      console.log(`SMS OTP sent to ${phoneNumber}: ${otp}`);
      
      // For demo purposes, show OTP in alert
      alert(`Demo OTP untuk ${phoneNumber}: ${otp}\n\nDalam aplikasi nyata, OTP akan dikirim via SMS.`);

      return { 
        success: true, 
        message: `Kode OTP telah dikirim ke ${phoneNumber}. Kode berlaku selama 5 menit.` 
      };
    } catch (error) {
      return { success: false, message: 'Gagal mengirim OTP. Silakan coba lagi.' };
    }
  }

  // Verify OTP
  async verifyOTP(phoneNumber: string, code: string): Promise<{ success: boolean; message: string }> {
    const cleanPhone = phoneNumber.replace(/\D/g, '');
    const storedOTP = this.otpStorage.get(cleanPhone);

    if (!storedOTP) {
      return { success: false, message: 'Kode OTP tidak ditemukan. Silakan minta kode baru.' };
    }

    // Check if OTP expired
    if (new Date() > storedOTP.expiresAt) {
      this.otpStorage.delete(cleanPhone);
      return { success: false, message: 'Kode OTP telah kedaluwarsa. Silakan minta kode baru.' };
    }

    // Check attempts
    if (storedOTP.attempts >= 3) {
      this.otpStorage.delete(cleanPhone);
      return { success: false, message: 'Terlalu banyak percobaan. Silakan minta kode baru.' };
    }

    // Verify code
    if (storedOTP.code !== code) {
      storedOTP.attempts++;
      return { success: false, message: `Kode OTP salah. Sisa percobaan: ${3 - storedOTP.attempts}` };
    }

    // Success - remove OTP from storage
    this.otpStorage.delete(cleanPhone);
    return { success: true, message: 'Nomor HP berhasil diverifikasi!' };
  }

  // Validate Indonesian phone number
  private isValidIndonesianPhone(phone: string): boolean {
    // Indonesian phone number patterns
    const patterns = [
      /^62\d{9,12}$/, // +62 format
      /^08\d{8,11}$/, // 08 format
      /^8\d{8,11}$/   // 8 format
    ];

    return patterns.some(pattern => pattern.test(phone));
  }

  // Format phone number for display
  formatPhoneNumber(phone: string): string {
    const clean = phone.replace(/\D/g, '');
    
    if (clean.startsWith('62')) {
      return `+${clean}`;
    } else if (clean.startsWith('08')) {
      return `+62${clean.substring(1)}`;
    } else if (clean.startsWith('8')) {
      return `+62${clean}`;
    }
    
    return phone;
  }
}

export const smsService = new SMSService();