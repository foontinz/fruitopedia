import React from 'react'
import { useState } from 'react';
import Searchbar from './Searchbar';
import Navbar from './Navbar';
import Globe from './Globe'
import Hero from './Hero';

let fruitData = [
  {
    id: 0,
    name: "Apple",
    varieties: [1, 2, 3]
  },
  {
    id: 1,
    name: "Orange",
    varieties: [4, 5, 6]
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
  "origin_countries": [1]
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
]

const Home = () => {
  const [countries, setCountries] = useState([]);

  const handleChildData = (dataFromChild) => {
    console.log("handleChildData: " + dataFromChild)
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
  return (
    <div>
          <Navbar></Navbar>
          <Hero></Hero>
          <Searchbar onFruitSelected={handleChildData}></Searchbar>
          <Globe countries={countries}></Globe>
    </div>
  );
};

export default Home;