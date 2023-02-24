import React from 'react'
import Searchbar from './Searchbar';
import Navbar from './Navbar';
import Globe from './Globe'
import Hero from './Hero';

const Home = () => {
  return (
    <div>
          <Navbar></Navbar>
          <Hero></Hero>
          <Searchbar></Searchbar>
          <Globe></Globe>
    </div>
  );
};

export default Home;