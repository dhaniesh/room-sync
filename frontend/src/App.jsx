import "./App.css";
import { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [date, setDate] = useState(new Date());
  const [time, setTime] = useState("00:00");
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    async function fetchRooms() {
      console.log({date, time})
      const body = {
        date: new Date(date).toISOString().slice(0, 10),
        time,
      };
      console.log({body})
      try {
        const response = await axios.post(
          "http://localhost:8000/meeting/availability",
          body
        );
        setRooms(response.data);
      } catch (error) {
        console.error("Error fetching rooms:", error);
      }
    }
    fetchRooms();
  }, [time, date]);

  function onChange(e, destinationFunction) {
    console.log(e.target.value);
    destinationFunction(e.target.value);
  }

  function onSearch(e) {}
  return (
    <>
      <div className="font-serif flex flex-col justify-center items-center gap-y-4 text-center pb-40">
        <p className="text-6xl font-bold text-stone-500">Room Sync</p>
        <p className="text-xl">Book a meeting now</p>
      </div>
      <div className="font-serif flex justify-center gap-x-20">
        <div>
          <p className="text-xl">Date</p>
          <input
            type="date"
            onChange={(e) => onChange(e, setDate)}
            value={date}
          />
        </div>
        <div>
          <p className="text-xl">Time</p>
          <input
            type="time"
            onChange={(e) => onChange(e, setTime)}
            value={time}
          />
        </div>
        <div>
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 border border-blue-700 rounded">
            Search
          </button>
        </div>
        <div>
          <p className="text-xl">Available rooms</p>
          <select>
            {rooms.length > 0 ? (
              rooms.map((room) => (
                <option key={room.id} value={room.id}>
                  {room.name}
                </option>
              ))
            ) : (
              <option>No rooms available</option>
            )}
          </select>
        </div>
      </div>
    </>
  );
}

export default App;
