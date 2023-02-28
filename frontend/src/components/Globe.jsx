import React from 'react';
import * as THREE from 'three'
import { useState, useEffect, useRef } from 'react';
import { default as Earth } from 'react-globe.gl'

let fetchedCountries = []
let fetchedCords = []

let cords = [0, 0]

const Globe = ({countries, onCountrySelected}) => {
    const [selectedCountries, setSelectedCountries] = useState([]);
    const [hoverD, setHoverD] = useState();

    const [windowWidth, setWindowWidth] = useState(0);
    const [windowHeight, setWindowHeight] = useState(0);

    let resizeWindow = () => {
        setWindowWidth(window.innerWidth);
        setWindowHeight(window.innerHeight);
    };

    useEffect(() => {
        if (fetchedCountries.length == 0) {
            fetch('countries.geojson').then(res => res.json()).then(res => fetchedCountries = res.features)
        }
        fetch('country-lat-long.json').then(res => res.json()).then(res => fetchedCords = res.ref_country_codes)
        resizeWindow();
        window.addEventListener("resize", resizeWindow);
        return () => window.removeEventListener("resize", resizeWindow);
    }, []);

    const globeEl = useRef()

    function isoToCords(iso) {
        let findByIso = fetchedCords.filter(c => c.alpha3 == iso)
        let res = [findByIso[0].latitude, findByIso[0].longitude]
        return res
    }

    function filterSelectedCountries(countryIsos) {
        if (fetchedCountries.length == 0) {
            return 0
        }
        let filteredCountries = fetchedCountries.filter((c) => {
            return countryIsos.some((iso) => {
                return c.properties.ISO_A3 == iso
            })
        })
        if (filteredCountries.length === 0) {
            return -1
        }
        setSelectedCountries(filteredCountries)
        cords = isoToCords(filteredCountries[0].properties.ISO_A3)
    }

    useEffect(() => {
        console.log("Countries: ", countries)
        let selectedCodes = countries.map((c) => {
            return c.iso_code
        })
        filterSelectedCountries(selectedCodes)
        globeEl.current.pointOfView({ lat: cords[0], lng: cords[1], altitude: 2 }); 
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
                polygonSideColor={() => '#000000'}
                polygonAltitude={d => d === hoverD ? 0.06 : 0.04}
                polygonCapColor={d => d === hoverD ? 'red' : 'lightgreen'}
                onPolygonHover={setHoverD}
                polygonLabel={({ properties: d }) => `
                    <b>${d.ADMIN} (${d.ISO_A2})</b>
                `}                    
                polygonsTransitionDuration={300}
                onPolygonClick={(c) => {
                    onCountrySelected(c.properties.ISO_A3)
                }}
            />
        </div>
    );
};

export default Globe;