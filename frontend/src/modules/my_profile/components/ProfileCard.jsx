import React from "react";

export default function ProfileCard({ profile }) {
  if (!profile) return <div>Loading...</div>;
  return (
    <div className="border p-3">
      <div className="font-bold">{profile.full_name}</div>
      <div>{profile.email}</div>
      <div>Student ID: {profile.student_id}</div>
    </div>
  );
}
