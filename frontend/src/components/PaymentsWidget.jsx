import React from "react";
import { Card, CardContent } from "../components/ui/Card";
import { usePaymentsSummary, useCreatePayment } from "../hooks/usePayments";
import toast from "react-hot-toast";

export default function PaymentsWidget() {
  const { data: summary, isLoading, isError, refetch } = usePaymentsSummary();
  const createMut = useCreatePayment();

  if (isLoading) return <div className="p-4">Loading payments…</div>;

  if (isError)
    return (
      <div className="bg-white border rounded p-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold">Payments</h3>
        </div>
        <div className="text-sm text-red-600 mt-2">
          Unable to load payments{" "}
          <button onClick={() => refetch()} className="ml-2 text-blue-600">
            Retry
          </button>
        </div>
      </div>
    );

  const recent = summary?.payment_history || [];

  const handleQuickPay = async () => {
    if (createMut.isLoading) return;
    const amount = summary?.next_due?.amount || 0;
    try {
      const res = await createMut.mutateAsync({ amount });
      // If backend returns a gateway URL, open a new window
      if (res && res.gateway_url) {
        window.open(res.gateway_url, "_blank");
        toast.success("Payment initiated. Gateway opened in new tab");
      } else {
        toast("Payment initiated", { icon: "⏳" });
      }
    } catch (err) {
      toast.error("Failed to initiate payment");
    }
  };

  return (
    <Card>
      <CardContent>
        <h3 className="font-semibold">Payments</h3>
        <div className="mt-2 text-sm">
          <div>Next due: {summary?.next_due?.due_date || "—"}</div>
          <div className="mt-2">Recent payments:</div>
          <ul className="mt-1 list-disc pl-5 text-sm">
            {recent.map((p) => (
              <li key={p.id}>
                {p.description || p.reference} — {p.amount}
              </li>
            ))}
          </ul>
          <div className="mt-3">
            <button
              onClick={handleQuickPay}
              disabled={createMut.isLoading}
              className="px-3 py-1 rounded bg-green-600 text-white disabled:opacity-50"
            >
              {createMut.isLoading ? "Initiating…" : "Quick pay"}
            </button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
