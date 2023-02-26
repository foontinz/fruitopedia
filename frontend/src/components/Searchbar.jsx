import React, { useEffect } from 'react'
import { useState } from 'react'
import { FcSearch } from 'react-icons/fc'

let fruitData = [
  {
    id: 0,
    name: "Apple"
  },
  {
    id: 1,
    name: "Orange"
  },
  {
    id: 2,
    name: "Pear"
  }
]

const Searchbar = (props) => {
  const [searchInput, setSearchInput] = useState("")

  function findMatch(input, element) {
    if (input.length == 0) {
      return null // no input
    }

    input = input.toLowerCase()
    let copyOfElement = element.toLowerCase()
    
    if(copyOfElement.startsWith(input)) {
      console.log(`Suggest: ${element}`)
      return element
    }
  }

  function handleChange(event) {
    let input = event.target.value
    const allLi = document.querySelectorAll("#suggestions-bar li")

    for (let i = 0; i < fruitData.length; i++) {
      let res = findMatch(input, fruitData[i].name)

      let noRepeat = allLi.forEach(e => e.id != res) // check whether element is already typed or not
      if (noRepeat === undefined) {
        noRepeat = true
      }
      if (res != null && noRepeat) { // if there is input and element doesnt repeat
        const ul = document.getElementById("suggestions-bar")
        const li = document.createElement("li")

        li.dataset.fruitName = fruitData[i].name
        li.dataset.fruitId = fruitData[i].id
        li.innerHTML = res
        li.className = "h-[30px] pl-[5px] w-[250px] md:w-[400px] hover:bg-blue-500 hover:rounded-md"
        li.addEventListener("click", (e) => {
          let id = e.target.dataset.fruitId
          event.target.value = res

          let allLi = document.querySelectorAll("#suggestions-bar li")
          allLi.forEach(e => e.remove()) // clear all li

          props.onFruitSelected(fruitData.find((el) => el.id == id))
        })

        ul.appendChild(li)
      } else {
        allLi.forEach(e => e.remove()) // if there is no input, clear all
      }
    } 
  }

  return (
    <div className='flex justify-center'>
        <div className='mt-5 w-[250px] md:w-[400px]'>
          <div id='search-bar' className='flex justify-center p-1 
            bg-gray-200 border-[4px] rounded-xl border-gray-400 focus-within:border-blue-500
            transition duration-700'>
            <input onChange={handleChange} className='w-full text-black p-1 bg-gray-200 font-bold bg-grey
              outline-none ' type="text" placeholder="Looking for some fruits.." />
            <div className=''>
              <FcSearch size={30} />
            </div>
          </div>
          <ul id='suggestions-bar' className='bg-gray-200 rounded-md text-start cursor-pointer absolute z-50'>
          </ul>
        </div>
    </div>
  );
};

export default Searchbar;