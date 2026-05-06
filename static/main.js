function updateFileName(input) {
      const fileName = input.files[0] ? input.files[0].name : "";
      const displayId = input.id === 'file-holerites' ? 'name-holerites' : 'name-ponto';
      document.getElementById(displayId).textContent = fileName;
    }