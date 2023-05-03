import { Typography } from "@mui/material";
import "styles/pages/user_profile.scss";

const ProfileDataBlock = ({ label, data }: { label: string; data: string }) => {
  return (
    <>
      <div className="user-data_block">
        <Typography variant="h6">{label}:</Typography>
        <Typography variant="body1">{data}</Typography>
      </div>
    </>
  );
};

export default ProfileDataBlock;
