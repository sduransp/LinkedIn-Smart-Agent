import './App.css';
import NavBar from './components/NavBar';
import SearchBar from './components/SearchBar';
import React from 'react';
import Results from './components/Results';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Routes, Route } from 'react-router-dom';

const Home = () => {
  return (
    <div className="background">
      <div className="search-title">
        <div className="title">The LinkedIn Agent</div>
        <div className="subtitle">Unleash the power of AI to discover your business opportunities</div>
      </div>
      <SearchBar />
    </div>
  );
};

const App = () => {
  return (
    <div className="page">
      <NavBar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </div>
  );
};

export default App;