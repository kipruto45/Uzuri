import React, { useEffect, useState } from "react";
import { fetchStatements } from "./api";
import FeeStatement from "./components/FeeStatement";

export default function FeesPage() {
  const [statements, setStatements] = useState([]);

  useEffect(() => {
    (async () => {
      try {
        const data = await fetchStatements("me");
        setStatements(data || []);
      } catch (e) {
        console.error(e);
      }
    })();
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl mb-2">Fee Statements</h2>
      {statements.map((s) => (
        <FeeStatement key={s.id} statement={s} />
      ))}
    </div>
  );
}
