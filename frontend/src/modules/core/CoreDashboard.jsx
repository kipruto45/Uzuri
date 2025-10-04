import React, { useEffect, useState } from "react";
import { fetchCoreOverview } from "./api";
import SummaryCard from "./components/SummaryCard";
import ActivityFeed from "./components/ActivityFeed";
import Sparkline from "./components/Sparkline";
import MiniBarChart from "./components/MiniBarChart";

function IconUsers() {
  return (
    <svg
      className="w-6 h-6"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10z"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
      <path
        d="M21 21v-2a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v2"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
      />
    </svg>
  );
}
function IconDocs() {
  return (
    <svg
      className="w-6 h-6"
      viewBox="0 0 24 24"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export default function CoreDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeframe, setTimeframe] = useState("7d");

  // sample small metric series (would come from metrics endpoint)
  const sampleSeries = [5, 8, 6, 10, 12, 9, 14];

  useEffect(() => {
    let mounted = true;
    async function load() {
      setLoading(true);
      const res = await fetchCoreOverview();
      if (mounted) setData(res);
      setLoading(false);
    }
    load();
    return () => (mounted = false);
  }, []);

  const usersCount = data?.users?.count;
  const profilesCount = data?.profiles?.count;
  const rolesCount = data?.roles?.count;
  const logs = data?.logs?.results || [];

  return (
    <div className="p-6">
      <header className="mb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">Core Dashboard</h1>
          <p className="text-sm text-gray-600">
            Overview of system health and recent activity
          </p>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="border rounded px-2 py-1"
          >
            <option value="24h">24h</option>
            <option value="7d">7d</option>
            <option value="30d">30d</option>
          </select>
          <button className="px-3 py-2 bg-indigo-600 text-white rounded">
            Create Report
          </button>
        </div>
      </header>

      {loading ? (
        <div>Loading…</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
          <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded shadow flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm text-gray-500">Active Users</div>
                  <div className="text-2xl font-semibold">
                    {usersCount ?? "—"}
                  </div>
                </div>
                <Sparkline data={sampleSeries} />
              </div>
              <div className="mt-3 text-xs text-gray-500">
                Users active in the selected timeframe
              </div>
            </div>
            <div className="bg-white p-4 rounded shadow flex flex-col justify-between">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-sm text-gray-500">Profiles</div>
                  <div className="text-2xl font-semibold">
                    {profilesCount ?? "—"}
                  </div>
                </div>
                <MiniBarChart data={[2, 3, 4, 5, 3, 6, 4]} />
              </div>
              <div className="mt-3 text-xs text-gray-500">
                New profiles created
              </div>
            </div>
          </div>
          <div className="lg:col-span-2">
            <div className="bg-white p-4 rounded shadow">
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-medium">System Metrics</h3>
                <div className="text-xs text-gray-500">Updated: just now</div>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                <SummaryCard
                  title="Users"
                  value={usersCount}
                  icon={<IconUsers />}
                />
                <SummaryCard
                  title="Profiles"
                  value={profilesCount}
                  icon={<IconDocs />}
                />
                <SummaryCard
                  title="Roles"
                  value={rolesCount}
                  icon={<IconDocs />}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      <section className="mt-6">
        <h2 className="text-lg font-medium mb-2">Recent Activity</h2>
        <ActivityFeed logs={logs} />
      </section>
    </div>
  );
}
