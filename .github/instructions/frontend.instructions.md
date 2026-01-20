---
applyTo: '**/*.{tsx,jsx,vue,svelte}'
description: Frontend development global standards
name: Frontend Standards
---

# Global Frontend Development Standards

## Technology Stack

- React 18+ or Vue 3+ or Svelte or Angular
- TypeScript mandatory
- Tailwind CSS or CSS Modules
- Vite or Next.js for bundling

## Component Design

```typescript
// Functional components with TypeScript
interface Props {
  title: string;
  onAction: () => void;
  isLoading?: boolean;
}

export const Component: React.FC<Props> = ({
  title,
  onAction,
  isLoading = false
}) => {
  return (
    <div className="component">
      {/* Implementation */}
    </div>
  );
};
```

## State Management

- React: useState/useReducer for local, Zustand/Context for global
- Vue: Composition API with Pinia
- Svelte: Stores for shared state
- Angular: Services with RxJS
- Keep state minimal and close to where it's used

## Performance

- Lazy loading for routes and heavy components
- Memoization: `useMemo`, `useCallback`, `React.memo`
- Code splitting
- Image optimization (WebP, lazy loading)
- Virtualization for long lists

## Accessibility

- Semantic HTML
- ARIA labels when needed
- Keyboard navigation
- Color contrast WCAG AA minimum
- Alt text for images
