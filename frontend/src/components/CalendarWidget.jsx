import React from "react";
import { Card, CardContent } from "./ui/Card";
import { Calendar as CalIcon } from "lucide-react";
import { useAllIntegrations } from "../hooks/useIntegrations";

export default function CalendarWidget() {
  const { data: integrations, isLoading, isError } = useAllIntegrations();
  const events = integrations?.events || [];

  if (isLoading)
    return <div className="animate-pulse bg-white border rounded p-4 h-32" />;
  if (isError)
    return (
      <div className="bg-white border rounded p-4">Unable to load events</div>
    );

  const next = events.slice(0, 3);

  return (
    <Card>
      <CardContent>
        <div className="flex items-center justify-between">
          <h3 className="font-semibold flex items-center gap-2">
            <CalIcon className="w-4 h-4 text-yellow-500" />
            Upcoming
          </h3>
          <a className="text-xs text-gray-500" href="/calendar">
            View calendar
          </a>
        </div>
        <ul className="mt-2 space-y-2">
          {next.length === 0 ? (
            <li className="text-sm text-gray-500">No upcoming events</li>
          ) : (
            next.map((e) => (
              <li key={e.id} className="text-sm">
                <div className="font-medium">{e.title}</div>
                <div className="text-xs text-gray-500">
                  {e.start ? new Date(e.start).toLocaleString() : ""}
                </div>
              </li>
            ))
          )}
        </ul>
      </CardContent>
    </Card>
  );
}
