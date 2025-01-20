"use client";

import { Component, ErrorInfo, ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="p-4 text-red-500">
            <h2 className="text-lg font-bold mb-2">Something went wrong</h2>
            <details className="text-sm">
              <summary>Error details</summary>
              <pre className="mt-2 p-2 bg-gray-100 rounded">
                {this.state.error?.message}
              </pre>
            </details>
          </div>
        )
      );
    }

    return this.props.children;
  }
} 