import React from "react";
import toast from "react-hot-toast";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error("ErrorBoundary caught", error, info);
    toast.error("An unexpected error occurred");
  }

  render() {
    if (this.state.hasError) {
      return <div className="p-6">Something went wrong.</div>;
    }
    return this.props.children;
  }
}
