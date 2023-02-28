import React from 'react'
import { useState } from 'react';
import Searchbar from './Searchbar';
import Navbar from './Navbar';
import Globe from './Globe'
import Hero from './Hero';
import Sidebar from './Sidebar';

let fruitData = [
  {
    id: 0,
    name: "Apple",
    varieties: [1, 2, 3]
  },
  {
    id: 1,
    name: "Orange",
    varieties: [4]
  },
  {
    id: 2,
    name: "Pear",
    varieties: [7, 8, 9]
  }
]

let fruitVarieties = [
  {
    "id": 1,
    "name": "Fuji",
    "fruit": 0,
    "description": "Some description",
    "origin_countries": [5]
  },
  {
    "id": 2,
    "name": "Semerinka",
    "fruit": 0,
    "description": "Some description",
    "origin_countries": [1]
  },
  {
    "id": 3,
    "name": "Rihard",
    "fruit": 0,
    "description": "Some description",
    "origin_countries": [4]
  },
  {
    "id": 4,
    "name": "Navel",
    "fruit": 1,
    "description": "Some description",
    "origin_countries": [1, 3, 6]
  },
]

let fruitCountries = [
  {
    "id": 1,
    "name": "Ukraine",
    "iso_code": "UKR",
    "description": "nice country",
    "own_varieties": []
  },
  {
    "id": 2,
    "name": "Uganda",
    "iso_code": "UGA",
    "description": "nice country",
    "own_varieties": []
  },
  {
    "id": 3,
    "name": "Russia",
    "iso_code": "RUS",
    "description": "nice country",
    "own_varieties": []
  },
  {
    "id": 4,
    "name": "Canada",
    "iso_code": "CAN",
    "description": "nice country",
    "own_varieties": []
  },
  {
    "id": 5,
    "name": "China",
    "iso_code": "CHN",
    "description": "nice country",
    "own_varieties": []
  },
  {
    "id": 6,
    "name": "Germany",
    "iso_code": "DEU",
    "description": "nice country",
    "own_varieties": []
  },
]

const Home = () => {
  const [countries, setCountries] = useState([]);
  const [dataFromGlobe, setDataFromGlobe] = useState()
  const [fruitVar, setFruitVar] = useState([])
  const [fruit, setFruit] = useState([])
  const [showSidebar, setShowSidebar] = useState(false)

  const handleSearchbarData = (dataFromChild) => {
    // must be fetch !
    let fruitDetails = fruitData.find((el) => {
      return el.id === dataFromChild.id
    })

    let varietyIds = fruitDetails.varieties
    let filteredVarieties = fruitVarieties.filter((v) => {
      return varietyIds.some((id) => {
        return v.id === id
      })
    })

    let originCountries = filteredVarieties.flatMap((v) => {
      return v.origin_countries
    })

    originCountries = [...new Set(originCountries)] // remove duplicates

    let countries = fruitCountries.filter((c) => {
      return originCountries.some((id) => {
        return c.id === id
      })
    })
    setCountries(countries)
    console.log(countries)
  };

  function isoToCountry(iso) {
    return fruitCountries.find((c) => {
      return c.iso_code === iso
    })
  }

  function countryIdToFruitVar(countryId) { // returns array with fruitvarieties belongs to its country
    let res = []
    fruitVarieties.filter((v) => {
      if(v.origin_countries.some((each) => each == countryId)) {
        res.push(v)
      }
    })
    return res
  }

  function countryIdToFruit(countryId) {
    let res = []
    fruitData.filter((f) => {
      if(f.varieties.some((each) => each == countryId)) {
        res.push(f)
      }
    })
    return res
  }
  
  return (
    <div>
          <Navbar/>
          <Hero/>
          <Searchbar onFruitSelected={handleSearchbarData}/>
          <Globe onCountrySelected={(val) => {
            let country = isoToCountry(val)
            let fruitVar = countryIdToFruitVar(country.id)
            let fruit = countryIdToFruit(country.id)
            
            setFruit(fruit)
            setFruitVar(fruitVar)
            setDataFromGlobe(country)
            setShowSidebar(true)
          }} countries={countries}/>
          <Sidebar onToggle={() => setShowSidebar(!showSidebar)} 
          fruit={fruit} country={dataFromGlobe} fruitVar={fruitVar} showSidebar={showSidebar}/>
    </div>
  );
};

export default Home;