import React from 'react';

const Login = (props) => {

    return (
        props.showLogin &&
        <div>
            <div onClick={() => props.changeState(false)} style={{backgroundColor: 'rgba(0, 0, 0, 0.5)'}}
         className='absolute top-0 left-0 w-screen h-screen z-[10]'>
            </div>
            <div className='absolute z-[100] top-[50%] md:mt-[-200px] left-[50%] md:ml-[-200px]
            mt-[-130px] ml-[-160px]
             w-[320px] h-[260px] md:w-[400px] md:h-[250px] bg-slate-200 border rounded-md'>
                <div className='flex flex-col m-4'>
                    <h1 className='text-center'>Login to your Fruitopedia account 🍒</h1>
                    <div className='mt-2'>
                        <ul>
                            <li className='my-2'>
                               <p>Username/Email</p>
                               <input className='border-2 border-black rounded-md p-1 w-full' type={"text"} placeholder='Type your fruity username'></input>
                            </li>
                            <li className='my-2'>
                               <p>Password</p>
                               <input className='border-2 border-black rounded-md p-1 w-full' type={"text"} placeholder='Type your fruity password'></input>
                            </li>
                        </ul>
                    </div>
                    <div className='flex justify-center mt-2'>
                        <button className='border-2 rounded-md border-blue-500 px-3 p-1 hover:bg-blue-500 transition duration-200'>Log in</button>
                    </div>
                </div>
            </div>
        </div>
        
    );
};

export default Login;