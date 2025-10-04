import React from "react";
import { Link } from "react-router-dom";
import { Home, User, Book, CreditCard, FileText, Calendar } from "lucide-react";

const items = [
  { to: "/profile", label: "My Profile", icon: <User /> },
  { to: "/academic-leave", label: "Academic Leave", icon: <Book /> },
  { to: "/calendar", label: "Calendar", icon: <Calendar /> },
  { to: "/clearance", label: "Clearance", icon: <FileText /> },
  { to: "/disciplinary", label: "Disciplinary", icon: <FileText /> },
  { to: "/emasomo", label: "Emasomo", icon: <Book /> },
  { to: "/exam-card", label: "Exam Card", icon: <FileText /> },
  { to: "/fee_management", label: "Fee Management", icon: <CreditCard /> },
  { to: "/feedback", label: "Feedback", icon: <FileText /> },
  { to: "/fees", label: "Fees", icon: <CreditCard /> },
  { to: "/final_results", label: "Final Results", icon: <FileText /> },
  {
    to: "/finance_registration",
    label: "Finance Registration",
    icon: <CreditCard />,
  },
  { to: "/graduation", label: "Graduation", icon: <Book /> },
  { to: "/hostel", label: "Hostels", icon: <Book /> },
  {
    to: "/lecturer_evaluation",
    label: "Lecturer Evaluation",
    icon: <FileText />,
  },
  {
    to: "/provisional_results",
    label: "Provisional Results",
    icon: <FileText />,
  },
  { to: "/unit_registration", label: "Unit Registration", icon: <FileText /> },
  { to: "/timetable", label: "Timetable", icon: <Calendar /> },
];

export default function Sidebar() {
  return (
    <aside className="hidden md:block w-64 bg-gradient-to-b from-white to-gray-50 border-r">
      <div className="p-4">
        <h3 className="font-bold text-xl">Uzuri</h3>
      </div>
      <nav className="p-2 space-y-1">
        {items.map((it) => (
          <Link
            key={it.to}
            to={it.to}
            className="flex items-center gap-3 p-3 rounded hover:bg-gray-100"
          >
            <span className="w-6 h-6">{it.icon}</span>
            <span>{it.label}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
}
