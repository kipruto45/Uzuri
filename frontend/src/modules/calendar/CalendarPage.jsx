import React, { useEffect, useState } from "react";
import PageShell from "../../components/ui/PageShell";
import { Card, CardContent } from "../../components/ui/Card";
import {
  myEvents,
  listEvents,
  createEvent,
  deleteEvent,
  exportIcal,
  googleAuthUrl,
  pushGoogle,
  pullGoogle,
} from "./api";
import EventForm from "./components/EventForm";

function EventRow({ e, onEdit, onDelete }) {
  return (
    <tr>
      <td className="p-2">{e.title}</td>
      <td className="p-2">{new Date(e.start_time).toLocaleString()}</td>
      <td className="p-2">{new Date(e.end_time).toLocaleString()}</td>
      <td className="p-2">{e.location}</td>
      <td className="p-2">
        <button
          onClick={() => onEdit(e)}
          className="mr-2 px-2 py-1 border rounded"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(e.id)}
          className="px-2 py-1 border rounded text-red-600"
        >
          Delete
        </button>
      </td>
    </tr>
  );
}

export default function CalendarPage() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);

  useEffect(() => {
    let mounted = true;
    async function load() {
      setLoading(true);
      try {
        const data = await myEvents();
        if (mounted) setEvents(data);
      } catch (e) {
        console.error("failed to load events", e);
      } finally {
        if (mounted) setLoading(false);
      }
    }
    load();
    return () => (mounted = false);
  }, []);

  async function onCreate(payload) {
    const created = await createEvent(payload);
    setEvents((p) => [created, ...p]);
    setShowForm(false);
  }

  async function onDelete(id) {
    await deleteEvent(id);
    setEvents((p) => p.filter((ev) => ev.id !== id));
  }

  return (
    <PageShell title="Calendar" subtitle="Events & scheduling">
      <div className="flex items-center justify-between mb-4">
        <div />
        <div className="flex gap-2">
          <button
            onClick={() => setShowForm(true)}
            className="px-3 py-2 bg-blue-600 text-white rounded"
          >
            New Event
          </button>
          <button
            onClick={() =>
              exportIcal().then((b) => {
                const blob = new Blob([b], { type: "text/calendar" });
                const url = URL.createObjectURL(blob);
                window.open(url);
              })
            }
            className="px-3 py-2 border rounded"
          >
            Export iCal
          </button>
        </div>
      </div>

      <Card>
        <CardContent>
          {loading ? (
            <div>Loading events…</div>
          ) : events.length === 0 ? (
            <div>No upcoming events. Create one to get started.</div>
          ) : (
            <div className="overflow-x-auto bg-white rounded shadow-sm">
              <table className="min-w-full">
                <thead>
                  <tr>
                    <th className="p-2 text-left">Title</th>
                    <th className="p-2 text-left">Start</th>
                    <th className="p-2 text-left">End</th>
                    <th className="p-2 text-left">Location</th>
                    <th className="p-2">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {events.map((e) => (
                    <EventRow
                      key={e.id}
                      e={e}
                      onEdit={(ev) => {
                        setEditing(ev);
                        setShowForm(true);
                      }}
                      onDelete={onDelete}
                    />
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {showForm && (
        <EventForm
          initial={editing}
          onCancel={() => {
            setShowForm(false);
            setEditing(null);
          }}
          onSave={onCreate}
        />
      )}
    </PageShell>
  );
}
