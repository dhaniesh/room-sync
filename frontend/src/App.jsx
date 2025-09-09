import "./App.css";
import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  let rooms = [];

  useEffect(() => {
    async function fetchRooms() {
      const data = await axios
        .get("http://localhost:8000/room")
        .then((response) => console.log(response.data))
        .catch((error) => console.error(error));
    }
    rooms = fetchRooms();
    console.log(rooms);
  }, []);

  function onDateChange(e, destinationFunction) {
    console.log(e.target.value);
    destinationFunction(e.target.value);
  }
  return (
    <>
      <div className="font-serif flex flex-col justify-center items-center gap-y-4 text-center pb-40">
        <p className="text-6xl font-bold text-stone-500">Room Sync</p>
        <p className="text-xl">Book a meeting now</p>
      </div>
      <div className="font-serif flex justify-center gap-x-20">
        <div>
          <p className="text-xl">Start time</p>
          <input
            type="date"
            onChange={(e) => onDateChange(e, setStartDate)}
            value={new Date(startDate).toISOString().slice(0, 10)}
          />
        </div>
        <div>
          <p className="text-xl">End time</p>
          <input
            type="date"
            onChange={(e) => onDateChange(e, setEndDate)}
            value={new Date(endDate).toISOString().slice(0, 10)}
          />
        </div>
        <div>
          <p className="text-xl">Available rooms</p>
          <select>
            {rooms.map((room) => (
              <option key={room.id} value={room.id}>
                {room.name}
              </option>
            ))}
          </select>
        </div>
      </div>
    </>
  );
}

export default App;
