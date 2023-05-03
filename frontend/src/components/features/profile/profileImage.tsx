import { Avatar, IconButton } from "@mui/material";
import { useState } from "react";
import { HiOutlineUpload } from "react-icons/hi";
import "styles/pages/user_profile.scss";
import { useAppSelector } from "app/store";
import { useUpdateUserMutation } from "api/userApi";
import FullScreenLoader from "../../core/FullScreenLoader";
import { useParams } from "react-router-dom";
const ProfileImage = ({ img }: { img: string }) => {
  const { username } = useParams();
  const [profileImage, setProfileImage] = useState(img);
  const [isHovering, setIsHovering] = useState(false);
  const user = useAppSelector((state) => state.userState.user);
  const [updateImage, { isLoading }] = useUpdateUserMutation();
  const handleMouseOver = () => {
    setIsHovering(true);
  };
  const handleMouseOut = () => {
    setIsHovering(false);
  };
  const uploadImage = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event?.target?.files?.[0] as File;
    const data = await updateImage({
      username: user?.username as string,
      body: { image: file },
    });
    if ("data" in data) {
      setProfileImage(data?.data?.image as string);
    }
    handleMouseOut();
  };
  return (
    <>
      <div
        className="profile-image"
        onMouseOver={handleMouseOver}
        onMouseOut={handleMouseOut}
      >
        {user?.username === username && isHovering && !isLoading && (
          <div>
            <input
              accept="image/*"
              onChange={async (e) => {
                await uploadImage(e);
              }}
              id="icon-button-file"
              type="file"
              style={{ display: "none" }}
            />
            <IconButton
              color="primary"
              aria-label="upload picture"
              className="profile-image_hover"
            >
              <label htmlFor="icon-button-file">
                <HiOutlineUpload className="profile-image_hover_upload-button" />
              </label>
            </IconButton>
          </div>
        )}
        {isLoading && <FullScreenLoader />}
        <Avatar
          src={"http://127.0.0.1:81/files/" + profileImage}
          className="profile-image-img"
        ></Avatar>
      </div>
    </>
  );
};

export default ProfileImage;
