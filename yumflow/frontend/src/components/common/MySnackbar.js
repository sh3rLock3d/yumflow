import { Snackbar } from "@mui/material";
import MuiAlert from "@mui/material/Alert";
import React from "react";
import { createTheme, ThemeProvider } from "@mui/material/styles";

const theme = createTheme({
  components: {
    MuiAlert: {
      styleOverrides: {
        action: {
          alignItems: "center",
          padding: "0 15px 0 0",
        },
      },
    },
  },
});

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

function MySnackbar({ open, onClose, message, variant }) {
  return (
    <ThemeProvider theme={theme}>
      <Snackbar
        open={open}
        // autoHideDuration={6000}
        onClose={onClose}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert onClose={onClose} severity={variant} sx={{ width: "100%" }}>
          {message}
        </Alert>
      </Snackbar>
    </ThemeProvider>
  );
}

export default MySnackbar;
