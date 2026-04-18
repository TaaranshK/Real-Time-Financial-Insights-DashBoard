# FinVue Frontend - Configuration & Customization Guide

## 🎨 Design System

### Color Palette

Located in `frontend/src/index.css`:

```css
/* Primary Colors */
--primary: 239 84% 67%; /* Indigo */
--accent: 199 89% 48%; /* Cyan */
--foreground: 210 40% 96%; /* Light text */

/* Status Colors */
--profit: 158 64% 52%; /* Green - Profit */
--loss: 350 89% 60%; /* Red - Loss */
--warning: 38 92% 50%; /* Amber - Warning */

/* Backgrounds */
--background: 222 47% 3%; /* Very dark blue */
--card: 222 40% 6%; /* Dark card */

/* Glassmorphism */
--glass-bg: rgba(255, 255, 255, 0.04);
--glass-border: rgba(255, 255, 255, 0.08);
--glass-hover: rgba(255, 255, 255, 0.07);
```

### Gradients

```css
--gradient-primary: linear-gradient(
  135deg,
  hsl(239, 84%, 67%),
  hsl(280, 87%, 65%),
  hsl(199, 89%, 48%)
);
--gradient-success: linear-gradient(
  135deg,
  hsl(158, 64%, 40%),
  hsl(158, 64%, 52%)
);
--gradient-danger: linear-gradient(
  135deg,
  hsl(350, 89%, 45%),
  hsl(350, 89%, 60%)
);
```

---

## 📦 Utility Classes

### Glass Card Component

```html
<div class="glass-card p-6">
  <!-- Glassmorphism effect: transparent background with blur -->
</div>
```

### Button Styles

```html
<!-- Primary Gradient Button -->
<button class="btn-gradient">Action</button>

<!-- Pulsing Button (for animations) -->
<button class="btn-pulse">Analyze</button>
```

### Input Fields

```html
<input type="text" class="fin-input" placeholder="Enter value" />
```

### Status Badges

```html
<!-- Profit Badge (Green) -->
<span class="badge-profit">+5.2%</span>

<!-- Loss Badge (Red) -->
<span class="badge-loss">-2.1%</span>

<!-- Neutral Badge (Amber) -->
<span class="badge-neutral">HOLD</span>
```

---

## 🔄 API Configuration

### Endpoint Configuration

File: `frontend/src/lib/api.ts`

```typescript
const BASE_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});
```

**To change backend URL:**

1. Update `BASE_URL` in `api.ts`
2. Or set `VITE_API_BASE_URL` environment variable

### Add New Endpoint

```typescript
export const newFeature = (data: any) =>
  api.post("/api/feature/endpoint", data);
```

---

## 🔐 Authentication Context

### Using Auth Context

```typescript
import { useAuth } from '@/contexts/AuthContext';

function MyComponent() {
  const { user, accessToken, isLoading, login, logout } = useAuth();

  if (isLoading) return <LoadingSpinner />;
  if (!accessToken) return <Navigate to="/login" />;

  return <div>Welcome, {user?.first_name}!</div>;
}
```

### Auth Flow

1. User logs in → `login(token, refreshToken, user)` called
2. Token stored in localStorage
3. Interceptor adds token to all requests
4. If 401 → auto logout and redirect to /login

---

## 🎬 Animation Patterns

### Framer Motion Examples

Located in various `pages/*.tsx` files:

```typescript
import { motion, Variants } from 'framer-motion';

const containerVariants: Variants = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.4 } },
};

// Usage
<motion.div variants={containerVariants} initial="hidden" animate="show">
  <motion.div variants={itemVariants}>Content</motion.div>
</motion.div>
```

### Common Animations

- **Stagger**: Children animate one after another
- **Scale**: Elements grow/shrink on hover
- **Fade**: Opacity transitions
- **Slide**: Y-axis position changes

---

## 📊 Dashboard Components

### Stats Card Component

```typescript
function StatCard({
  icon: Icon,
  label,
  value,
  isCurrency,
  isProfit
}) {
  const count = useCountUp(Math.abs(value)); // Animated counter

  return (
    <motion.div variants={cardVariants} whileHover={{ y: -3 }}>
      {/* Card content */}
    </motion.div>
  );
}
```

### Charts Integration

Uses Recharts with shared styling:

```typescript
<ResponsiveContainer width="100%" height={300}>
  <AreaChart data={chartData}>
    <Area
      type="monotone"
      dataKey="value"
      fill="#6366f1"
      stroke="#6366f1"
      fillOpacity={0.1}
    />
  </AreaChart>
</ResponsiveContainer>
```

---

## 🛣️ Routing Structure

### Route Configuration

File: `frontend/src/App.tsx`

```typescript
<Routes>
  {/* Public routes */}
  <Route path="/login" element={<Login />} />
  <Route path="/register" element={<Register />} />
  <Route path="/forgot-password" element={<ForgotPassword />} />

  {/* Protected routes */}
  <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
    <Route path="/" element={<Dashboard />} />
    <Route path="/portfolio" element={<Portfolio />} />
    <Route path="/holdings" element={<Holdings />} />
    <Route path="/market-analysis" element={<MarketAnalysis />} />
    <Route path="/settings" element={<Settings />} />
  </Route>
</Routes>
```

### Add New Page

1. Create file: `frontend/src/pages/NewPage.tsx`
2. Add route in `App.tsx`
3. Add navigation link in `frontend/src/components/Sidebar.tsx`

---

## 🔔 Toast Notifications

### Usage

```typescript
import toast from "react-hot-toast";

// Success
toast.success("Operation successful");

// Error
toast.error("Something went wrong");

// Loading
const toastId = toast.loading("Processing...");
toast.success("Done!", { id: toastId });
```

### Styling

Configured in `App.tsx`:

```typescript
<Toaster
  position="top-right"
  toastOptions={{
    style: {
      background: 'rgba(15, 23, 42, 0.95)',
      border: '1px solid rgba(255,255,255,0.1)',
      color: 'hsl(210, 40%, 96%)',
      borderRadius: '12px',
      backdropFilter: 'blur(20px)',
    },
  }}
/>
```

---

## 🧹 Code Style & Conventions

### Component Structure

```typescript
import { useState, useEffect } from 'react';
import { motion, Variants } from 'framer-motion';
import { useAuth } from '@/contexts/AuthContext';
import { getApiData } from '@/lib/api';

interface Props { }
interface State { }

const MyComponent: React.FC<Props> = () => {
  const { user } = useAuth();
  const [state, setState] = useState<State>();

  useEffect(() => {
    loadData();
  }, []);

  return <div>Component</div>;
};

export default MyComponent;
```

### File Naming

- Components: `PascalCase.tsx`
- Utils: `camelCase.ts`
- Constants: `UPPER_CASE`

### Import Organization

1. External packages
2. Internal contexts
3. Internal utilities
4. Styles

---

## 📱 Responsive Design

### Breakpoints (Tailwind)

- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px
- `2xl`: 1536px

### Mobile Considerations

- Sidebar → Bottom tab bar on mobile
- Charts → Responsive container
- Cards → Stack vertically on mobile
- Inputs → Full width on mobile

### Example

```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  {/* 1 col mobile, 2 md, 3 lg */}
</div>
```

---

## 🧪 Component Testing

### Manual Testing Checklist

- [ ] Component renders correctly
- [ ] Interactions work (clicks, inputs)
- [ ] API calls succeed
- [ ] Error states display properly
- [ ] Loading states show correctly
- [ ] Animations are smooth
- [ ] Mobile responsive
- [ ] Dark theme looks good

### React DevTools

- Install React DevTools browser extension
- Inspect component props and state
- Performance profiling available

---

## 🚀 Build & Optimization

### Development Build

```bash
npm run dev        # Start dev server
npm run build:dev  # Build in dev mode
```

### Production Build

```bash
npm run build      # Optimized build
npm run preview    # Preview production build
```

### Build Output

```
dist/
├── index.html         # Main HTML
├── assets/
│   ├── index-*.css    # Minified CSS (11.95 KB gzipped)
│   └── index-*.js     # Minified JS (251.93 KB gzipped)
```

### Optimization Tips

- Use dynamic imports: `React.lazy(() => import('./Page'))`
- Optimize images with next-gen formats
- Enable gzip compression on server
- Cache static assets with long expiry

---

## 🐛 Debugging

### Browser DevTools

- **Console**: Check for errors and warnings
- **Network**: Monitor API calls
- **Application**: View localStorage (tokens, user data)
- **Performance**: Profile slow components

### React DevTools

- Inspect component tree
- Check prop and state values
- Trace renders and re-renders
- Use Profiler for performance

### Common Issues

```typescript
// Issue: Token not sent in requests
// Solution: Clear localStorage, re-login

// Issue: CORS errors
// Solution: Verify backend allows frontend origin

// Issue: Components not updating
// Solution: Check dependency arrays in useEffect

// Issue: Animation jank
// Solution: Use transform/opacity, not height/width
```

---

## 📚 Useful Libraries

- **React Query**: Data fetching & caching (tanstack/react-query)
- **React Hook Form**: Form state management
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Animation library
- **Recharts**: Chart library
- **Lucide React**: Icon library
- **Axios**: HTTP client
- **React Hot Toast**: Toast notifications

---

## 🔗 Useful Links

- [React Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Framer Motion](https://www.framer.com/motion/)
- [TypeScript](https://www.typescriptlang.org/)
- [Vite](https://vitejs.dev)
- [Recharts](https://recharts.org)

---

**Last Updated**: March 9, 2026
**Version**: 1.0.0
