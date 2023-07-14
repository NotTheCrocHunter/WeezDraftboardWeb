import React, { useState } from "react";
import "../App.css";
import DraftCell from "./DraftCell";
import EmptyCell from "./EmptyCell";
import DraftHeader from "./DraftHeader";

const Draftboard = (props) => {
  const [rounds, setRounds] = useState(15); // State for the number of rounds
  const [teams, setTeams] = useState(12); // State for the number of teams

  // Event handler for round selection change
  const handleRoundChange = (event) => {
    setRounds(parseInt(event.target.value));
  };

  // Event handler for team selection change
  const handleTeamChange = (event) => {
    setTeams(parseInt(event.target.value));
  };

  // Function to render the table headers
  const renderTableHeaders = () => {
    const headers = [];
    //headers.push(<th key={0}></th>); // Add an empty header cell at the beginning
    headers.push(<DraftHeader key={0} headerValue="" />); // Add an empty header cell at the beginning
    for (let i = 1; i <= teams; i++) {
      headers.push(<DraftHeader key={i} headerValue={i} />);
      //headers.push(<th className="draftboard-heading" key={i}>{i}</th>);
    
    }
    return headers;
  };

  // Function to render the table rows
  const renderTableRows = () => {
    const rows = [];
    for (let i = 1; i <= rounds; i++) {
      const cells = [];
      for (let j = 1; j <= teams; j++) {
        const columnNumber = i % 2 === 0 ? teams - j + 1 : j;
        /*HERE GOES THE PLAYER ARRAY*/
        const players = props.players;
        const playerIndex = (i - 1) * teams + (columnNumber - 1);
        
        const player = players[playerIndex];
        const cellLocation = `${playerIndex}, ${i}.${columnNumber}`;
        console.log(player);
        const cellValue = player ? (
          <DraftCell
            key={player.id}
            name={player.name}
            team={player.team}
            position={player.position}
            cellLocation={cellLocation}
            playerID={player.id}
            rowNumber={i}
          />
        ) : (
          <EmptyCell cellLocation={cellLocation} rowNumber={i} />
        );
        //console.log(cellValue);

        cells.push(<td key={j}>{cellValue}</td>); // Render DraftCell component passing player props

        //cells.push(<td key={j}>{cellValue}</td>);
      }
      //<th>Round {i}</th>
      rows.push(
        <tr key={i}>
          <DraftHeader key={0} headerValue={i} />
          {cells}
        </tr>
      );
    }
    return rows;
  };

  return (
    <div>

      <div>
        <label htmlFor="rounds">Select number of rounds:</label>
        <select id="rounds" value={rounds} onChange={handleRoundChange}>
          {/* Generate options for round selection */}
          {Array.from(Array(14).keys()).map((number) => (
            <option key={number + 2} value={number + 2}>
              {number + 2}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label htmlFor="teams">Select number of teams:</label>
        <select id="teams" value={teams} onChange={handleTeamChange}>
          {/* Generate options for team selection */}
          {Array.from(Array(11).keys()).map((number) => (
            <option key={number + 2} value={number + 2}>
              {number + 2}
            </option>
          ))}
        </select>
      </div>
      
      <div className="draftboard-table-container">
        <table>
          <thead>
            <tr>
              {/* Render the table headers */}
              {renderTableHeaders()}
            </tr>
          </thead>
          <tbody>
            {/* Render the table rows */}
            {renderTableRows()}
          </tbody>
        </table>
      </div>
      w
    </div>
  );
};

export default Draftboard;

/* OLD RETURN




*/
