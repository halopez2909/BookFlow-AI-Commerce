/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import ErrorsTable from "../src/components/inventory/ErrorsTable";

const errors = [
  { id: "e1", row_number: 2, error_type: "MISSING_ISBN", message: "Falta ISBN", fix_hint: "Revisar" }
];

test("renders error row", () => {
  render(<ErrorsTable errors={errors} />);
  expect(screen.getByText("Falta ISBN")).toBeInTheDocument();
  expect(screen.getByText("MISSING_ISBN")).toBeInTheDocument();
});
