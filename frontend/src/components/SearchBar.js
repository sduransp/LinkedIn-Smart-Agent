import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import searchIcon from '../images/search.png'
import axios from "axios";

const publicUrl = "http://0.0.0.0:8000"

const SearchBar = (props) => {
    let navigate = useNavigate();
    const [searchValue, setSearchValue] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const handleSearchInputChanges = (e) => {
      setSearchValue(e.target.value);
    }
    console.log(`Making request to ${publicUrl}/clients with text: ${searchValue}`);
    const callSearchFunction = async (e) => {
      e.preventDefault();
      setLoading(true);
      setError(null);
      console.log(`Making request to ${publicUrl}/clients with text: ${searchValue}`);

      try {
          const response = await axios.post(`${publicUrl}/clients`, { text: searchValue });
          console.log("Response from backend:", response.data);
          navigate(`/results`, { state: { results: response.data.selected_companies } });
      } catch (error) {
          console.error("Error fetching potential customers:", error);
          setError("An error occurred while searching. Please try again.");
      } finally {
          setLoading(false);
      }
  };

    return (
        <div class="search-bar">
            <form class= "test" onSubmit={callSearchFunction}>
              <div class="inner-form">
                <div class="basic-search">
                  <div class="input-field">
                    <input  value={searchValue} onChange={handleSearchInputChanges} type="text" placeholder = "Describe your target company..."/>
                    <div class="icon-wrap">
                      <img src={searchIcon} width="24" height="24"  onClick={callSearchFunction} type="submit" value="SEARCH" >

                      </img>
                    </div>
                  </div>
                </div>
              </div>
            </form>
    </div>
      );
}
export default SearchBar