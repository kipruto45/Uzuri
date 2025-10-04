import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { listLeaveRequests } from "./api";
import LeaveCard from "./components/LeaveCard";
import NewRequestModal from "./components/NewRequestModal";
import DocumentsList from "./components/DocumentsList";
import NotificationsPanel from "./components/NotificationsPanel";
import FAB from "./components/FAB";
import toast from "react-hot-toast";

function Breadcrumbs() {
  return (
    <div className="text-sm text-gray-500 mb-3">
      Dashboard /{" "}
      <span className="text-gray-900 dark:text-gray-100">Academic Leave</span>
    </div>
  );
}

export default function AcademicLeavePage() {
  const [selected, setSelected] = useState(null);
  const [openNew, setOpenNew] = useState(false);

  const { data, isLoading } = useQuery(["leaveRequests"], () =>
    listLeaveRequests({ page_size: 50 }),
  );

  const leaves = data?.results || [];

  return (
    <div className="p-4 max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-4">
        <div>
          <Breadcrumbs />
          <h1 className="text-2xl font-semibold">Academic Leave</h1>
        </div>
        <div className="hidden md:block">
          <button
            onClick={() => setOpenNew(true)}
            className="px-4 py-2 rounded-md bg-gradient-to-r from-indigo-600 to-indigo-400 text-white"
          >
            + New Request
          </button>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="md:col-span-2">
          <section>
            <h2 className="text-lg font-medium mb-3">Your Requests</h2>

            {isLoading ? (
              <div className="space-y-3">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className="h-24 bg-gray-100 dark:bg-gray-800 rounded animate-pulse"
                  ></div>
                ))}
              </div>
            ) : leaves.length === 0 ? (
              <div className="text-center py-16">
                <div className="text-4xl">📄</div>
                <div className="mt-4 text-lg font-medium">No requests yet</div>
                <div className="text-sm text-gray-500 mt-2">
                  Start by submitting your first leave request.
                </div>
                <div className="mt-4">
                  <button
                    onClick={() => setOpenNew(true)}
                    className="px-4 py-2 rounded-md bg-indigo-600 text-white"
                  >
                    New Request
                  </button>
                </div>
              </div>
            ) : (
              <div className="grid sm:grid-cols-2 gap-4">
                {leaves.map((l) => (
                  <LeaveCard
                    key={l.id}
                    leave={l}
                    onOpen={(lv) => setSelected(lv)}
                  />
                ))}
              </div>
            )}
          </section>

          {selected && (
            <section className="mt-6 bg-white dark:bg-gray-800 p-4 rounded">
              <h3 className="font-semibold">Request details</h3>
              <div className="mt-2 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-gray-500">Type</div>
                  <div className="font-medium">{selected.leave_type}</div>
                  <div className="text-sm text-gray-500 mt-2">Dates</div>
                  <div className="font-medium">
                    {selected.start_date} → {selected.end_date}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">Reason</div>
                  <div className="mt-1 text-sm">{selected.reason}</div>
                </div>
              </div>

              <div className="mt-4">
                <h4 className="font-medium">Documents</h4>
                <div className="mt-2">
                  <DocumentsList docs={selected.documents || []} />
                </div>
              </div>
            </section>
          )}
        </div>

        <aside>
          <div className="bg-white dark:bg-gray-800 p-4 rounded mb-4">
            <h3 className="font-medium">Notifications</h3>
            <div className="mt-3">
              <NotificationsPanel
                items={[]}
                onMarkRead={(id) => toast("Marked read")}
              />
            </div>
          </div>

          <div className="bg-white dark:bg-gray-800 p-4 rounded">
            <h3 className="font-medium">Quick actions</h3>
            <div className="mt-3 space-y-2">
              <button className="w-full text-left px-3 py-2 rounded border">
                Download all documents
              </button>
              <button className="w-full text-left px-3 py-2 rounded border">
                Contact admin
              </button>
            </div>
          </div>
        </aside>
      </div>

      <NewRequestModal isOpen={openNew} onClose={() => setOpenNew(false)} />
      <FAB onClick={() => setOpenNew(true)} />
    </div>
  );
}
