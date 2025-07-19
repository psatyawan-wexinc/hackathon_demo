# shadcn/ui with Tailwind v4 Design System Guidelines

This document outlines design principles and implementation guidelines for applications using shadcn/ui with Tailwind v4. These guidelines ensure consistency, accessibility, and best practices throughout the UI development process.

## Core Design Principles

### 1. Typography System: 4 Sizes, 2 Weights
- **4 Font Sizes Only**:
  - Size 1: Large headings
  - Size 2: Subheadings/Important content
  - Size 3: Body text
  - Size 4: Small text/labels
- **2 Font Weights Only**:
  - Semibold: For headings and emphasis
  - Regular: For body text and general content
- **Consistent Hierarchy**: Maintain clear visual hierarchy with limited options

### 2. 8pt Grid System
- **All spacing values must be divisible by 8 or 4**
- **Examples**:
  - Instead of 25px padding → Use 24px (divisible by 8)
  - Instead of 11px margin → Use 12px (divisible by 4)
- **Consistent Rhythm**: Creates visual harmony throughout the interface

### 3. 60/30/10 Color Rule
- **60%**: Neutral color (white/light gray)
- **30%**: Complementary color (dark gray/black)
- **10%**: Main brand/accent color (e.g., red, blue)
- **Color Balance**: Prevents visual stress while maintaining hierarchy

### 4. Clean Visual Structure
- **Logical Grouping**: Related elements should be visually connected
- **Deliberate Spacing**: Spacing between elements should follow the grid system
- **Alignment**: Elements should be properly aligned within their containers
- **Simplicity Over Flashiness**: Focus on clarity and function first

## Foundation

### Tailwind v4 Integration
- **Use Tailwind CSS v4 for styling**: Leverage the latest Tailwind features including the new @theme directive, dynamic utility values, and OKLCH colors. [Tailwind CSS v4 Documentation](mdc:https://tailwindcss.com/docs)
- **Modern browsing features**: Tailwind v4 uses bleeding-edge browser features and is designed for modern browsers.
- **Simplified installation**: Fewer dependencies, zero configuration required in many cases.
- **shadcn/ui v4 demo**: Reference the demo site for component examples. [shadcn/ui v4 Demo](mdc:https://v4.shadcn.com/)

### New CSS Structure
- **Replace @layer base with @theme directive**:
  ```css
  /* Old approach in v3 */
  @layer base {
    :root {
      --background: 0 0% 100%;
      --foreground: 0 0% 3.9%;
    }
  }
  
  /* New approach in v4 */
  @theme {
    --color-background: hsl(var(--background));
    --color-foreground: hsl(var(--foreground));
  }
  ```
- **Tailwind imports**: Use `@import "tailwindcss"` instead of `@tailwind base`
- **Container queries**: Built-in support without plugins
- **OKLCH color format**: Updated from HSL for better color perception

## Typography System

### Font Sizes & Weights
- **Strictly limit to 4 distinct sizes**:
  - Size 1: Large headings (largest)
  - Size 2: Subheadings
  - Size 3: Body text
  - Size 4: Small text/labels (smallest)
- **Only use 2 font weights**:
  - Semibold: For headings and emphasis
  - Regular: For body text and most UI elements
- **Common mistakes to avoid**:
  - Using more than 4 font sizes
  - Introducing additional font weights
  - Inconsistent size application

### Typography Implementation
- **Reference shadcn's typography primitives** for consistent text styling
- **Use monospace variant** for numerical data when appropriate
- **data-slot attribute**: Every shadcn/ui primitive now has a data-slot attribute for styling
- **Maintain hierarchy** using consistent sizing patterns

## 8pt Grid System

### Spacing Guidelines
- **All spacing values MUST be divisible by 8 or 4**:
  - ✅ DO: Use 8, 16, 24, 32, 40, 48, etc.
  - ❌ DON'T: Use 25, 11, 7, 13, etc.

- **Practical examples**:
  - Instead of 25px padding → Use 24px (divisible by 8)
  - Instead of 11px margin → Use 12px (divisible by 4)
  - Instead of 15px gap → Use 16px (divisible by 8)

- **Use Tailwind's spacing utilities**:
  - p-4 (16px), p-6 (24px), p-8 (32px)
  - m-2 (8px), m-4 (16px), m-6 (24px)
  - gap-2 (8px), gap-4 (16px), gap-8 (32px)

- **Why this matters**:
  - Creates visual harmony
  - Simplifies decision-making
  - Establishes predictable patterns

### Implementation
- **Tailwind v4 dynamic spacing**: Spacing utilities accept any value without arbitrary syntax
- **Consistent component spacing**: Group related elements with matching gap values
- **Check responsive behavior**: Ensure grid system holds at all breakpoints

## 60/30/10 Color Rule

### Color Distribution
- **60%**: neutral color (bg-background)
  - Usually white or light gray in light mode
  - Dark gray or black in dark mode
  - Used for primary backgrounds, cards, containers

- **30%**: complementary color (text-foreground)
  - Usually dark gray or black in light mode
  - Light gray or white in dark mode
  - Used for text, icons, subtle UI elements

- **10%**: accent color (brand color)
  - Your primary brand color (red, blue, etc.)
  - Used sparingly for call-to-action buttons, highlights, important indicators
  - Avoid overusing to prevent visual stress

### Common Mistakes
- ❌ Overusing accent colors creates visual stress
- ❌ Not enough contrast between background and text
- ❌ Too many competing accent colors (stick to one primary accent)

### Implementation with shadcn/ui
- **Background/foreground convention**: Each component uses the background/foreground pattern
- **CSS variables in globals.css**:
  ```css
  :root {
    --background: oklch(1 0 0);
    --foreground: oklch(0.145 0 0);
    --primary: oklch(0.205 0 0);
    --primary-foreground: oklch(0.985 0 0);
    /* Additional variables */
  }
  
  @theme {
    --color-background: var(--background);
    --color-foreground: var(--foreground);
    /* Register other variables */
  }
  ```
- **OKLCH color format**: More accessible colors, especially in dark mode
- **Reserve accent colors** for important elements that need attention

## Component Architecture

### shadcn/ui Component Structure
- **2-layered architecture**:
  1. Structure and behavior layer (Radix UI primitives)
  2. Style layer (Tailwind CSS)
- **Class Variance Authority (CVA)** for variant styling
- **data-slot attribute** for styling component parts

### Implementation
- **Install components individually** using CLI (updated for v4) or manual installation
- **Component customization**: Modify components directly as needed
- **Radix UI primitives**: Base components for accessibility and behavior
- **New-York style**: Default recommended style for new projects (deprecated "default" style)

## Visual Hierarchy

### Design Principles
- **Simplicity over flashiness**: Focus on clarity and usability
- **Emphasis on what matters**: Highlight important elements
- **Reduced cognitive load**: Use consistent terminology and patterns
- **Visual connection**: Connect related UI elements through consistent patterns

### Implementation
- **Use shadcn/ui Blocks** for common UI patterns
- **Maintain consistent spacing** between related elements
- **Align elements properly** within containers
- **Logical grouping** of related functionality

## Installation & Setup

### Project Setup
- **CLI initialization**:
  ```bash
  npx create-next-app@latest my-app
  cd my-app
  npx shadcn-ui@latest init
  ```
- **Manual setup**: Follow the guide at [Manual Installation](mdc:https://ui.shadcn.com/docs/installation/manual)
- **components.json configuration**:
  ```json
  {
    "style": "new-york",
    "rsc": true,
    "tailwind": {
      "config": "",
      "css": "app/globals.css",
      "baseColor": "neutral",
      "cssVariables": true
    },
    "aliases": {
      "components": "@/components",
      "utils": "@/lib/utils"
    }
  }
  ```

### Adding Components
- **Use the CLI**: `npx shadcn-ui@latest add button`
- **Install dependencies**: Required for each component
- **Find components**: [Component Reference](mdc:https://ui.shadcn.com/docs/components)

## Advanced Features

### Dark Mode
- **Updated dark mode colors** for better accessibility using OKLCH
- **Consistent contrast ratios** across light and dark themes
- **Custom variant**: `@custom-variant dark (&:is(.dark *))`

### Container Queries
- **Built-in support** without plugins
- **Responsive components** that adapt to their container size
- **@min-* and @max-* variants** for container query ranges

### Data Visualization
- **Chart components**: Use with consistent styling
- **Consistent color patterns**: Use chart-1 through chart-5 variables

## Experience Design

### Motion & Animation
- **Consider transitions** between screens and states
- **Animation purpose**: Enhance usability, not distract
- **Consistent motion patterns**: Similar elements should move similarly

### Implementation
- **Test experiences** across the entire flow
- **Design with animation in mind** from the beginning
- **Balance speed and smoothness** for optimal user experience

## Resources

- [shadcn/ui Documentation](mdc:https://ui.shadcn.com/docs)
- [Tailwind CSS v4 Documentation](mdc:https://tailwindcss.com/docs)
- [shadcn/ui GitHub Repository](mdc:https://github.com/shadcn/ui)
- [Tailwind v4 Upgrade Guide](mdc:https://tailwindcss.com/docs/upgrade-guide)
- [shadcn/ui v4 Demo](mdc:https://v4.shadcn.com/)
- [Figma Design System](mdc:https://www.figma.com/community/file/1203061493325953101/shadcn-ui-design-system)

## Performance Architecture

### Core Web Vitals Optimization (2025 Standards)
- **Largest Contentful Paint (LCP) < 2.5s**:
  - Implement Early Hints for resource preloading
  - Use `fetchpriority="high"` for hero images
  - Critical CSS inlining with `@layer` directive
  - Optimize image formats: AVIF > WebP > JPEG
  - Implement resource hints: `<link rel="preconnect">`, `<link rel="dns-prefetch">`
  
- **Interaction to Next Paint (INP) < 200ms** (replaced FID in March 2024):
  - Break long tasks with `scheduler.yield()`
  - Implement input debouncing for search/filter operations
  - Use CSS containment: `contain: layout style paint`
  - Optimize event handlers with passive listeners
  - Implement virtual scrolling for large lists

- **Cumulative Layout Shift (CLS) < 0.1**:
  - Reserve space for dynamic content with aspect-ratio
  - Use CSS Grid/Flexbox for stable layouts
  - Implement font-display: optional for critical text
  - Set explicit dimensions for media elements

### Bundle Optimization Strategies
- **Performance Budgets**:
  ```javascript
  // webpack.config.js or vite.config.js
  performance: {
    maxAssetSize: 244000,      // 244KB per asset
    maxEntrypointSize: 244000, // 244KB per entry
    hints: 'error'             // Fail build on budget exceed
  }
  ```

- **Code Splitting Patterns**:
  ```javascript
  // Route-based splitting
  const Dashboard = lazy(() => import('./pages/Dashboard'))
  
  // Component-based splitting
  const HeavyChart = lazy(() => 
    import(/* webpackChunkName: "charts" */ './components/HeavyChart')
  )
  
  // Conditional splitting
  if (userNeedsAdvancedFeatures) {
    const AdvancedModule = await import('./modules/Advanced')
  }
  ```

- **Tree Shaking & Dead Code Elimination**:
  - Use ES6 modules exclusively
  - Enable sideEffects: false in package.json
  - Implement barrel exports carefully
  - Use production builds for proper DCE

### AI-Powered Performance
- **Navigation AI**: Predictive prefetching based on user patterns
- **Real User Monitoring (RUM) AI**: Automated insights and anomaly detection
- **Smart bundling**: AI-driven chunk optimization based on user journeys

## Modern Libraries & Frameworks

### Component Libraries Hierarchy

#### Primary Recommendation: shadcn/ui
- **Approach**: Copy-paste components (not npm package)
- **Benefits**: 
  - Full control over component code
  - No version lock-in or breaking changes
  - Tree-shakes perfectly (only what you use)
  - 66k+ GitHub stars, massive community
- **Installation**: 
  ```bash
  npx shadcn-ui@latest init
  npx shadcn-ui@latest add button card dialog
  ```

#### Headless UI Libraries
1. **Radix UI** (shadcn/ui foundation):
   - Unstyled, accessible primitives
   - WAI-ARIA compliant out-of-the-box
   - Focus management and keyboard navigation
   - Install individually: `npm install @radix-ui/react-dialog`

2. **Ark UI** (Alternative to Radix):
   - State machine-based components
   - Multi-framework support (React, Vue, Solid)
   - 45+ components with consistent API
   - Better for complex state management

3. **React Aria** (Adobe):
   - Most comprehensive accessibility
   - Internationalization built-in
   - Used by Next UI and React Spectrum

### CSS Framework: Tailwind CSS v4
- **Key v4 Features**:
  - Native cascade layers support
  - Lightning CSS under the hood
  - Zero-config setup in most cases
  - Container queries without plugins
  - Dynamic values without arbitrary value syntax

- **OKLCH Color Migration**:
  ```css
  /* Modern color definition */
  @theme {
    --color-primary: oklch(0.7 0.25 250);
    --color-primary-hover: oklch(0.65 0.25 250);
  }
  ```

### Icon Libraries
1. **Lucide React** (Primary):
   - Consistent with shadcn/ui
   - 1000+ icons, tree-shakeable
   - TypeScript support
   ```jsx
   import { Search, Menu, X } from 'lucide-react'
   ```

2. **Radix Icons**:
   - Designed for UI, 15x15 default
   - Perfect for shadcn/ui projects

3. **Heroicons**:
   - By Tailwind team
   - Solid and outline variants

### Animation Libraries

#### Motion Libraries Comparison
1. **Framer Motion** (Most Popular):
   ```jsx
   import { motion } from 'framer-motion'
   
   <motion.div
     initial={{ opacity: 0, y: 20 }}
     animate={{ opacity: 1, y: 0 }}
     transition={{ duration: 0.5 }}
   />
   ```

2. **React Spring** (Physics-based):
   ```jsx
   import { useSpring, animated } from '@react-spring/web'
   
   const styles = useSpring({
     from: { opacity: 0 },
     to: { opacity: 1 }
   })
   ```

3. **Auto-Animate** (Simplest):
   ```jsx
   import autoAnimate from '@formkit/auto-animate'
   
   useEffect(() => {
     parent.current && autoAnimate(parent.current)
   }, [parent])
   ```

4. **Lottie React**:
   - For complex After Effects animations
   - JSON-based, designer-friendly

### Modern UI Enhancements
- **Magic UI**: 50+ pre-built animated components
- **Aceternity UI**: Advanced animations and effects
- **Chadcn Blocks**: Pre-built page sections and layouts

## Modern Font Systems

### Variable Fonts Architecture
Variable fonts provide multiple weights and styles in a single file, dramatically reducing HTTP requests and improving performance.

#### Primary Font Recommendations

1. **Inter** (UI Standard):
   ```css
   @font-face {
     font-family: 'Inter';
     src: url('/fonts/Inter.var.woff2') format('woff2');
     font-weight: 100 900;
     font-display: swap;
   }
   ```
   - 9 weights in one file
   - Excellent screen rendering
   - Perfect for UI elements

2. **Geist** (Modern Alternative):
   ```css
   /* Next.js font optimization */
   import { GeistSans, GeistMono } from 'geist/font'
   
   export default function Layout() {
     return (
       <html className={`${GeistSans.variable} ${GeistMono.variable}`}>
   ```
   - Created by Vercel
   - Optimized for modern screens
   - Sans and Mono variants

3. **System Font Stack** (Fastest):
   ```css
   font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 
                Roboto, 'Helvetica Neue', Arial, sans-serif;
   ```

### Font Loading Optimization
```css
/* Critical text with fallback */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter.var.woff2') format('woff2');
  font-display: swap; /* or 'optional' for critical text */
  unicode-range: U+0020-007F; /* Latin subset first */
}

/* Preload critical fonts */
<link rel="preload" href="/fonts/Inter.var.woff2" 
      as="font" type="font/woff2" crossorigin>
```

### Typography Performance Rules
1. **Maximum 2 font families** (sans + mono)
2. **Maximum 2-3 weights per family**
3. **Use variable fonts when >2 weights needed**
4. **Subset fonts for non-Latin content**
5. **Self-host for GDPR compliance**

## Advanced Accessibility Patterns

### WCAG 2.2 Compliance Architecture

#### Focus Management System
```jsx
// Focus trap hook for modals/dialogs
import { useFocusTrap } from '@radix-ui/react-focus-scope'

function Modal({ isOpen, children }) {
  const trapRef = useFocusTrap(isOpen)
  
  return (
    <div ref={trapRef} role="dialog" aria-modal="true">
      {children}
    </div>
  )
}
```

#### Live Regions Architecture
```jsx
// Announcer component for dynamic content
function LiveAnnouncer({ message, priority = 'polite' }) {
  return (
    <div 
      role="status" 
      aria-live={priority}
      aria-atomic="true"
      className="sr-only"
    >
      {message}
    </div>
  )
}
```

#### Keyboard Navigation Patterns
```jsx
// Roving tabindex for lists
function NavigableList({ items }) {
  const [focusedIndex, setFocusedIndex] = useState(0)
  
  const handleKeyDown = (e) => {
    switch(e.key) {
      case 'ArrowDown':
        setFocusedIndex(prev => 
          Math.min(prev + 1, items.length - 1)
        )
        break
      case 'ArrowUp':
        setFocusedIndex(prev => Math.max(prev - 1, 0))
        break
    }
  }
  
  return items.map((item, index) => (
    <div
      key={item.id}
      tabIndex={index === focusedIndex ? 0 : -1}
      onKeyDown={handleKeyDown}
    >
      {item.content}
    </div>
  ))
}
```

### AI-Powered Accessibility
- **Automated alt text generation**
- **Color contrast auto-correction**
- **ARIA pattern suggestions**
- **Screen reader testing automation**

## State Management Architecture

### State Management Decision Matrix

| State Type | Scope | Persistence | Recommendation |
|------------|-------|-------------|----------------|
| UI State | Component | No | useState/useReducer |
| Form State | Page | No | React Hook Form |
| Server Cache | Global | Yes | TanStack Query |
| App State | Global | Sometimes | Zustand/Valtio |
| Complex State | Global | Yes | Redux Toolkit |

### Modern State Patterns

#### Local State Optimization
```jsx
// Optimized state updates
const [state, setState] = useState(() => 
  expensiveComputation() // Lazy initial state
)

// Batch updates automatically in React 18+
function handleClick() {
  setState(prev => prev + 1)
  setOtherState(prev => prev + 1)
  // Single re-render
}
```

#### Global State with Zustand
```jsx
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

const useStore = create(
  persist(
    (set) => ({
      user: null,
      theme: 'light',
      setUser: (user) => set({ user }),
      toggleTheme: () => set((state) => ({ 
        theme: state.theme === 'light' ? 'dark' : 'light' 
      }))
    }),
    {
      name: 'app-storage',
      partialize: (state) => ({ theme: state.theme }) // Selective persistence
    }
  )
)
```

#### Server State with TanStack Query
```jsx
// Optimistic updates pattern
const mutation = useMutation({
  mutationFn: updateTodo,
  onMutate: async (newTodo) => {
    await queryClient.cancelQueries({ queryKey: ['todos'] })
    const previousTodos = queryClient.getQueryData(['todos'])
    
    queryClient.setQueryData(['todos'], old => [...old, newTodo])
    
    return { previousTodos }
  },
  onError: (err, newTodo, context) => {
    queryClient.setQueryData(['todos'], context.previousTodos)
  },
  onSettled: () => {
    queryClient.invalidateQueries({ queryKey: ['todos'] })
  }
})
```

## Micro-Frontend Architecture

### Module Federation Setup
```javascript
// webpack.config.js for host app
const ModuleFederationPlugin = require('webpack/lib/container/ModuleFederationPlugin')

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'host',
      remotes: {
        cart: 'cart@http://localhost:3001/remoteEntry.js',
        catalog: 'catalog@http://localhost:3002/remoteEntry.js'
      },
      shared: {
        react: { singleton: true, requiredVersion: '^18.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^18.0.0' }
      }
    })
  ]
}
```

### Cross-MFE Communication
```javascript
// Event bus pattern
class MicroFrontendEventBus {
  constructor() {
    this.events = {}
  }
  
  emit(event, data) {
    window.dispatchEvent(new CustomEvent(`mfe:${event}`, { 
      detail: data 
    }))
  }
  
  on(event, callback) {
    const handler = (e) => callback(e.detail)
    window.addEventListener(`mfe:${event}`, handler)
    return () => window.removeEventListener(`mfe:${event}`, handler)
  }
}

// Shared state pattern
const sharedStore = new Proxy({}, {
  set(target, property, value) {
    target[property] = value
    window.postMessage({ 
      type: 'STATE_UPDATE', 
      key: property, 
      value 
    }, '*')
    return true
  }
})
```

## Component Composition Patterns

### Compound Components
```jsx
// Compound component pattern with context
const TabsContext = createContext()

function Tabs({ children, defaultValue }) {
  const [activeTab, setActiveTab] = useState(defaultValue)
  
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>
      <div role="tablist">{children}</div>
    </TabsContext.Provider>
  )
}

Tabs.List = function TabsList({ children }) {
  return <div className="flex gap-2">{children}</div>
}

Tabs.Tab = function Tab({ value, children }) {
  const { activeTab, setActiveTab } = useContext(TabsContext)
  
  return (
    <button
      role="tab"
      aria-selected={activeTab === value}
      onClick={() => setActiveTab(value)}
    >
      {children}
    </button>
  )
}

// Usage
<Tabs defaultValue="tab1">
  <Tabs.List>
    <Tabs.Tab value="tab1">Tab 1</Tabs.Tab>
    <Tabs.Tab value="tab2">Tab 2</Tabs.Tab>
  </Tabs.List>
</Tabs>
```

### Render Props vs Hooks
```jsx
// Modern hook approach (preferred)
function useToggle(initial = false) {
  const [state, setState] = useState(initial)
  const toggle = useCallback(() => setState(prev => !prev), [])
  return [state, toggle]
}

// Legacy render prop (avoid unless necessary)
function Toggle({ children, initial = false }) {
  const [on, setOn] = useState(initial)
  return children({ on, toggle: () => setOn(!on) })
}
```

### Slot-based Composition
```jsx
// Vue-inspired slots in React
function Card({ header, footer, children }) {
  return (
    <div className="card">
      {header && <div className="card-header">{header}</div>}
      <div className="card-body">{children}</div>
      {footer && <div className="card-footer">{footer}</div>}
    </div>
  )
}

// Usage with explicit slots
<Card
  header={<CardTitle>Title</CardTitle>}
  footer={<CardActions>...</CardActions>}
>
  Content
</Card>
```

## Error Handling & Resilience

### Error Boundary Architecture
```jsx
// Generic error boundary with fallback UI
class ErrorBoundary extends Component {
  state = { hasError: false, error: null }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }
  
  componentDidCatch(error, errorInfo) {
    // Log to error reporting service
    errorReporter.log({ error, errorInfo })
  }
  
  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />
    }
    
    return this.props.children
  }
}

// Async error boundary with retry
function AsyncBoundary({ children, fallback, onError }) {
  return (
    <ErrorBoundary fallback={fallback}>
      <Suspense fallback={<Loading />}>
        {children}
      </Suspense>
    </ErrorBoundary>
  )
}
```

### Circuit Breaker Pattern
```javascript
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5
    this.resetTimeout = options.resetTimeout || 60000
    this.state = 'CLOSED'
    this.failureCount = 0
  }
  
  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.openedAt > this.resetTimeout) {
        this.state = 'HALF_OPEN'
      } else {
        throw new Error('Circuit breaker is OPEN')
      }
    }
    
    try {
      const result = await fn()
      this.onSuccess()
      return result
    } catch (error) {
      this.onFailure()
      throw error
    }
  }
  
  onSuccess() {
    this.failureCount = 0
    this.state = 'CLOSED'
  }
  
  onFailure() {
    this.failureCount++
    if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN'
      this.openedAt = Date.now()
    }
  }
}
```

## Modern CSS Architecture

### CSS-in-JS Alternatives (2025)
With the shift away from runtime CSS-in-JS, modern alternatives include:

1. **CSS Modules + PostCSS**:
   ```css
   /* Button.module.css */
   .button {
     @apply px-4 py-2 rounded-lg font-semibold;
     
     &:hover {
       @apply bg-opacity-90;
     }
     
     &.primary {
       @apply bg-primary text-primary-foreground;
     }
   }
   ```

2. **Vanilla Extract** (Zero-runtime CSS-in-TS):
   ```typescript
   import { style, createTheme } from '@vanilla-extract/css'
   
   export const [themeClass, vars] = createTheme({
     color: {
       primary: 'oklch(0.7 0.25 250)',
       secondary: 'oklch(0.6 0.20 200)'
     }
   })
   
   export const button = style({
     padding: vars.space[4],
     backgroundColor: vars.color.primary,
     ':hover': {
       transform: 'translateY(-2px)'
     }
   })
   ```

3. **Panda CSS** (Build-time atomic CSS):
   ```jsx
   import { css } from '../styled-system/css'
   
   <button className={css({
     bg: 'primary',
     color: 'white',
     p: { base: 4, md: 6 },
     rounded: 'lg',
     _hover: { bg: 'primary.dark' }
   })}>
   ```

### Container Queries & Modern Layout
```css
/* Container query support in Tailwind v4 */
.card-container {
  container-type: inline-size;
}

.card {
  @container (min-width: 400px) {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

/* Native CSS approach */
@container sidebar (max-width: 300px) {
  .nav-item {
    padding: 0.5rem;
    font-size: 0.875rem;
  }
}
```

### CSS Performance Patterns
```css
/* Content-visibility for long pages */
.section {
  content-visibility: auto;
  contain-intrinsic-size: auto 500px;
}

/* CSS containment for component isolation */
.widget {
  contain: layout style paint;
  /* Isolates rendering, improves performance */
}

/* Layer management for cascade control */
@layer base, components, utilities;

@layer components {
  .btn {
    /* Component styles */
  }
}
```

## Testing & Quality Assurance

### Modern Testing Stack (2025)

#### Unit Testing
```javascript
// Vitest configuration (faster than Jest)
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    environment: 'happy-dom', // Lighter than jsdom
    globals: true,
    setupFiles: './test/setup.ts',
    coverage: {
      reporter: ['text', 'html'],
      threshold: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80
      }
    }
  }
})
```

#### Component Testing
```jsx
// Testing Library + Vitest
import { render, screen, userEvent } from '@testing-library/react'
import { expect, test, vi } from 'vitest'

test('accessible form submission', async () => {
  const user = userEvent.setup()
  const onSubmit = vi.fn()
  
  render(<ContactForm onSubmit={onSubmit} />)
  
  await user.type(screen.getByLabelText(/email/i), 'test@example.com')
  await user.click(screen.getByRole('button', { name: /submit/i }))
  
  expect(onSubmit).toHaveBeenCalledWith({
    email: 'test@example.com'
  })
})
```

#### E2E Testing with Playwright
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 13'] }
    }
  ]
})
```

#### Visual Regression Testing
```javascript
// Using Chromatic with Storybook
// .storybook/main.js
module.exports = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx|mdx)'],
  addons: [
    '@storybook/addon-essentials',
    '@chromatic-com/storybook'
  ]
}

// Component story with visual test
export const Default = {
  args: {
    variant: 'primary',
    children: 'Click me'
  },
  parameters: {
    chromatic: { 
      viewports: [320, 768, 1200],
      delay: 300 // Wait for animations
    }
  }
}
```

## Monitoring & Observability

### Real User Monitoring (RUM)
```javascript
// Web Vitals monitoring
import { onCLS, onINP, onLCP } from 'web-vitals'

function sendToAnalytics(metric) {
  // Send to your analytics endpoint
  fetch('/analytics', {
    method: 'POST',
    body: JSON.stringify({
      name: metric.name,
      value: metric.value,
      rating: metric.rating,
      delta: metric.delta,
      navigationType: metric.navigationType
    })
  })
}

onCLS(sendToAnalytics)
onINP(sendToAnalytics)
onLCP(sendToAnalytics)
```

### Error Tracking Integration
```javascript
// Sentry configuration
import * as Sentry from '@sentry/nextjs'

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  integrations: [
    Sentry.replayIntegration({
      maskAllText: false,
      blockAllMedia: false,
    }),
    Sentry.browserTracingIntegration(),
  ],
  tracesSampleRate: 1.0,
  replaysSessionSampleRate: 0.1,
  replaysOnErrorSampleRate: 1.0,
})
```

### Custom Performance Monitoring
```javascript
// Performance observer for custom metrics
const observer = new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    if (entry.entryType === 'measure') {
      analytics.track('Custom Timing', {
        measureName: entry.name,
        duration: entry.duration,
        startTime: entry.startTime
      })
    }
  }
})

observer.observe({ entryTypes: ['measure'] })

// Usage
performance.mark('myFeature-start')
// ... feature code ...
performance.mark('myFeature-end')
performance.measure('myFeature', 'myFeature-start', 'myFeature-end')
```

## AI-Enhanced Development

### AI-Powered Code Optimization
```javascript
// GitHub Copilot configuration
// .github/copilot-config.yml
suggestions:
  - match: "*.tsx"
    language: "typescript-react"
    max_suggestions: 3
  - match: "*.css"
    language: "css"
    include_tailwind: true

// VS Code settings for AI assistance
{
  "github.copilot.enable": {
    "*": true,
    "markdown": true,
    "yaml": true
  },
  "tabnine.experimentalAutoImports": true
}
```

### Predictive Prefetching
```javascript
// AI-driven resource prefetching
class PredictivePrefetch {
  constructor() {
    this.userPattern = []
    this.predictions = new Map()
  }
  
  trackNavigation(from, to) {
    this.userPattern.push({ from, to, timestamp: Date.now() })
    this.updatePredictions()
  }
  
  updatePredictions() {
    // Simple Markov chain for next page prediction
    const current = window.location.pathname
    const transitions = this.userPattern.filter(p => p.from === current)
    
    const counts = transitions.reduce((acc, t) => {
      acc[t.to] = (acc[t.to] || 0) + 1
      return acc
    }, {})
    
    const total = Object.values(counts).reduce((a, b) => a + b, 0)
    const probabilities = Object.entries(counts).map(([page, count]) => ({
      page,
      probability: count / total
    }))
    
    // Prefetch top predictions
    probabilities
      .filter(p => p.probability > 0.3)
      .forEach(({ page }) => {
        const link = document.createElement('link')
        link.rel = 'prefetch'
        link.href = page
        document.head.appendChild(link)
      })
  }
}
```

## Security Best Practices

### Content Security Policy (CSP)
```javascript
// Next.js security headers
const securityHeaders = [
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net;
      style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
      font-src 'self' https://fonts.gstatic.com;
      img-src 'self' data: https:;
      connect-src 'self' https://api.example.com;
    `.replace(/\n/g, '')
  },
  {
    key: 'X-Frame-Options',
    value: 'DENY'
  },
  {
    key: 'X-Content-Type-Options',
    value: 'nosniff'
  },
  {
    key: 'Referrer-Policy',
    value: 'strict-origin-when-cross-origin'
  }
]
```

### Secure Authentication Flow
```jsx
// OAuth implementation with PKCE
import { generateCodeVerifier, generateCodeChallenge } from 'oauth-pkce'

async function initiateLogin() {
  const verifier = generateCodeVerifier()
  const challenge = await generateCodeChallenge(verifier)
  
  // Store verifier securely
  sessionStorage.setItem('oauth_verifier', verifier)
  
  const params = new URLSearchParams({
    client_id: process.env.NEXT_PUBLIC_CLIENT_ID,
    redirect_uri: window.location.origin + '/callback',
    response_type: 'code',
    scope: 'openid profile email',
    code_challenge: challenge,
    code_challenge_method: 'S256'
  })
  
  window.location.href = `${AUTH_ENDPOINT}?${params}`
}
```

## Performance Budgets & Metrics

### Budget Configuration
```javascript
// performance-budget.json
{
  "timings": {
    "firstContentfulPaint": 1800,
    "largestContentfulPaint": 2500,
    "firstInputDelay": 100,
    "totalBlockingTime": 300
  },
  "resourceSizes": {
    "script": 150000,
    "style": 50000,
    "image": 500000,
    "font": 100000,
    "total": 800000
  },
  "resourceCounts": {
    "script": 10,
    "style": 5,
    "image": 30,
    "font": 5,
    "total": 50
  }
}

// Webpack bundle analyzer integration
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: process.env.ANALYZE ? 'server' : 'disabled'
    })
  ]
}
```

### Automated Performance Testing
```javascript
// Lighthouse CI configuration
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/about'],
      numberOfRuns: 3
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 1 }],
        'first-contentful-paint': ['error', { maxNumericValue: 1800 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }]
      }
    },
    upload: {
      target: 'temporary-public-storage'
    }
  }
}
```

## Code Review Checklist

### Core Design Principles
- [ ] Typography: Uses only 4 font sizes and 2 font weights (Semibold, Regular)
- [ ] Spacing: All spacing values are divisible by 8 or 4
- [ ] Colors: Follows 60/30/10 color distribution (60% neutral, 30% complementary, 10% accent)
- [ ] Structure: Elements are logically grouped with consistent spacing

### Performance Standards
- [ ] LCP < 2.5s with Early Hints implemented
- [ ] INP < 200ms with optimized event handlers
- [ ] CLS < 0.1 with reserved space for dynamic content
- [ ] Bundle size < 200KB for initial load
- [ ] Code splitting implemented for routes and heavy components
- [ ] Images optimized with modern formats (AVIF/WebP)

### Modern Stack Implementation
- [ ] Uses shadcn/ui with copy-paste approach
- [ ] Implements Radix UI for accessibility
- [ ] Tailwind CSS v4 with @theme directive
- [ ] Variable fonts (Inter or Geist) with font-display: swap
- [ ] Animation library chosen based on needs (Framer/Spring/Auto-Animate)
- [ ] Icon library consistent with design system (Lucide/Radix)

### Accessibility Compliance
- [ ] WCAG 2.2 Level AA compliant
- [ ] Keyboard navigation fully functional
- [ ] Screen reader tested with NVDA/JAWS
- [ ] Focus management implemented for modals/drawers
- [ ] Live regions for dynamic content updates
- [ ] Color contrast ratios meet standards (4.5:1 for normal text)

### State Management
- [ ] Appropriate state solution for each use case
- [ ] Server state cached with TanStack Query/SWR
- [ ] Optimistic updates implemented where applicable
- [ ] State persistence strategy defined
- [ ] No unnecessary global state

### Architecture Quality
- [ ] Components follow composition patterns
- [ ] Error boundaries implemented at appropriate levels
- [ ] Loading states with Suspense boundaries
- [ ] Micro-frontends communicate via event bus/shared state
- [ ] Performance monitoring integrated
- [ ] Bundle size budgets enforced

### Technical Implementation
- [ ] Uses proper OKLCH color variables
- [ ] Leverages @theme directive for variables
- [ ] Components implement data-slot attribute properly
- [ ] Visual hierarchy is clear and consistent
- [ ] Components use Class Variance Authority for variants
- [ ] Dark mode implementation is consistent

### Common Issues to Flag
- [ ] Too many font sizes (more than 4)
- [ ] Inconsistent spacing values (not divisible by 8 or 4)
- [ ] Overuse of accent colors (exceeding 10%)
- [ ] Random or inconsistent margins/padding
- [ ] Insufficient contrast between text and background
- [ ] Unnecessary custom CSS when Tailwind utilities would suffice
- [ ] Missing error boundaries
- [ ] No loading states for async operations
- [ ] Unoptimized images or fonts
- [ ] Direct DOM manipulation instead of React patterns