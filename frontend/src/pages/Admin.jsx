import axios from "axios"


export default function Admin() {
const addMovie = () => {
axios.post("http://localhost:8000/admin/movies", {
title: "Matrix",
description: "Sci-fi",
duration: 120
})
}


return <button onClick={addMovie}>Add Movie</button>
}