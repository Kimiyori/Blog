import { useAppSelector } from "app/store";
import {
  useGetUserQuery,
  useUpdateUserMutation,
  UpdateUser,
} from "api/userApi";
import {
  Box,
  Button,
  Divider,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { object, string, TypeOf } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { FormProvider, SubmitHandler, useForm } from "react-hook-form";
import FormInput from "components/shared/Entity/FormInput";
import { LoadingButton } from "@mui/lab";
import { useEffect } from "react";
const changeEmailSchema = object({
  email: string()
    .min(1, "Email address is required")
    .email("Email Address is invalid"),
});
export type ChangeEmailInput = TypeOf<typeof changeEmailSchema>;
const ChangeEmail = () => {
  const methods = useForm<ChangeEmailInput>({
    resolver: zodResolver(changeEmailSchema),
  });
  const {
    reset,
    handleSubmit,
    formState: { isSubmitSuccessful },
  } = methods;
  const user = useAppSelector((state) => state.userState.user);
  const [updateEmail, { isLoading }] = useUpdateUserMutation();
  const onSubmitHandler: SubmitHandler<ChangeEmailInput> = (values) => {
    user && updateEmail({ username: user.username, body: values });
  };
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
            <Typography variant="h6">Change email</Typography>
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
          <FormInput name="email" label="New email" type="email" />
        </FormProvider>
      </Box>
    </>
  );
};

export default ChangeEmail;
