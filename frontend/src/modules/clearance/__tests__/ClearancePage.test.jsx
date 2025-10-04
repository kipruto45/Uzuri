import React from "react";
import { render, screen, act } from "../../../test-utils";
import ClearancePage from "../ClearancePage";

jest.mock("../api", () => ({
  listClearanceDocuments: jest.fn(() => ({ results: [] })),
  uploadClearanceDocument: jest.fn(),
  deleteClearanceDocument: jest.fn(),
}));

test("renders clearance header and upload section", async () => {
  await act(async () => {
    render(<ClearancePage />);
  });
  expect(
    screen.getByRole("heading", { name: /clearance documents/i }),
  ).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/search documents/i)).toBeInTheDocument();
});
