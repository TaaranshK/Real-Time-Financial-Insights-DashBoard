import React, { Component, ReactNode, ErrorInfo } from 'react';
import { AlertCircle } from 'lucide-react';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex h-screen items-center justify-center bg-background p-4">
          <div className="glass-card p-8 max-w-md text-center">
            <div className="flex justify-center mb-4">
              <AlertCircle size={48} className="text-destructive" />
            </div>
            <h1 className="text-2xl font-bold text-foreground mb-2">Oops! Something went wrong</h1>
            <p className="text-muted-foreground mb-4">
              {this.state.error?.message || 'An unexpected error occurred'}
            </p>
            <div className="bg-muted/20 rounded-lg p-3 mb-4 text-left text-xs text-muted-foreground overflow-auto max-h-32">
              <code>{this.state.error?.stack}</code>
            </div>
            <button
              onClick={() => window.location.href = '/'}
              className="btn-gradient w-full"
            >
              Go to Home
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
