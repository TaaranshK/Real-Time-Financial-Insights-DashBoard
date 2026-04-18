import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, Variants } from 'framer-motion';
import { Eye, EyeOff, Mail, Lock, User, Phone, Zap, Loader2 } from 'lucide-react';
import toast from 'react-hot-toast';
import { registerUser } from '@/lib/api';
import ParticleBackground from '@/components/ParticleBackground';

interface FormData {
  first_name: string; last_name: string; username: string;
  email: string; phone: string; password: string; confirm_password: string;
}
interface Errors { [key: string]: string; }

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.06 } },
};
const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const Register: React.FC = () => {
  const [form, setForm] = useState<FormData>({ first_name: '', last_name: '', username: '', email: '', phone: '', password: '', confirm_password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Errors>({});
  const navigate = useNavigate();

  const validate = () => {
    const e: Errors = {};
    if (!form.first_name.trim()) e.first_name = 'First name is required';
    if (!form.username.trim()) e.username = 'Username is required';
    if (!form.email.trim()) e.email = 'Email is required';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) e.email = 'Invalid email format';
    if (!form.password) e.password = 'Password is required';
    else if (form.password.length < 6) e.password = 'Password must be at least 6 characters';
    if (form.password !== form.confirm_password) e.confirm_password = 'Passwords do not match';
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  const handleChange = (field: keyof FormData, value: string) => {
    setForm({ ...form, [field]: value });
    if (errors[field]) setErrors({ ...errors, [field]: '' });
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!validate()) return;
    setLoading(true);
    try {
      await registerUser({ username: form.username, email: form.email, password: form.password, first_name: form.first_name, last_name: form.last_name, phone: form.phone });
      toast.success('Account created successfully! Please sign in.');
      navigate('/login');
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Registration failed. Please try again.');
    } finally { setLoading(false); }
  };

  const textFields = [
    { id: 'first_name', label: 'First Name', icon: User, type: 'text', placeholder: 'John', half: true },
    { id: 'last_name', label: 'Last Name', icon: User, type: 'text', placeholder: 'Doe', half: true },
    { id: 'username', label: 'Username', icon: User, type: 'text', placeholder: 'johndoe', half: false },
    { id: 'email', label: 'Email Address', icon: Mail, type: 'email', placeholder: 'you@example.com', half: false },
    { id: 'phone', label: 'Phone (optional)', icon: Phone, type: 'tel', placeholder: '+1234567890', half: false },
  ];

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-background py-12">
      <ParticleBackground />
      <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none" />

      <motion.div variants={containerVariants} initial="hidden" animate="show" className="w-full max-w-lg mx-4 z-10">
        <motion.div variants={itemVariants} className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-gradient-primary flex items-center justify-center shadow-glow-primary mb-4">
            <Zap size={28} className="text-white" fill="white" />
          </div>
          <h1 className="text-3xl font-black text-gradient">FinVue</h1>
          <p className="text-muted-foreground text-sm mt-1">Create your account to get started</p>
        </motion.div>

        <motion.div variants={itemVariants} className="glass-card p-8">
          <h2 className="text-xl font-bold text-foreground mb-6">Create account</h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              {textFields.filter(f => f.half).map(({ id, label, icon: Icon, type, placeholder }) => (
                <motion.div key={id} variants={itemVariants}>
                  <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">{label}</label>
                  <div className="relative">
                    <Icon size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
                    <input type={type} value={form[id as keyof FormData]} onChange={(e) => handleChange(id as keyof FormData, e.target.value)} placeholder={placeholder} className="fin-input pl-9 text-sm" />
                  </div>
                  {errors[id] && <p className="text-xs text-loss mt-1">{errors[id]}</p>}
                </motion.div>
              ))}
            </div>
            {textFields.filter(f => !f.half).map(({ id, label, icon: Icon, type, placeholder }) => (
              <motion.div key={id} variants={itemVariants}>
                <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">{label}</label>
                <div className="relative">
                  <Icon size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
                  <input type={type} value={form[id as keyof FormData]} onChange={(e) => handleChange(id as keyof FormData, e.target.value)} placeholder={placeholder} className="fin-input pl-10" autoComplete={type === 'email' ? 'email' : undefined} />
                </div>
                {errors[id] && <p className="text-xs text-loss mt-1">{errors[id]}</p>}
              </motion.div>
            ))}
            {[{ id: 'password', label: 'Password' }, { id: 'confirm_password', label: 'Confirm Password' }].map(({ id, label }) => (
              <motion.div key={id} variants={itemVariants}>
                <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">{label}</label>
                <div className="relative">
                  <Lock size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
                  <input type={showPassword ? 'text' : 'password'} value={form[id as keyof FormData]} onChange={(e) => handleChange(id as keyof FormData, e.target.value)} placeholder="••••••••" className="fin-input pl-10 pr-10" />
                  {id === 'password' && (
                    <button type="button" onClick={() => setShowPassword(!showPassword)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors">
                      {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                    </button>
                  )}
                </div>
                {errors[id] && <p className="text-xs text-loss mt-1">{errors[id]}</p>}
              </motion.div>
            ))}
            <motion.div variants={itemVariants}>
              <button type="submit" disabled={loading} className="btn-gradient w-full py-3 rounded-xl text-sm font-semibold flex items-center justify-center gap-2 mt-2">
                {loading ? <><Loader2 size={16} className="animate-spin" /> Creating account...</> : 'Create Account'}
              </button>
            </motion.div>
          </form>
          <p className="text-center text-sm text-muted-foreground mt-6">
            Already have an account?{' '}
            <Link to="/login" className="text-primary hover:text-primary/80 font-medium transition-colors">Sign in</Link>
          </p>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Register;
