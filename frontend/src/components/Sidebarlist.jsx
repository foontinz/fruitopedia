import React from 'react';

const Sidebarlist = (props) => {
    return (
        <div>
            <ul>
                <li>Country: {props.country.name} 
                {` (${props.country.iso_code})`}</li>
                <li>Description: {props.country.description}</li>
                <li>Fruits: {props.fruit.map((el) => el.name).join(', ')} </li>
                <li>Varieties: {props.fruitVar.map((el) => el.name).join(', ')}</li>
            </ul>
        </div>
    );
};

export default Sidebarlist;