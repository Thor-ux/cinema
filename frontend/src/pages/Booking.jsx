import axios from "axios"


export default function Booking() {
const reserve = () => {
axios.post("http://localhost:8000/booking", {
showtime_id: 1,
seat_id: 2
})
}


return <button onClick={reserve}>Reserve Seat</button>
}