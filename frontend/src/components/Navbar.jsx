import React from 'react';
import { RxHamburgerMenu } from 'react-icons/rx'
import { SlClose } from 'react-icons/sl'
import { useState, useEffect } from 'react';
import Login from './Login';
import Registration from './Registration'

const Navbar = () => {
    const [isOpen, setOpen] = useState(false)
    const [showLogin, setShowLogin] = useState(false)
    const [showRegistration, setShowRegistration] = useState(false)

    function toggleShrink() {
        const nav = document.getElementById('nav')
        isOpen ? nav.className = 'block' : nav.className = 'hidden md:block'
    }

    useEffect(() => {
        toggleShrink()
    })

    return (
        <div className=''>
            <nav className="bg-[#C7EDE4] flex">
                <div className="w-full p-6">
                    <div onClick={() => setOpen(!isOpen)} className='md:hidden'>
                        {!isOpen && <RxHamburgerMenu color='black' />}
                        {isOpen && <SlClose color='black' />}
                    </div>
                    <div id='nav' className="hidden md:block">
                        <ul className="flex text-center justify-center mt-6 md:mt-0 flex-col md:flex-row text-[#2D2A32] text-sm font-medium">
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="/" className="hover:underline">
                                    Home
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="/" className="hover:underline">
                                    Articles
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="about" className="hover:underline">
                                    About
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="/" className="hover:underline">
                                    FAQ
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="/" className="hover:underline">
                                    Contact
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="/" className="hover:underline">
                                    Support
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
                <Login changeState={(state) => setShowLogin(state)} showLogin={showLogin}/>
                <Registration changeState={(state) => setShowRegistration(state)} showRegistration={showRegistration}/>
                <div id='authorization' className='absolute right-1 h-[68px] flex justify-center items-center mx-4 text-sm'>
                    <div className='border rounded-md border-black hover:bg-blue-400 mx-2 p-1.5 px-3 transition hover-duration:500'>
                        <h1 onClick={() => setShowLogin(true)} className='hover:cursor-pointer '>
                                Login
                            </h1>
                    </div>
                    <div className='border rounded-md border-black hover:bg-blue-400 mx-2 p-1.5 transition hover-duration:500'>
                        <h1 onClick={() => setShowRegistration(true)} className='hover:cursor-pointer '>
                                Register
                            </h1>
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Navbar;