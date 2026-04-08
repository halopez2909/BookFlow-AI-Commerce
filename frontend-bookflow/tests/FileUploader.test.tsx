/// <reference types="vitest" />
import { render, screen } from "@testing-library/react";
import FileUploader from "../src/components/inventory/FileUploader";

test("renders file input and button", () => {
  render(<FileUploader onResult={() => {}} />);
  const input = document.querySelector("input[type=file]");
  expect(input).toBeTruthy();
  expect(screen.getByText(/Subir archivo/i)).toBeInTheDocument();
});
