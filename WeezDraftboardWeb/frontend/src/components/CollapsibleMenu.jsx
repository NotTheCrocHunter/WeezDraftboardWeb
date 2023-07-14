import React, { useState } from "react";

function CollapsibleMenu() {
  const [isCollapsed, setIsCollapsed] = useState(true);

  const toggleMenu = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div>
      <button onClick={toggleMenu}>
        {isCollapsed ? "Show Menu" : "Hide Menu"}
      </button>
      {!isCollapsed && (
        <ul>
          <li>Menu Item 1</li>
          <li>Menu Item 2</li>
          <li>Menu Item 3</li>
        </ul>
      )}
    </div>
  );
}

export default CollapsibleMenu;
