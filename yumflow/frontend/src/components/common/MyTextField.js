import React from "react";
import { withStyles, ThemeProvider } from "@mui/styles";
import { createTheme, TextField } from "@mui/material";

const StyledTextField = withStyles(() => ({
  root: {
    "& label": {
      width: "100%",
      textAlign: "right",
      zIndex: 1,
      right: 5,
      left: -5,
      transformOrigin: "top right",
      "&.Mui-focused": {
        transformOrigin: "top right",
      },
    },
  },
}))(TextField);

const theme = createTheme({});

function MyTextField({
  id,
  label,
  placeholder = "",
  type = "text",
  dir = "rtl",
}) {
  return (
    <ThemeProvider theme={theme}>
      <StyledTextField
        variant="standard"
        style={{ direction: dir }}
        id={id}
        label={label}
        placeholder={placeholder}
        type={type}
      />
    </ThemeProvider>
  );
}

export default MyTextField;
