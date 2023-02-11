import React from 'react'
import {useRef} from 'react'
import {FcSearch} from 'react-icons/fc'

const Hero = () => {
  return (
    <div className='mt-6 text-center font-light'>
      <h1 className='text-[38px] md:text-[50px]'>
        Fruitopedia
      </h1>
      <h1 className='text-[10px] md:text-[10px] md:mt-2'>
        From people to people
      </h1>
      <div className='flex justify-center mt-5'>
        <div id='search-bar' className='flex justify-center p-1 
        bg-gray-200 border-[4px]  rounded-xl border-gray-400 focus-within:border-blue-500
        transition duration-700'>
          <input className='text-black p-1 bg-gray-200  font-bold bg-grey w-[400px]
          outline-none ' type="text" placeholder="Looking for some fruits.."/>
          <div className=''>
            <FcSearch size={30}/>
          </div>
      </div>
    </div>
  </div>
  );
};

export default Hero;