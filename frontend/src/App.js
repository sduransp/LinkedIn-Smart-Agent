import './App.css';
import NavBar from './components/NavBar';
import SearchBar from './components/SearchBar';
import React from 'react';
import BrandIcons from './components/BrandIcons'
import 'bootstrap/dist/css/bootstrap.min.css';
import Trending from './components/Trending';
import Products from './components/Products';
import Results from './components/Results';
import Login, { Render } from 'react-login-page';
import Logo from 'react-login-page/logo';

import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";

const publicUrl = "http://0.0.0.0:8000"

const App = () => {
    return (
      <div class='page'>
        <div>
          <NavBar/>
        </div>
        <div class='background'>
          <div class='search-title'>
              <div class= 'title'>
                The LinkedIn Agent
              </div>
              <div class= 'subtitle'>
                Unleash the power of AI to discover your business opportunities
              </div>
          </div>
          <SearchBar />
          <BrandIcons/>
        </div>
        <Routes>
          <Route exact path={publicUrl+'/'} component={Trending}/>
          <Route path={publicUrl +'/search/:key'} component={Products}/>
          <Route path="/results" element={<Results />} /> {/* Nueva ruta para resultados */}
        </Routes>
      </div>
    );
}


export default App;
