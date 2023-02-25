import React from 'react';
import Hero from './Hero';
import Navbar from './Navbar';

const About = () => {
    return (
        <div>
            <Navbar></Navbar>
            <Hero></Hero>
            <div className='flex m-5 md:mx-[30%] mx-[10%] justify-center'>
                <div>
                    <h1 className=''>
                        Welcome to Fruitopedia - our platform dedicated to providing information about fruits and their growing seasons. Here, you will find valuable information about various fruits and the different regions in which they grow.                        
                    </h1>
                    <h1 className='mt-5'>
                        Fruits are an important part of a healthy diet and come in many different varieties, each with their unique taste, texture, and nutritional value. Understanding the growing seasons of different fruits can help you make informed choices about what  fruits to buy and when to buy them. 
                    </h1>
                    <h1 className='mt-5 text-center'>
                        Enjoy using our website ! 🥝
                    </h1>
                </div>
            </div>
        </div>
    );
};

export default About;