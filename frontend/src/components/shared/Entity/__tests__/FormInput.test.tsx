import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import FormInput from "../FormInput";
import { FormProvider, useForm } from "react-hook-form";
import userEvent from "@testing-library/user-event";

const BASIC_CONFIGURATTION = { name: "username", label: "Username" };
type TestTypeInput = {
  username: string;
  password: string;
};
const Wrapper = (props: any) => {
  const formMethods = useForm<TestTypeInput>();

  return <FormProvider {...formMethods}>{props.children}</FormProvider>;
};
describe("rendering", () => {
  describe("initial state", () => {
    test("label", async () => {
      render(
        <Wrapper>
          <FormInput {...BASIC_CONFIGURATTION} />
        </Wrapper>
      );
      expect(screen.getByText(/Username/i)).toBeInTheDocument();
    });
    test("input", async () => {
      render(
        <Wrapper>
          <FormInput {...BASIC_CONFIGURATTION} />
        </Wrapper>
      );
      expect(screen.getByLabelText("Username")).toHaveValue("");
    });
  });
  test("types into input", async () => {
    render(
      <Wrapper>
        <FormInput {...BASIC_CONFIGURATTION} />
      </Wrapper>
    );
    const input = screen.getByLabelText(/Username/i) as HTMLInputElement;
    fireEvent.input(input, {
        target: {
          value: "test_input"
        }
      });
    // await userEvent.type(input, "test_input");
      expect(input).toHaveValue("test_input");
  
  });
});
