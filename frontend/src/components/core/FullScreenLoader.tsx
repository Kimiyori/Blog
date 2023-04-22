import { Box, CircularProgress, Container } from "@mui/material";

const FullScreenLoader = () => {
  return (
    <Container>
      <Box
        display="flex"
        alignItems="center"
        justifyContent="center"
        sx={{
          height: "100%",
          zIndex: 1,
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
        }}
      >
        <CircularProgress />
      </Box>
    </Container>
  );
};

export default FullScreenLoader;
