import React from 'react';

const Sidebarlist = (props) => {
    return (
        <div>
            <ul>
                <li className='text-xl text-center'><strong>{props.country.name}
                {` (${props.country.iso_code})`}</strong></li>
                <div className='mt-2'>
                    <li>Description: {props.country.description}</li>
                    <li>Fruits: {props.fruit.map((el) => el.name).join(', ')} </li>
                    <li>Varieties: {props.fruitVar.map((el) => el.name).join(', ')}</li>
                </div>
            </ul>
        </div>
    );
};

export default Sidebarlist;