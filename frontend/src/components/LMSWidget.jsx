import React from "react";
import { Card, CardContent } from "../components/ui/Card";
import { useLMSCourses } from "../hooks/useLMS";

export default function LMSWidget() {
  const { data: courses = [], isLoading } = useLMSCourses();
  if (isLoading) return <div className="p-4">Loading courses…</div>;
  return (
    <Card>
      <CardContent>
        <h3 className="font-semibold">LMS</h3>
        <ul className="mt-2 text-sm">
          {courses.slice(0, 5).map((c) => (
            <li key={c.id}>{c.title}</li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
