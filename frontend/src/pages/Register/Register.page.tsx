import { Box, Container, Typography } from "@mui/material";
import { FormProvider, SubmitHandler, useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import FormInput from "components/shared/Entity/FormInput";
import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LoadingButton } from "@mui/lab";
import { useRegisterUserMutation } from "api/userApi";

import "styles/pages/auth.scss";
import NotifyMessage from "features/notifyMessage";

const registerSchema = z
  .object({
    username: z.string().min(1, "Full name is required").max(100),
    email: z
      .string()
      .min(1, "Email is required")
      .email("Email Address is invalid"),
    password: z
      .string()
      .min(1, "Password is required")
      .min(8, "Password must be more than 8 characters")
      .max(32, "Password must be less than 32 characters"),
    passwordConfirm: z.string().min(1, "Please confirm your password"),
  })
  .refine((data) => data.password === data.passwordConfirm, {
    path: ["passwordConfirm"],
    message: "Passwords do not match",
  });

export type RegisterInput = z.TypeOf<typeof registerSchema>;

const RegisterPage = () => {
  const methods = useForm<RegisterInput>({
    resolver: zodResolver(registerSchema),
  });

  // ? Calling the Register Mutation
  const [registerUser, { isLoading, isSuccess, error, isError }] =
    useRegisterUserMutation();

  const navigate = useNavigate();

  const {
    reset,
    handleSubmit,
    formState: { isSubmitSuccessful },
  } = methods;
  NotifyMessage(
    "User registered successfully",
    isLoading,
    isSuccess,
    isError,
    error
  );
  useEffect(() => {
    if (isSuccess) {
      navigate("/login");
    }
  }, [isSuccess, navigate]);

  useEffect(() => {
    if (isSubmitSuccessful) {
      reset();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSubmitSuccessful]);
  const onSubmitHandler: SubmitHandler<RegisterInput> = (values) => {
    registerUser(values);
  };
  return (
    <Container className="auth-main">
      <Box className="auth-box">
        <Typography component="h1">Welcome!</Typography>
        <FormProvider {...methods}>
          <Box
            data-testid="form"
            role="form"
            component="form"
            className="auth-form"
            onSubmit={handleSubmit(onSubmitHandler)}
            noValidate
            autoComplete="off"
            maxWidth="27rem"
            width="100%"
          >
            <FormInput name="username" label="Username" />
            <FormInput name="email" label="Email Address" type="email" />
            <FormInput name="password" label="Password" type="password" />
            <FormInput
              name="passwordConfirm"
              label="Confirm Password"
              type="password"
            />
            <Typography
              className="link-item"
              sx={{ fontSize: "0.9rem", mb: "1rem" }}
            >
              Already have an account? <Link to="/login">Login here</Link>
            </Typography>

            <LoadingButton
              variant="contained"
              fullWidth
              className="loading-button"
              disableElevation
              type="submit"
              loading={isLoading}
            >
              Sign Up
            </LoadingButton>
          </Box>
        </FormProvider>
      </Box>
    </Container>
  );
};

export default RegisterPage;
