import React from 'react';
import {CgCloseR} from 'react-icons/cg'
import Sidebarlist from './Sidebarlist';

const Sidebar = (props) => {
    return (
        <div>
            {props.showSidebar &&
             <div className='cursor-pointer fixed right-10 top-6 z-50 block' onClick={props.onToggle}>
                {!props.showSidebar && <CgCloseR color='black' />}
                {props.showSidebar && <CgCloseR color='white' />}
            </div>
            }
        <div
            className={`top-0 right-0 w-[100%] md:w-[33%] bg-blue-600 md:rounded-l-xl p-10 pl-20 text-white fixed h-full z-40 ease-in-out duration-300 ${
            props.showSidebar ? "translate-x-0 " : "translate-x-full"
            }`}>
           {
                props.country &&
                <Sidebarlist fruit={props.fruit} country={props.country} fruitVar={props.fruitVar}/>
           }
        </div>
        </div>
  );
};

export default Sidebar;