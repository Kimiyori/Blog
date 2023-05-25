import { render,screen } from "@testing-library/react";
import ProfileDataBlock from "../profileBlock";

test("rendering", async () => {
  render(<ProfileDataBlock label="labeltest" data="datatest" />);
  expect(screen.getByText(/labeltest/i)).toBeInTheDocument()
  expect(screen.getByText(/datatest/i)).toBeInTheDocument()
});
