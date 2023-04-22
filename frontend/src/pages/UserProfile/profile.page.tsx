import { Avatar, Button } from "@mui/material";
import { useParams } from "react-router-dom";
import { useAppSelector } from "app/store";
import { useGetUserQuery } from "api/userApi";
import "styles/pages/user_profile.scss";
import banner from "./profile_pattern.jpg";
import ProfileImage from "../../components/core/UserProfile/profileImage";
import ProfileDataBlock from "components/core/UserProfile/profileBlock";
const ProfilePage = () => {
  const { username } = useParams();
  const { data, isLoading, isFetching, isError } = useGetUserQuery(
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
              <div>
                <Button variant="outlined">Settings</Button>
              </div>
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
