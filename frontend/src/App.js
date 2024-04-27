import './App.css';
import NavBar from './components/NavBar';
import SearchBar from './components/SearchBar';
import React from 'react';
import BrandIcons from './components/BrandIcons'
import 'bootstrap/dist/css/bootstrap.min.css';
import Trending from './components/Trending';
import Products from './components/Products';




import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";



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
          <Route exact path={process.env.PUBLIC_URL+'/'} component={Trending}/>
          <Route path={process.env.PUBLIC_URL +'/search/:key'} component={Products}/>
        </Routes>
      </div>
    );
}


export default App;
