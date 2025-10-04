import React, { useEffect, useState } from "react";
import { fetchProfile } from "./api";
import ProfileCard from "./components/ProfileCard";

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    (async () => {
      const p = await fetchProfile();
      setProfile(p);
    })();
  }, []);

  return (
    <div className="p-4">
      <h2>My Profile</h2>
      <ProfileCard profile={profile} />
    </div>
  );
}
