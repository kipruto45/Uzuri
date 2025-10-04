import React from "react";
import { motion } from "framer-motion";
import {
  FileText,
  Calendar,
  CheckCircle,
  XCircle,
  Clock,
  Paperclip,
} from "lucide-react";

const statusMap = {
  approved: {
    label: "Approved",
    bg: "bg-green-100",
    text: "text-green-800",
    icon: <CheckCircle className="w-4 h-4 inline mr-1" />,
  },
  rejected: {
    label: "Rejected",
    bg: "bg-red-100",
    text: "text-red-800",
    icon: <XCircle className="w-4 h-4 inline mr-1" />,
  },
  pending: {
    label: "Pending",
    bg: "bg-yellow-100",
    text: "text-yellow-800",
    icon: <Clock className="w-4 h-4 inline mr-1" />,
  },
  cancelled: {
    label: "Cancelled",
    bg: "bg-gray-100",
    text: "text-gray-700",
    icon: <XCircle className="w-4 h-4 inline mr-1" />,
  },
};

export default function LeaveCard({ leave, onOpen }) {
  const s = statusMap[leave.status] || statusMap.pending;

  return (
    <motion.div
      whileHover={{ y: -6, boxShadow: "0 20px 40px rgba(0,0,0,0.12)" }}
      transition={{ type: "spring", stiffness: 300 }}
      className="bg-white dark:bg-gray-800 rounded-lg p-4 border border-gray-100 dark:border-gray-700"
      onClick={() => onOpen && onOpen(leave)}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-indigo-50 dark:bg-indigo-900 rounded-md">
            <FileText className="w-5 h-5 text-indigo-600 dark:text-indigo-200" />
          </div>
          <div>
            <div className="text-sm font-semibold text-gray-900 dark:text-gray-100">
              {leave.leave_type}
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400">
              {leave.reason?.slice(0, 80) || "—"}
            </div>
          </div>
        </div>

        <div
          className="text-xs px-2 py-1 rounded-full flex items-center"
          aria-hidden
        >
          <span
            className={`${s.bg} ${s.text} px-2 py-1 rounded-full text-xs font-medium flex items-center`}
          >
            {s.icon}
            {s.label}
          </span>
        </div>
      </div>

      <div className="mt-3 flex items-center justify-between text-sm text-gray-600 dark:text-gray-300">
        <div className="flex items-center space-x-2">
          <Calendar className="w-4 h-4" />
          <div>
            {leave.start_date} → {leave.end_date}
          </div>
        </div>

        <div className="flex items-center space-x-3">
          <div className="flex items-center text-xs text-gray-500 dark:text-gray-400">
            <Paperclip className="w-4 h-4 mr-1" />
            {leave.documents?.length || 0}
          </div>
        </div>
      </div>
    </motion.div>
  );
}
