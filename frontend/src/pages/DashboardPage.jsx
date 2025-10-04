import React from "react";
import { Card, CardContent } from "../components/ui/Card";
import PageShell from "../components/ui/PageShell";
import { motion } from "framer-motion";
import {
  User,
  Wallet,
  Home,
  Book,
  CreditCard,
  FileText,
  Calendar,
  RefreshCw,
  Bell,
  Clock,
  CheckCircle,
  XCircle,
} from "lucide-react";
import { Link } from "react-router-dom";
import {
  useStudentDashboard,
  useDashboardSummary,
} from "../hooks/useDashboard";
import { useQuery } from "@tanstack/react-query";
import { useAllIntegrations } from "../hooks/useIntegrations";
import NotificationsWidget from "../components/NotificationsWidget";
import PaymentsWidget from "../components/PaymentsWidget";
import LMSWidget from "../components/LMSWidget";
import LearningPathwaysWidget from "../components/LearningPathwaysWidget";
import ProfileCard from "../components/ProfileCard";
import CalendarWidget from "../components/CalendarWidget";
import AttachmentsUploader from "../components/AttachmentsUploader";
import { useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import ErrorBoundary from "../components/ErrorBoundary";

export default function DashboardPage() {
  const {
    data: student,
    isLoading: loadingStudent,
    isError: studentError,
  } = useStudentDashboard();
  const { data: summary, isLoading: loadingSummary } = useDashboardSummary();
  const queryClient = useQueryClient();
  const {
    data: integrations,
    isLoading: loadingIntegrations,
    isError: integrationsError,
    refetch: refetchIntegrations,
  } = useAllIntegrations();
  const [lastRefresh, setLastRefresh] = useState(null);

  const cards = (summary && Array.isArray(summary.cards) && summary.cards.length
    ? summary.cards
    : null) || [
    {
      title: "My Profile",
      desc: "View & update details",
      icon: <User className="w-8 h-8 text-blue-500" />,
      link: "/profile",
    },
    {
      title: "Academic Leave",
      desc: "Apply for academic leave",
      icon: <Book className="w-8 h-8 text-indigo-500" />,
      link: "/academic-leave",
    },
    {
      title: "Calendar",
      desc: "Academic calendar & events",
      icon: <Calendar className="w-8 h-8 text-yellow-500" />,
      link: "/calendar",
    },
    {
      title: "Clearance",
      desc: "Clearance status & actions",
      icon: <FileText className="w-8 h-8 text-gray-600" />,
      link: "/clearance",
    },
    {
      title: "Disciplinary",
      desc: "Disciplinary records",
      icon: <FileText className="w-8 h-8 text-red-500" />,
      link: "/disciplinary",
    },
    {
      title: "Emasomo",
      desc: "Course materials (Emasomo)",
      icon: <Book className="w-8 h-8 text-purple-500" />,
      link: "/emasomo",
    },
    {
      title: "Exam Card",
      desc: "Download exam card",
      icon: <FileText className="w-8 h-8 text-teal-500" />,
      link: "/exam-card",
    },
    {
      title: "Fee Management",
      desc: "Manage fee payments",
      icon: <CreditCard className="w-8 h-8 text-green-600" />,
      link: "/fee_management",
    },
    {
      title: "Feedback",
      desc: "Provide feedback",
      icon: <FileText className="w-8 h-8 text-indigo-400" />,
      link: "/feedback",
    },
    {
      title: "Fees",
      desc: "View outstanding fees",
      icon: <CreditCard className="w-8 h-8 text-green-400" />,
      link: "/fees",
    },
    {
      title: "Final Results",
      desc: "View final results",
      icon: <FileText className="w-8 h-8 text-blue-600" />,
      link: "/final_results",
    },
    {
      title: "Finance Registration",
      desc: "Finance registration",
      icon: <CreditCard className="w-8 h-8 text-yellow-600" />,
      link: "/finance_registration",
    },
    {
      title: "Graduation",
      desc: "Graduation status & applications",
      icon: <Book className="w-8 h-8 text-pink-500" />,
      link: "/graduation",
    },
    {
      title: "Hostels",
      desc: "Hostel booking & status",
      icon: <Home className="w-8 h-8 text-yellow-500" />,
      link: "/hostel",
    },
    {
      title: "Lecturer Evaluation",
      desc: "Evaluate your lecturers",
      icon: <FileText className="w-8 h-8 text-gray-700" />,
      link: "/lecturer_evaluation",
    },
    {
      title: "Provisional Results",
      desc: "View provisional results",
      icon: <FileText className="w-8 h-8 text-orange-500" />,
      link: "/provisional_results",
    },
    {
      title: "Unit Registration",
      desc: "Register for units",
      icon: <FileText className="w-8 h-8 text-blue-400" />,
      link: "/unit_registration",
    },
    {
      title: "Timetable",
      desc: "View class timetable",
      icon: <Calendar className="w-8 h-8 text-cyan-500" />,
      link: "/timetable",
    },
    {
      title: "Attachments",
      desc: "Upload & manage files",
      icon: <FileText className="w-8 h-8 text-purple-500" />,
      link: "/attachments",
    },
    {
      title: "Accessibility",
      desc: "Accessibility tools & features",
      icon: <User className="w-8 h-8 text-indigo-500" />,
      link: "/accessibility",
    },
    {
      title: "Support",
      desc: "Get help & support",
      icon: <HelpCircle className="w-8 h-8 text-green-500" />,
      link: "/support",
    },
  ];

  const notifications = integrations?.notifications || [];
  const events = integrations?.events || [];

  // integrations health summary
  const integrationsHealth = (integrations && integrations._health) || null;

  const handleRefresh = async () => {
    try {
      await Promise.all([
        queryClient.invalidateQueries(["dashboard", "student"]),
        queryClient.invalidateQueries(["dashboard", "summary"]),
        queryClient.invalidateQueries(["integrations", "all"]),
      ]);
      setLastRefresh(new Date());
    } catch (e) {
      // ignore
    }
  };

  return (
    <PageShell
      title="Dashboard"
      subtitle={`Welcome back${student?.user?.first_name ? `, ${student.user.first_name}` : ""}`}
      actions={
        <button
          onClick={handleRefresh}
          aria-label="Refresh dashboard"
          title="Refresh dashboard"
          className="inline-flex items-center gap-2 px-3 py-1.5 bg-white border rounded shadow-sm hover:bg-gray-50"
        >
          <RefreshCw className="w-4 h-4" aria-hidden /> Refresh
        </button>
      }
    >
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {loadingStudent || loadingSummary || loadingIntegrations ? (
          // Skeleton grid when loading
          <>
            <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-6">
              {Array.from({ length: 6 }).map((_, i) => (
                <div
                  key={i}
                  className="animate-pulse bg-white border rounded p-6 h-28"
                />
              ))}
            </div>
            <aside className="space-y-4">
              <div className="animate-pulse bg-white border rounded p-4 h-40" />
              <div className="animate-pulse bg-white border rounded p-4 h-40" />
            </aside>
          </>
        ) : studentError ? (
          <div className="text-red-600">Failed to load dashboard</div>
        ) : (
          <>
            <div className="lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-6">
              <ProfileCard />
              {cards.map((c, i) => (
                <motion.div whileHover={{ scale: 1.03 }} key={i}>
                  <Link
                    to={c.link}
                    className="block focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-400"
                    aria-label={`${c.title} - ${c.desc}`}
                  >
                    <Card>
                      <CardContent className="flex items-center gap-4 p-6">
                        {React.cloneElement(c.icon, { "aria-hidden": true })}
                        <div>
                          <h2 className="text-xl font-bold">{c.title}</h2>
                          <p className="text-sm text-gray-500">{c.desc}</p>
                        </div>
                        <div className="ml-auto">
                          <span className="text-sm text-blue-600">Open</span>
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                </motion.div>
              ))}
              <AttachmentsUploader />
            </div>
            <aside className="space-y-4">
              <div aria-live="polite">
                <NotificationsWidget />
              </div>
              <CalendarWidget />

              <PaymentsWidget />

              <Card>
                <CardContent>
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold flex items-center gap-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      Integrations
                    </h3>
                    <span className="text-xs text-gray-500">
                      {integrations ? "Status" : "Unknown"}
                    </span>
                  </div>
                  <div className="mt-3 space-y-2">
                    {integrationsHealth ? (
                      Object.keys(integrationsHealth).map((k) => (
                        <div
                          key={k}
                          className="flex items-center justify-between text-sm"
                        >
                          <div>{k}</div>
                          <div className="flex items-center gap-2">
                            {integrationsHealth[k] ? (
                              <span className="text-green-600">Healthy</span>
                            ) : (
                              <span className="text-red-600">Down</span>
                            )}
                          </div>
                        </div>
                      ))
                    ) : (
                      <div className="text-sm text-gray-500">
                        No integration health data
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>

              <LMSWidget />

              <LearningPathwaysWidget />
            </aside>
          </>
        )}
      </div>
    </PageShell>
  );
}
