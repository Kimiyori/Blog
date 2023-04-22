import { Avatar, IconButton } from "@mui/material";
import { useState } from "react";
import { HiOutlineUpload } from "react-icons/hi";
import "styles/pages/user_profile.scss";
import { useAppSelector } from "app/store";
import { useUpdateUserMutation } from "api/userApi";
import FullScreenLoader from "../FullScreenLoader";
const ProfileImage = ({ img }: { img: string }) => {
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
    await updateImage({
      username: user?.username as string,
      body: { image: file },
    });
  };
  return (
    <>
      <div
        className="profile-image"
        onMouseOver={handleMouseOver}
        onMouseOut={handleMouseOut}
      >
        {isHovering && !isLoading && (
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
        <Avatar src={'http://127.0.0.1:81/'+'files/'+img} className="profile-image-img"></Avatar>
      </div>
    </>
  );
};

export default ProfileImage;
