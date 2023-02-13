import React from 'react'
import {FcSearch} from 'react-icons/fc'

const Searchbar = () => {
  return (
    <div className='flex justify-center mt-5'>
        <div id='search-bar' className='flex justify-center p-1 
        bg-gray-200 border-[4px] rounded-xl border-gray-400 focus-within:border-blue-500
        transition duration-700'>
          <input className='text-black p-1 bg-gray-200  font-bold bg-grey w-[250px] md:w-[400px]
          outline-none ' type="text" placeholder="Looking for some fruits.."/>
          <div className=''>
            <FcSearch size={30}/>
          </div>
      </div>
    </div>
  );
};

export default Searchbar;