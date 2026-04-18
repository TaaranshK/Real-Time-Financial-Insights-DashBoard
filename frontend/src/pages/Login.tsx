import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, Variants } from 'framer-motion';
import { Eye, EyeOff, Mail, Lock, Zap, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { loginUser } from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';
import ParticleBackground from '@/components/ParticleBackground';

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.08 },
  },
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const Login: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!email || !password) { toast.error('Please fill in all fields'); return; }
    setLoading(true);
    try {
      const res = await loginUser({ email, password });
      const { access_token, refresh_token, user } = res.data.data;
      login(access_token, refresh_token, user);
      toast.success(`Welcome back, ${user.first_name ?? user.username}!`);
      navigate('/');
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Login failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-background">
      <ParticleBackground />
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/10 rounded-full blur-3xl pointer-events-none" />

      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="show"
        className="w-full max-w-md mx-4 z-10"
      >
        <motion.div variants={itemVariants} className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-gradient-primary flex items-center justify-center shadow-glow-primary mb-4">
            <Zap size={28} className="text-white" fill="white" />
          </div>
          <h1 className="text-3xl font-black text-gradient">FinVue</h1>
          <p className="text-muted-foreground text-sm mt-1">Your Financial Intelligence Platform</p>
        </motion.div>

        <motion.div variants={itemVariants} className="glass-card p-8">
          <h2 className="text-xl font-bold text-foreground mb-2">Welcome back</h2>
          <p className="text-muted-foreground text-sm mb-6">Sign in to your account to continue</p>

          <form onSubmit={handleSubmit} className="space-y-4">
            <motion.div variants={itemVariants}>
              <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Email Address</label>
              <div className="relative">
                <Mail size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@example.com" className="fin-input pl-10" autoComplete="email" />
              </div>
            </motion.div>

            <motion.div variants={itemVariants}>
              <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Password</label>
              <div className="relative">
                <Lock size={16} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
                <input type={showPassword ? 'text' : 'password'} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" className="fin-input pl-10 pr-10" autoComplete="current-password" />
                <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors">
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              <div className="flex justify-end mt-1.5">
                <Link to="/forgot-password" className="text-xs text-primary hover:text-primary/80 transition-colors">Forgot password?</Link>
              </div>
            </motion.div>

            <motion.div variants={itemVariants}>
              <button type="submit" disabled={loading} className="btn-gradient w-full py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2 mt-2">
                {loading ? <><Loader2 size={16} className="animate-spin" /> Signing in...</> : 'Sign In'}
              </button>
            </motion.div>
          </form>

          <motion.p variants={itemVariants} className="text-center text-sm text-muted-foreground mt-6">
            Don't have an account?{' '}
            <Link to="/register" className="text-primary hover:text-primary/80 font-medium transition-colors">Create account</Link>
          </motion.p>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Login;
