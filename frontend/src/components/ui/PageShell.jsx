import React from "react";

export default function PageShell({ title, subtitle, actions, children }) {
  return (
    <div className="p-6">
      <header className="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">{title}</h1>
          {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className="flex items-center gap-2">{actions}</div>
      </header>
      <main>{children}</main>
    </div>
  );
}
