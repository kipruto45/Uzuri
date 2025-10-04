import React from "react";
// Replace useQuery during this test to avoid exercising react-query internals
jest.mock("@tanstack/react-query", () => {
  const actual = jest.requireActual("@tanstack/react-query");
  return {
    ...actual,
    useQuery: (key, fn, opts) => {
      if (Array.isArray(key) && key[0] === "payments") {
        try {
          const axios = require("../../api/axiosClient");
          if (axios.get && axios.get.mock && axios.get.mock.results[0]) {
            const res = axios.get.mock.results[0].value;
            if (res && res.data)
              return { data: res.data, isSuccess: true, isLoading: false };
          }
        } catch (e) {}
        return {
          data: { next_due: null, payment_history: [] },
          isSuccess: true,
          isLoading: false,
        };
      }
      return actual.useQuery(key, fn, opts);
    },
    useQueryClient: () => ({ invalidateQueries: jest.fn() }),
  };
});

import { renderWithClient, screen } from "../../test-utils";
import axios from "../../api/axiosClient";
import PaymentsWidget from "../PaymentsWidget";

jest.mock("../../api/axiosClient");
// Provide a mocked hook implementation so the component renders deterministic UI
jest.mock("../../hooks/usePayments", () => ({
  usePaymentsSummary: () => ({
    data: {
      next_due: { due_date: "2025-10-03", amount: 100 },
      payment_history: [{ id: 1, amount: 100, reference: "abc" }],
    },
    isLoading: false,
    isError: false,
  }),
  useCreatePayment: () => ({
    isLoading: false,
    mutateAsync: jest.fn().mockResolvedValue({}),
  }),
}));

// use shared renderWithClient from test-utils which provides a pre-patched
// QueryClient instance for stability in test environments.

test("PaymentsWidget shows recent payments", async () => {
  axios.get.mockResolvedValue({
    data: {
      next_due: { due_date: "2025-10-03", amount: 100 },
      payment_history: [{ id: 1, amount: 100, reference: "abc" }],
    },
  });
  renderWithClient(<PaymentsWidget />);
  expect(await screen.findByText(/Next due/)).toBeInTheDocument();
  expect(await screen.findByText(/abc/)).toBeInTheDocument();
});
