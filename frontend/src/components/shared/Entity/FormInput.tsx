import {
  FormHelperText,
  Typography,
  FormControl,
  Input,
  InputProps,
} from "@mui/material";
import { FC } from "react";
import { Controller, useFormContext } from "react-hook-form";
import "styles/components/form_input.scss";


type IFormInputProps = {
  name: string;
  label: string;
} & InputProps;

const FormInput: FC<IFormInputProps> = ({ name, label, ...otherProps }) => {
  const {
    control,
    formState: { errors },
  } = useFormContext();
  return (
    <Controller
      control={control}
      defaultValue=""
      name={name}
      render={({ field }) => (
        <FormControl fullWidth sx={{ mb: 2 }}>
          <Typography variant="body2" sx={{  mb: 1, fontWeight: 500 }}>{label}</Typography>
          <Input
            {...field}
            fullWidth
            className="form-input"
            disableUnderline
            error={!!errors[name]}
            {...otherProps}
          />
          <FormHelperText error={!!errors[name]}>
            {errors[name] && (errors[name]?.message as string)}
          </FormHelperText>
        </FormControl>
      )}
    />
  );
};

export default FormInput;
