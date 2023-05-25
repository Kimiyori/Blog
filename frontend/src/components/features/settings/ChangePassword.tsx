import { useAppSelector } from "app/store";
import { useUpdateUserMutation } from "api/userApi";
import { Box, Divider, Typography } from "@mui/material";
import { object, string, TypeOf } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { FormProvider, SubmitHandler, useForm } from "react-hook-form";
import FormInput from "components/shared/Entity/FormInput";
import { LoadingButton } from "@mui/lab";
import { useEffect } from "react";
import NotifyMessage from "features/notifyMessage";
const changePasswordSchema = object({
  password: string()
    .min(1, "Password is required")
    .min(8, "Password must be more than 8 characters")
    .max(32, "Password must be less than 32 characters"),
  passwordConfirm: string().min(1, "Please confirm your new password"),
}).refine((data) => data.password === data.passwordConfirm, {
  path: ["passwordConfirm"],
  message: "Passwords do not match",
});
export type ChangePasswordInput = TypeOf<typeof changePasswordSchema>;
const ChangePassword = () => {
  const methods = useForm<ChangePasswordInput>({
    resolver: zodResolver(changePasswordSchema),
  });
  const {
    reset,
    handleSubmit,
    formState: { isSubmitSuccessful },
  } = methods;
  const user = useAppSelector((state) => state.userState.user);
  const [updatePassword, { isLoading, isSuccess, isError, error }] =
    useUpdateUserMutation();
  const onSubmitHandler: SubmitHandler<
    Omit<ChangePasswordInput, "passwordConfirm">
  > = (values) => {
    user && updatePassword({ userData: values });
  };
  NotifyMessage(
    "You have successfully changed your password",
    isLoading,
    isSuccess,
    isError,
    error
  );
  useEffect(() => {
    if (isSubmitSuccessful) {
      reset();
    }
  });
  return (
    <>
      <Box className="settings-block">
        <FormProvider {...methods}>
          <Box
            className="settings-block__label"
            component="form"
            onSubmit={handleSubmit(onSubmitHandler)}
            noValidate
            autoComplete="off"
          >
            <Typography variant="h6">Change password</Typography>
            <LoadingButton
              variant="outlined"
              disableElevation
              type="submit"
              loading={isLoading}
            >
              Save
            </LoadingButton>
          </Box>
          <Divider />
          <FormInput name="password" label="New password" type="password" />
          <FormInput
            name="passwordConfirm"
            label="Confirm new password"
            type="password"
          />
        </FormProvider>
      </Box>
    </>
  );
};

export default ChangePassword;
