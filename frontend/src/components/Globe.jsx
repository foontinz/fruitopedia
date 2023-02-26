import React from 'react';
import * as THREE from 'three'
import { useState, useEffect, useRef } from 'react';
import { default as Earth } from 'react-globe.gl'

let fetchedCountries = []

const Globe = ({countries}) => {
    const [selectedCountries, setSelectedCountries] = useState([]);

    const [windowWidth, setWindowWidth] = useState(0);
    const [windowHeight, setWindowHeight] = useState(0);

    let resizeWindow = () => {
        setWindowWidth(window.innerWidth);
        setWindowHeight(window.innerHeight);
    };

    useEffect(() => {
        if (fetchedCountries.length == 0) {
            fetch('countries.geojson').then(res => res.json()).then((res) => fetchedCountries = res.features);
        }
        resizeWindow();
        window.addEventListener("resize", resizeWindow);
        return () => window.removeEventListener("resize", resizeWindow);
    }, []);

    const genRandHighlightColor = () => {
        let r = Math.floor(Math.random()*50 + 205).toString(16)
        let g = Math.floor(Math.random()*1 + 20).toString(16)
        let b = Math.floor(Math.random()*1 + 50).toString(16)

        let res = '#' + r + g +b
        return  res
    }

    const globeEl = useRef();

    function zoomToCountry(lat, lng, altitude = 1.5) {
        useEffect(() => {
            globeEl.current.pointOfView({ lat: lat, lng: lng, altitude: altitude });
          }, []);
    }

    function filterSelectedCountries(countryIsos) {
        if (fetchedCountries.length == 0) {
            return 0
        }
        let filteredCounties = fetchedCountries.filter((c) => {
            return countryIsos.some((iso) => {
                return c.properties.ISO_A3 == iso
            })
        })
        setSelectedCountries(filteredCounties)
    }

    useEffect(() => {
        let selectedCodes = countries.map((c) => {
            return c.iso_code
        })
        filterSelectedCountries(selectedCodes)
    }, [countries])

    return (
        <div className='flex justify-center my-12 md:my-5'>
            <Earth
                ref={globeEl}
                width={windowWidth}
                height={windowHeight/2}
                globeImageUrl="https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/i/4013c234-b843-4331-84cd-8a86d940d26f/dcrbmun-38493001-d0cc-4bd6-9acb-2bf1109b488b.jpg"
                backgroundColor={'#E8EEF2'}
                polygonsData={selectedCountries}
                polygonResolution={3}
                polygonMargin={0.3}
                polygonCapColor={() => genRandHighlightColor()}
                polygonSideColor={() => '#000000'}
                polygonStrokeColor={() => false}
            />
        </div>
    );
};

export default Globe;