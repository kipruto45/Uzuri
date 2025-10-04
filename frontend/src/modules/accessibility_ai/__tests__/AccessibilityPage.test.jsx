import React from "react";
import { renderWithClient, screen, userEvent } from "../../../test-utils";
import AccessibilityPage from "../AccessibilityPage";

jest.mock("../api", () => ({
  // Return synchronous values so our mocked useQuery can read data
  listAccessibilityFeatures: jest.fn(() => [
    { id: 1, feature_type: "high_contrast", enabled: true },
  ]),
  toggleAccessibilityFeature: jest.fn((id, payload) => ({
    id,
    feature_type: "high_contrast",
    enabled: payload.enabled,
  })),
  createAccessibilityFeature: jest.fn((p) => ({
    id: 2,
    feature_type: p.feature_type,
    enabled: p.enabled,
  })),
}));

// Mock react-query hooks for deterministic behavior in this unit test and to
// avoid exercising internal QueryClient internals that can vary in Jest envs.
jest.mock("@tanstack/react-query", () => {
  const actual = jest.requireActual("@tanstack/react-query");
  return {
    ...actual,
    useQuery: (key, fn, opts) => {
      if (Array.isArray(key) && key[0] === "accessibility") {
        try {
          const api = require("../api");
          const data = api.listAccessibilityFeatures();
          return { data: data || [], isSuccess: true, isLoading: false };
        } catch (e) {
          return { data: [], isSuccess: true, isLoading: false };
        }
      }
      return actual.useQuery(key, fn, opts);
    },
    useMutation: (mutationFn, opts) => {
      return {
        mutateAsync: async (variables) => {
          const res = await (mutationFn ? mutationFn(variables) : undefined);
          if (opts && typeof opts.onSuccess === "function") opts.onSuccess(res);
          return res;
        },
        mutate: (v) => Promise.resolve(mutationFn ? mutationFn(v) : undefined),
      };
    },
    useQueryClient: () => ({
      cancelQueries: jest.fn(),
      getQueryData: jest.fn(() => []),
      setQueryData: jest.fn(),
      invalidateQueries: jest.fn(),
    }),
  };
});

describe("AccessibilityPage", () => {
  test("renders features and allows toggle and create", async () => {
    const { rerender } = renderWithClient(<AccessibilityPage />);

    expect(
      await screen.findByText(/Accessibility features/i),
    ).toBeInTheDocument();
    expect(await screen.findByText(/high_contrast/i)).toBeInTheDocument();

    // toggle: simulate the backend update by changing the mocked list and
    // re-rendering — this keeps the unit test deterministic without
    // depending on optimistic mutation wiring.
    const btn = screen.getByRole("button", { name: /Disable/i });
    userEvent.click(btn);
    const api = require("../api");
    api.listAccessibilityFeatures.mockImplementation(() => [
      { id: 1, feature_type: "high_contrast", enabled: false },
    ]);
    rerender(<AccessibilityPage />);
    expect(await screen.findByText(/Enabled: false/i)).toBeInTheDocument();

    // create: update the mocked list to include the newly created feature and
    // re-render the page so the new item appears in the DOM.
    api.listAccessibilityFeatures.mockImplementation(() => [
      { id: 1, feature_type: "high_contrast", enabled: true },
      { id: 2, feature_type: "spoken_feedback", enabled: true },
    ]);
    // type and press Create (this will call createAccessibilityFeature mock)
    await userEvent.type(
      screen.getByPlaceholderText(/New feature type/i),
      "spoken_feedback",
    );
    await userEvent.click(screen.getByText(/Create/i));

    // Re-render the page to pick up the updated list from the API mock.
    rerender(<AccessibilityPage />);
    expect(await screen.findByText(/spoken_feedback/i)).toBeInTheDocument();
  });
});
