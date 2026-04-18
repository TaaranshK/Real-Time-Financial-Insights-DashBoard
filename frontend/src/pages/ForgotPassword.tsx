import { useState, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence, Variants } from 'framer-motion';
import { Mail, Lock, CheckCircle2, Zap, Loader2, ArrowLeft } from 'lucide-react';
import toast from 'react-hot-toast';
import { forgotPassword, verifyOtp, resetPassword } from '@/lib/api';
import ParticleBackground from '@/components/ParticleBackground';

const steps = ['Email', 'Verify OTP', 'New Password'];

const stepVariants: Variants = {
  hidden: { opacity: 0, x: 30 },
  show: { opacity: 1, x: 0, transition: { duration: 0.35 } },
  exit: { opacity: 0, x: -30, transition: { duration: 0.2 } },
};

const ForgotPassword: React.FC = () => {
  const [step, setStep] = useState(0);
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState(['', '', '', '', '', '']);
  const [resetToken, setResetToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const otpRefs = useRef<(HTMLInputElement | null)[]>([]);
  const navigate = useNavigate();

  const handleOtpChange = (index: number, value: string) => {
    if (!/^\d?$/.test(value)) return;
    const next = [...otp];
    next[index] = value;
    setOtp(next);
    if (value && index < 5) otpRefs.current[index + 1]?.focus();
  };

  const handleOtpKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) otpRefs.current[index - 1]?.focus();
  };

  const handleStep0 = async () => {
    if (!email) { toast.error('Please enter your email'); return; }
    setLoading(true);
    try {
      await forgotPassword(email);
      toast.success('OTP sent to your email!');
      setStep(1);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Failed to send OTP');
    } finally { setLoading(false); }
  };

  const handleStep1 = async () => {
    const otpStr = otp.join('');
    if (otpStr.length !== 6) { toast.error('Please enter the complete 6-digit OTP'); return; }
    setLoading(true);
    try {
      const res = await verifyOtp({ email, otp: otpStr });
      setResetToken(res.data.reset_token);
      toast.success('OTP verified!');
      setStep(2);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Invalid OTP');
    } finally { setLoading(false); }
  };

  const handleStep2 = async () => {
    if (!newPassword || newPassword.length < 6) { toast.error('Password must be at least 6 characters'); return; }
    if (newPassword !== confirmPassword) { toast.error('Passwords do not match'); return; }
    setLoading(true);
    try {
      await resetPassword({ token: resetToken, new_password: newPassword });
      toast.success('Password reset successfully!');
      navigate('/login');
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Failed to reset password');
    } finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-background">
      <ParticleBackground />
      <div className="absolute top-1/3 left-1/3 w-80 h-80 bg-primary/10 rounded-full blur-3xl pointer-events-none" />

      <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="w-full max-w-md mx-4 z-10">
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-gradient-primary flex items-center justify-center shadow-glow-primary mb-4">
            <Zap size={28} className="text-white" fill="white" />
          </div>
          <h1 className="text-3xl font-black text-gradient">FinVue</h1>
        </div>

        <div className="glass-card p-8">
          {/* Stepper */}
          <div className="flex items-center mb-8">
            {steps.map((s, i) => (
              <div key={i} className="flex items-center flex-1 last:flex-none">
                <div className="flex flex-col items-center">
                  <div
                    className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold text-white transition-all duration-300"
                    style={{ background: i < step ? 'hsl(158, 64%, 52%)' : i === step ? 'linear-gradient(135deg, hsl(239,84%,67%), hsl(199,89%,48%))' : 'rgba(255,255,255,0.1)' }}
                  >
                    {i < step ? <CheckCircle2 size={14} /> : i + 1}
                  </div>
                  <span className={`text-xs mt-1 whitespace-nowrap ${i === step ? 'text-primary' : 'text-muted-foreground'}`}>{s}</span>
                </div>
                {i < 2 && <div className="flex-1 h-px mx-2 mb-4 transition-all duration-300" style={{ background: i < step ? 'hsl(158, 64%, 52%)' : 'rgba(255,255,255,0.1)' }} />}
              </div>
            ))}
          </div>

          <AnimatePresence mode="wait">
            {step === 0 && (
              <motion.div key="step0" variants={stepVariants} initial="hidden" animate="show" exit="exit" className="space-y-4">
                <h2 className="text-xl font-bold text-foreground">Forgot password?</h2>
                <p className="text-sm text-muted-foreground">Enter your email and we'll send you a verification code.</p>
                <div>
                  <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Email Address</label>
                  <div className="relative">
                    <Mail size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
                    <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" className="fin-input pl-10" onKeyDown={(e) => e.key === 'Enter' && handleStep0()} />
                  </div>
                </div>
                <button onClick={handleStep0} disabled={loading} className="btn-gradient w-full py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2">
                  {loading ? <><Loader2 size={16} className="animate-spin" /> Sending...</> : 'Send OTP'}
                </button>
              </motion.div>
            )}
            {step === 1 && (
              <motion.div key="step1" variants={stepVariants} initial="hidden" animate="show" exit="exit" className="space-y-4">
                <h2 className="text-xl font-bold text-foreground">Enter verification code</h2>
                <p className="text-sm text-muted-foreground">We sent a 6-digit code to <span className="text-primary font-medium">{email}</span></p>
                <div className="flex gap-2 justify-between">
                  {otp.map((digit, i) => (
                    <input key={i} ref={(el) => { otpRefs.current[i] = el; }} type="text" inputMode="numeric" maxLength={1} value={digit} onChange={(e) => handleOtpChange(i, e.target.value)} onKeyDown={(e) => handleOtpKeyDown(i, e)} className="w-11 h-12 text-center text-lg font-bold rounded-xl fin-input" />
                  ))}
                </div>
                <button onClick={handleStep1} disabled={loading} className="btn-gradient w-full py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2">
                  {loading ? <><Loader2 size={16} className="animate-spin" /> Verifying...</> : 'Verify OTP'}
                </button>
              </motion.div>
            )}
            {step === 2 && (
              <motion.div key="step2" variants={stepVariants} initial="hidden" animate="show" exit="exit" className="space-y-4">
                <h2 className="text-xl font-bold text-foreground">Set new password</h2>
                <p className="text-sm text-muted-foreground">Choose a strong password for your account.</p>
                {[{ val: newPassword, set: setNewPassword, label: 'New Password' }, { val: confirmPassword, set: setConfirmPassword, label: 'Confirm Password' }].map(({ val, set, label }) => (
                  <div key={label}>
                    <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">{label}</label>
                    <div className="relative">
                      <Lock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
                      <input type="password" value={val} onChange={(e) => set(e.target.value)} placeholder="••••••••" className="fin-input pl-10" />
                    </div>
                  </div>
                ))}
                <button onClick={handleStep2} disabled={loading} className="btn-gradient w-full py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2">
                  {loading ? <><Loader2 size={16} className="animate-spin" /> Resetting...</> : 'Reset Password'}
                </button>
              </motion.div>
            )}
          </AnimatePresence>

          <div className="mt-6 text-center">
            <Link to="/login" className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors">
              <ArrowLeft size={14} /> Back to login
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default ForgotPassword;
