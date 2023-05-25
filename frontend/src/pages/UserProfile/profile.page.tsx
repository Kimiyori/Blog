import { Button } from "@mui/material";
import { useParams } from "react-router-dom";
import { useAppSelector } from "app/store";
import { useGetUserQuery } from "api/userApi";
import { useNavigate } from "react-router-dom";
import "styles/pages/user_profile.scss";
import banner from "./profile_pattern.jpg";
import ProfileImage from "../../components/features/profile/profileImage";
import ProfileDataBlock from "components/features/profile/profileBlock";
const ProfilePage = () => {
  const { username } = useParams();
  const navigate = useNavigate();
  const user = useAppSelector((state) => state.userState.user);
  const { data } = useGetUserQuery(
    username as string
  );
  return (
    <>
      {data && (
        <div className="user-profile">
          <div className="upper-banner">
            <img src={banner} alt="" />
          </div>
          <div className="bottom-user-block">
            <div className="user-nav">
              <ProfileImage img={data.image} />
              <Button
                variant="outlined"
                disabled={username !== user?.username}
                onClick={() => navigate(`/users/${username}/settings`)}
              >
                Settings
              </Button>
            </div>
            <div className="user-data">
              <ProfileDataBlock label="Username" data={data.username} />
              <ProfileDataBlock label="User ID" data={data._id} />
              <ProfileDataBlock label="User type" data={data.type} />
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ProfilePage;
