import React, { useState, useEffect } from "react";
import "./App.css";
import Draftboard from "./components/Draftboard";
import CollapsibleMenu from "./components/CollapsibleMenu";
import axios from "axios";
/*need to make array from django api. localhost:8000/api/adp */

function App () {
  
  const [players, setPlayers] = useState([]); // State for the number of rounds
  
  useEffect(() => {
    axios.get("http://localhost:8000/api/adp")
      .then((res) => {
        setPlayers(res.data);
        console.log(res.data);
      })
      .catch((error) => {
        console.error("Error fetching players:", error);
      });
  }, []);

    return (
      <div>
      <div className="top-section">
        <CollapsibleMenu />
        <h1 className="heading">Weez Tools</h1>
      </div>
        
        <div className="draftboard-container">
          <h2>Draftboard JSX</h2>
          <Draftboard players={players} />
        </div>
      </div>
    );
  
}

export default App;
