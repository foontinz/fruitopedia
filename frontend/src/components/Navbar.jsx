import React from 'react';
import { RxHamburgerMenu } from 'react-icons/rx'
import { SlClose } from 'react-icons/sl'
import { useState, useEffect } from 'react';

const Navbar = () => {
    const [isOpen, setOpen] = useState(false)

    function toggleShrink() {
        const nav = document.getElementById('nav')
        isOpen ? nav.className = 'block' : nav.className = 'hidden md:block'
        console.log(`open: ${isOpen}`)
    }

    // useEffect allows to call function after rendering DOM
    useEffect(() => {
        toggleShrink()
    })

    return (
        <div className=''>
            <nav className="bg-[#C7EDE4]">
                <div className="w-full p-6">
                    <div onClick={() => setOpen(!isOpen)} className='md:hidden'>
                        {!isOpen && <RxHamburgerMenu color='black' />}
                        {isOpen && <SlClose color='black' />}
                    </div>
                    <div id='nav' className="hidden md:block">
                        <ul className="flex text-center justify-center flex-col md:flex-row text-[#2D2A32] text-sm font-medium">
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="#" className="hover:underline">
                                    Home
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="#" className="hover:underline">
                                    Articles
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="#" className="hover:underline">
                                    About
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="#" className="hover:underline">
                                    FAQ
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="#" className="hover:underline">
                                    Contact
                                </a>
                            </li>
                            <li className='md:mx-4 py-4 md:py-0'>
                                <a href="#" className="hover:underline">
                                    Support
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </div>
    );
};

export default Navbar;