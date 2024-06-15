import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import searchIcon from '../images/search.png';
import axios from 'axios';

const publicUrl = 'http://0.0.0.0:8000';

const SearchBar = () => {
  const navigate = useNavigate();
  const [searchValue, setSearchValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearchInputChanges = (e) => {
    if (!loading) {
      setSearchValue(e.target.value);
    }
  };

  const callSearchFunction = async (e) => {
    e.preventDefault();
    if (loading) return; // Evita múltiples clics
    setLoading(true);
    setError(null);
    console.log(`Making request to ${publicUrl}/clients with text: ${searchValue}`);

    try {
      const response = await axios.post(`${publicUrl}/clients`, { text: searchValue });
      console.log('Response from backend:', response.data);
      navigate('/results', { state: { results: response.data.selected_companies } });
    } catch (error) {
      console.error('Error fetching potential customers:', error);
      setError('An error occurred while searching. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="search-bar">
      <form className="test" onSubmit={callSearchFunction}>
        <div className="inner-form">
          <div className="basic-search">
            <div className="input-field">
              <input
                value={searchValue}
                onChange={handleSearchInputChanges}
                type="text"
                placeholder="Describe your target company..."
                disabled={loading} // Deshabilita el campo de entrada mientras se carga
              />
              <div className="icon-wrap">
                <img
                  src={searchIcon}
                  width="24"
                  height="24"
                  onClick={callSearchFunction}
                  alt="search"
                  style={{ cursor: loading ? 'not-allowed' : 'pointer' }} // Cambia el cursor si está cargando
                />
              </div>
            </div>
          </div>
        </div>
      </form>
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default SearchBar;