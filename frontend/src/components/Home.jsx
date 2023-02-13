import React from 'react'
import Searchbar from './Searchbar';
import Navbar from './Navbar';

const Home = () => {
  return (
    <div>
      <Navbar></Navbar>
      <div className='text-[#37393A]'>
        <div className='mt-2 text-center font-light'>
          <h1 className='text-[38px] md:text-[50px]'>
            Fruitopedia
          </h1>
          <h1 className='text-[10px] md:text-[10px] md:mt-2'>
            From people to people
          </h1>
          <Searchbar></Searchbar>
      </div>
    </div>
  </div>
  );
};

export default Home;