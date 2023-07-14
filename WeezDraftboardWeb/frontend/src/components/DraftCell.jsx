import React, { useState } from "react";

function DraftCell(props) {
  const [isHovered, setIsHovered] = useState(false);
  const [isClicked, setIsClicked] = useState(false);
  const isEvenRow = props.rowNumber % 2 === 0;
  const arrow = isEvenRow ? "←" : "→";

  const handleMouseEnter = () => {
    setIsHovered(true);
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
  };

  const handleClick = () => {
    setIsClicked(!isClicked);
  };
  //{//<div className={`${props.position} cell-container`}>}
  return (
    <div
      className={`${props.position} cell-container ${
        isHovered ? "hovered" : ""
      } ${isClicked ? "clicked" : ""}`}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={handleClick}
    >
      <div className={`${props.position} ${props.cellLocation}`}></div>
      <div className="player">
        <div className="player-name">{props.name}</div>
        <div className="position">
          {props.position} - {props.team}
        </div>
      </div>
      <div className="cell-direction-wrap">{arrow}</div>
      <div className="player-avatar-container">{props.playerID}</div>
    </div>
  );
}

export default DraftCell;
