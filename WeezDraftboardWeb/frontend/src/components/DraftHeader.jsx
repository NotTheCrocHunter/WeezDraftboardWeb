import React from "react";

function DraftHeader(props) {
  return (
    <th className="draftboard-header">
        {props.headerValue}
    </th>
  );
}

export default DraftHeader;