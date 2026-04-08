/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import BatchTable from "../src/components/inventory/BatchTable";

const batches = [
  {
    id: "1",
    file_name: "a.csv",
    upload_date: new Date().toISOString(),
    processed_rows: 10,
    valid_rows: 8,
    invalid_rows: 2,
    status: "processed"
  }
];

test("renders batch row", () => {
  render(<BatchTable batches={batches} onRowClick={() => {}} />);
  expect(screen.getByText("a.csv")).toBeInTheDocument();
  expect(screen.getByText("processed")).toBeInTheDocument();
});
