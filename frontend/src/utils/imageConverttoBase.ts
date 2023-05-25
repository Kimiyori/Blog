export const blobToData = (blob: File) => {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onloadend = () =>
      resolve((reader.result as string).split(",").pop());
    reader.readAsDataURL(blob);
  });
};
