     // Get all table cells
     const cells = document.querySelectorAll('td');
      
     // Add event listener to each cell
     cells.forEach(cell => {
       cell.addEventListener('click', () => {
         // Toggle the "clicked" class
         cell.classList.toggle('clicked');
       });
     });