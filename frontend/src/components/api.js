export default class Api {
    constructor() {
        this.apiBase = "http://localhost:5000/api/v1/"
    }
    getAllFruits() {
        const url = this.apiBase + "fruit/"
        return fetch(url, {
            method: "GET"
        }).then((r) => r.json())
    }
    getFruitDetails(id) {
        const url = this.apiBase + "fruit/" + id + '?detailed=true'
        return fetch(url, {
            method: "GET"
        }).then((r) => r.json())
    }
    getCountriesByFruitId(id) {
        const url = this.apiBase + `country/fruit/${id}?detailed=true`
        return fetch(url, {
            method: "GET"
        }).then((r) => r.json())
    }
}