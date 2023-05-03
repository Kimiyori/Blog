import { Box, Container, Typography } from "@mui/material";
import { FormProvider, SubmitHandler, useForm } from "react-hook-form";
import { object, string, TypeOf } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import FormInput from "components/shared/Entity/FormInput";
import { useEffect } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { LoadingButton } from "@mui/lab";
import React from "react";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useLoginUserMutation } from "api/authApi";
import "styles/pages/auth.scss";

const loginSchema = object({
  username: string().min(1, "Full name is required").max(100),
  password: string()
    .min(1, "Password is required")
    .min(6, "Password must be more than 8 characters")
    .max(32, "Password must be less than 32 characters"),
});

export type LoginInput = TypeOf<typeof loginSchema>;

const LoginPage = () => {
  const methods = useForm<LoginInput>({
    resolver: zodResolver(loginSchema),
  });
  // ? API Login Mutation
  const [loginUser, { isLoading, isError, error, isSuccess }] =
    useLoginUserMutation();

  const navigate = useNavigate();
  const location = useLocation();

  const from = ((location.state as any)?.from.pathname as string) || "/";
  const {
    reset,
    handleSubmit,
    formState: { isSubmitSuccessful },
  } = methods;

  useEffect(() => {
    if (isSuccess) {
      toast.success("You successfully logged in", {
        position: toast.POSITION.TOP_RIGHT,
      });
      navigate(from);
    }
    if (isError) {
      toast.error((error as any).data.detail, {
        position: toast.POSITION.TOP_RIGHT,
      });
    }

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isLoading]);

  useEffect(() => {
    if (isSubmitSuccessful) {
      reset();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isSubmitSuccessful]);

  const onSubmitHandler: SubmitHandler<LoginInput> = (values) => {
    // ? Executing the loginUser Mutation
    loginUser(values);
  };
  return (
      <Container  className="auth-main">
        <Box className="auth-box">
          <Typography component="h1">
            Welcome Back!
          </Typography>
          <FormProvider {...methods}>
            <Box
              component="form"
              className="auth-form "
              onSubmit={handleSubmit(onSubmitHandler)}
              noValidate
              autoComplete="off"
              maxWidth="27rem"
              width="100%"
            >
              <FormInput name="username" label="Username" />
              <FormInput name="password" label="Password" type="password" />
              <Typography sx={{ fontSize: "0.9rem", mb: "1rem" }}>
                Need an account?
                <Link className="link-item" to="/register">
                  Sign Up
                </Link>
              </Typography>
              <LoadingButton
                variant="contained"
                fullWidth
                className="loading-button"
                disableElevation
                type="submit"
                loading={isLoading}
              >
                Login
              </LoadingButton>
            </Box>
          </FormProvider>
        </Box>
      </Container>
  );
};

export default LoginPage;
