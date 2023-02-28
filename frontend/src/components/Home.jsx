import React, { useEffect } from 'react'
import { useState } from 'react';
import Searchbar from './Searchbar';
import Navbar from './Navbar';
import Globe from './Globe'
import Hero from './Hero';
import Sidebar from './Sidebar';
import Api from "./api.js"

let api = new Api()

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
  const [fruitList, setFruitList] = useState([])
  const [fruitsLoaded, setFruitsLoaded] = useState(false)

  useEffect(() => {
    if (fruitList.length == 0) {
      api.getAllFruits().then((f) => {
        setFruitList(f.fruits) 
      })
    }
  })

  const handleSearchbarData = (dataFromChild) => {
    api.getFruitDetails(dataFromChild.id).then((d) => {
      return api.getCountriesByFruitId(d.id)
    }).then((c) => {
      setCountries(c.countries)
    })
  };

  function isoToCountry(iso) {
    return fruitCountries.find((c) => {
      return c.iso_code === iso
    })
  }

  function countryIdToFruitVar(countryId) {
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
          <Searchbar fruitList={fruitList} onFruitSelected={handleSearchbarData}/>
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