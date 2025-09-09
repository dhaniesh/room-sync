import "./App.css";
import { useState } from "react";

function App() {
  return (
    <>
      <div className="font-serif flex flex-col justify-center items-center gap-y-4 text-center pb-40">
        <p className="text-6xl font-bold">Room Sync</p>
        <p className="text-xl">Book a meeting now</p>
      </div>
      <div className="font-serif flex justify-center gap-x-20">
        <div>
          <p className="text-xl">Start time</p>
        </div>
        <p className="text-xl">End time</p>
        <p className="text-xl">Available rooms</p>
      </div>
    </>
  );
}

export default App;
