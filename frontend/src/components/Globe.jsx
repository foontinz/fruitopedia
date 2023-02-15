import React from 'react';
import * as THREE from 'three'
import { useState, useEffect } from 'react';
import { default as Earth } from 'react-globe.gl'

const Globe = () => {
    const [countries, setCountries] = useState([]);


    // useEffect(() => {
    //     // load specific country
    //     fetch('countries.geojson').then(res => res.json()).then(res => setCountries(res.features.filter(f => f.properties.ISO_A3 == "AFG")));
    // }, []);

    useEffect(() => {
        // load each country
        fetch('countries.geojson').then(res => res.json()).then(res => setCountries(res.features));
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

    // gen earth-like texture function

    const genRandColor = () => {
        let r = Math.floor(Math.random()*100 + 100).toString(16)
        let g = Math.floor(Math.random()*100 + 155).toString(16)
        let b = Math.floor(Math.random()*50 + 40).toString(16)

        let res = '#' + r + g +b
        return  res
    }

    // custom globe material

    const globeMaterial = new THREE.MeshPhongMaterial(
        {
            color: 0x0489AF,
            specular: 0x270AFF,
            shininess: 30,
        }
    )

    return (
        <div className='flex justify-center my-12 md:my-5'>
            <Earth
                width={windowWidth}
                height={windowHeight/2}
                // globeImageUrl="https:///unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
                // bumpImageUrl="https://unpkg.com/three-globe/example/img/earth-topology.png"
                globeMaterial={globeMaterial}
                backgroundColor={'#E8EEF2'}
                polygonsData={countries}
                polygonResolution={3}
                polygonMargin={0.3}
                polygonCapColor={() => genRandColor()}
                polygonSideColor={() => '#000000'}
                polygonStrokeColor={() => false}
            />
        </div>
    );
};

export default Globe;