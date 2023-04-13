import "styles/components/search_bar.scss";
import { AiOutlineSearch } from "react-icons/ai";
import { InputBase } from "@mui/material";
const SearchBar = () => {
  return (
    <div className="search">
      <div className="search-icon-wrapper">
        <AiOutlineSearch />
      </div>
      <InputBase 
        className="search-input"
        placeholder="Search…"
        inputProps={{ "aria-label": "search" }}
      />
    </div>
  );
};

export default SearchBar;
