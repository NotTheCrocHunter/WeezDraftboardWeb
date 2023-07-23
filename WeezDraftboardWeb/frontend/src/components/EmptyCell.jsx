import React, { useState } from "react";

function EmptyCell(props) {
  const isEvenRow = props.rowNumber % 2 === 0;
  const arrow = isEvenRow ? "←" : "→";

  return (
    <div className={`undrafted-cell cell-container`}>
      <div className="pick-number">{props.cellLocation}</div>
      <div className="cell-direction-wrap">{arrow}</div>
    </div>
  );
}

export default EmptyCell;
