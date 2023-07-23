import React, { useState } from 'react';
import DraftCell from './DraftCell';

function DraftTable(props) {
    
    const players = props.players;
    console.log(players);
    
    return (
        <table> 
            <tbody>
                {players.map((playerItem, index) => (
                    <DraftCell 
                        key={playerItem.id}
                        name={playerItem.name}
                        team={playerItem.team}
                        position={playerItem.position}
                    />
                )
                )}
                    
            </tbody>        
        </table>
    );
    }

export default DraftTable;