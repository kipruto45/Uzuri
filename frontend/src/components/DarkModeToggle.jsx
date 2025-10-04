import React, { useContext } from "react";
import { ThemeContext } from "../contexts/ThemeContext";
import { Sun, Moon } from "lucide-react";

export default function DarkModeToggle() {
  const { dark, toggle } = useContext(ThemeContext);
  return (
    <button
      onClick={toggle}
      aria-pressed={dark}
      title={dark ? "Switch to light mode" : "Switch to dark mode"}
      className="px-2 py-1 rounded-md flex items-center space-x-2"
    >
      {dark ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
      <span className="text-xs">{dark ? "Light" : "Dark"}</span>
    </button>
  );
}
