import React from 'react';
import { useState, useEffect } from 'react';
import { default as Earth } from 'react-globe.gl'

const Globe = () => {
    const [countries, setCountries] = useState([]);


    useEffect(() => {
        // load data
        fetch('countries.geojson').then(res => res.json()).then(res => setCountries(res.features.filter(f => f.properties.ISO_A3 == "AFG")));
    }, []);

    // resizing window

    const [windowWidth, setWindowWidth] = useState(0);
    const [windowHeight, setWindowHeight] = useState(0);
    let resizeWindow = () => {
        setWindowWidth(window.innerWidth);
        setWindowHeight(window.innerHeight);
    };

    useEffect(() => {
        resizeWindow();
        window.addEventListener("resize", resizeWindow);
        return () => window.removeEventListener("resize", resizeWindow);
    }, []);

    console.log(windowWidth, windowHeight)

    return (
        <div className='flex justify-center my-12 md:my-5'>
            <Earth
                width={windowWidth}
                height={windowHeight/2}
                globeImageUrl="earth_texture.jpg"
                backgroundColor='#E8EEF2'
                polygonsData={countries}
                polygonResolution={3}
                polygonMargin={0.3}
                polygonCapColor={() => '#00FF00'}
                polygonStrokeColor={() => `#000000`}
                polygonSideColor={() => '#000000'}
            />
        </div>
    );
};

export default Globe;