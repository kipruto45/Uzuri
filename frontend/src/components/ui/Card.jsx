import React from "react";

export function Card({ title, children, footer, className = "" }) {
  return (
    <div className={`bg-white rounded shadow p-4 ${className}`}>
      {title && <div className="font-medium mb-2">{title}</div>}
      <div>{children}</div>
      {footer && <div className="mt-3 text-sm text-gray-500">{footer}</div>}
    </div>
  );
}

export function CardContent({ children, className = "" }) {
  return <div className={`p-4 ${className}`}>{children}</div>;
}

export default Card;
