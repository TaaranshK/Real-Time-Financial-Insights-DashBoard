import { useState } from 'react';
import { motion, Variants } from 'framer-motion';
import { User, Lock, Shield, Loader2, Check, Eye, EyeOff } from 'lucide-react';
import toast from 'react-hot-toast';
import { useAuth } from '@/contexts/AuthContext';
import { updateProfile, changePassword } from '@/lib/api';

const sectionVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.12 } },
};

const Settings: React.FC = () => {
  const { user, updateUser } = useAuth();

  // Profile form
  const [username, setUsername] = useState(user?.username ?? '');
  const [firstName, setFirstName] = useState(user?.first_name ?? '');
  const [lastName, setLastName] = useState(user?.last_name ?? '');
  const [phone, setPhone] = useState(user?.phone ?? '');
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileSaved, setProfileSaved] = useState(false);

  // Password form
  const [currentPwd, setCurrentPwd] = useState('');
  const [newPwd, setNewPwd] = useState('');
  const [confirmPwd, setConfirmPwd] = useState('');
  const [pwdLoading, setPwdLoading] = useState(false);
  const [showPwd, setShowPwd] = useState(false);

  const handleSaveProfile = async () => {
    setProfileLoading(true);
    try {
      const res = await updateProfile({ username, first_name: firstName, last_name: lastName, phone });
      updateUser(res.data?.user ?? res.data);
      toast.success('Profile updated successfully!');
      setProfileSaved(true);
      setTimeout(() => setProfileSaved(false), 2000);
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Failed to update profile');
    } finally { setProfileLoading(false); }
  };

  const handleChangePassword = async () => {
    if (!currentPwd || !newPwd || !confirmPwd) { toast.error('Please fill all password fields'); return; }
    if (newPwd.length < 6) { toast.error('New password must be at least 6 characters'); return; }
    if (newPwd !== confirmPwd) { toast.error('Passwords do not match'); return; }
    setPwdLoading(true);
    try {
      await changePassword({ current_password: currentPwd, new_password: newPwd });
      toast.success('Password changed successfully!');
      setCurrentPwd(''); setNewPwd(''); setConfirmPwd('');
    } catch (err: unknown) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error.response?.data?.detail ?? 'Failed to change password');
    } finally { setPwdLoading(false); }
  };

  const memberSince = user?.created_at
    ? new Date(user.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'long' })
    : 'N/A';

  return (
    <div className="p-6 max-w-3xl mx-auto">
      <motion.h1 initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-2xl font-black text-foreground mb-6">
        Settings
      </motion.h1>

      <motion.div variants={containerVariants} initial="hidden" animate="show" className="space-y-6">
        {/* Account Info */}
        <motion.div variants={sectionVariants} className="glass-card p-6">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-10 h-10 rounded-xl bg-accent/15 flex items-center justify-center">
              <Shield size={18} className="text-accent" />
            </div>
            <h2 className="font-bold text-foreground">Account Information</h2>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            <div className="p-3 rounded-xl bg-white/[0.03] border border-white/5">
              <p className="text-xs text-muted-foreground mb-1">Email</p>
              <p className="text-sm font-medium text-foreground truncate">{user?.email}</p>
            </div>
            <div className="p-3 rounded-xl bg-white/[0.03] border border-white/5">
              <p className="text-xs text-muted-foreground mb-1">Role</p>
              <span className="text-xs px-2 py-1 rounded-full bg-primary/15 text-primary font-medium capitalize">{user?.role ?? 'User'}</span>
            </div>
            <div className="p-3 rounded-xl bg-white/[0.03] border border-white/5">
              <p className="text-xs text-muted-foreground mb-1">Member Since</p>
              <p className="text-sm font-medium text-foreground">{memberSince}</p>
            </div>
          </div>
        </motion.div>

        {/* Profile Section */}
        <motion.div variants={sectionVariants} className="glass-card p-6">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-10 h-10 rounded-xl bg-primary/15 flex items-center justify-center">
              <User size={18} className="text-primary" />
            </div>
            <h2 className="font-bold text-foreground">Profile Details</h2>
          </div>
          <div className="grid grid-cols-2 gap-4 mb-4">
            {[
              { label: 'First Name', value: firstName, set: setFirstName, placeholder: 'John' },
              { label: 'Last Name', value: lastName, set: setLastName, placeholder: 'Doe' },
            ].map(({ label, value, set, placeholder }) => (
              <div key={label}>
                <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">{label}</label>
                <input value={value} onChange={(e) => set(e.target.value)} placeholder={placeholder} className="fin-input" />
              </div>
            ))}
          </div>
          <div className="grid grid-cols-2 gap-4 mb-5">
            {[
              { label: 'Username', value: username, set: setUsername, placeholder: 'johndoe' },
              { label: 'Phone', value: phone, set: setPhone, placeholder: '+1234567890' },
            ].map(({ label, value, set, placeholder }) => (
              <div key={label}>
                <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">{label}</label>
                <input value={value} onChange={(e) => set(e.target.value)} placeholder={placeholder} className="fin-input" />
              </div>
            ))}
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.97 }}
            onClick={handleSaveProfile}
            disabled={profileLoading}
            className="btn-gradient px-6 py-2.5 rounded-xl text-sm font-semibold flex items-center gap-2"
          >
            {profileLoading ? (
              <><Loader2 size={15} className="animate-spin" /> Saving...</>
            ) : profileSaved ? (
              <><Check size={15} /> Saved!</>
            ) : (
              'Save Changes'
            )}
          </motion.button>
        </motion.div>

        {/* Change Password */}
        <motion.div variants={sectionVariants} className="glass-card p-6">
          <div className="flex items-center gap-3 mb-5">
            <div className="w-10 h-10 rounded-xl bg-warning/15 flex items-center justify-center">
              <Lock size={18} className="text-warning" />
            </div>
            <h2 className="font-bold text-foreground">Change Password</h2>
          </div>
          <div className="space-y-4 mb-5">
            <div>
              <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">Current Password</label>
              <div className="relative">
                <Lock size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
                <input type={showPwd ? 'text' : 'password'} value={currentPwd} onChange={(e) => setCurrentPwd(e.target.value)} placeholder="••••••••" className="fin-input pl-10 pr-10" />
                <button type="button" onClick={() => setShowPwd(!showPwd)} className="absolute right-3.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors">
                  {showPwd ? <EyeOff size={15} /> : <Eye size={15} />}
                </button>
              </div>
            </div>
            {[
              { label: 'New Password', value: newPwd, set: setNewPwd },
              { label: 'Confirm New Password', value: confirmPwd, set: setConfirmPwd },
            ].map(({ label, value, set }) => (
              <div key={label}>
                <label className="block text-xs font-medium text-muted-foreground mb-1.5 uppercase tracking-wide">{label}</label>
                <div className="relative">
                  <Lock size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
                  <input type="password" value={value} onChange={(e) => set(e.target.value)} placeholder="••••••••" className="fin-input pl-10" />
                </div>
              </div>
            ))}
          </div>
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.97 }}
            onClick={handleChangePassword}
            disabled={pwdLoading}
            className="btn-gradient px-6 py-2.5 rounded-xl text-sm font-semibold flex items-center gap-2"
          >
            {pwdLoading ? <><Loader2 size={15} className="animate-spin" /> Updating...</> : 'Update Password'}
          </motion.button>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Settings;
