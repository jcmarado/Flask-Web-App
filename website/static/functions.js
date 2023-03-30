function openForm() {
    fetch("/delete-note", {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
      }).then((_res) => {
        window.location.href = "/";
      });
    }
    document.getElementById("myForm").style.display = "block";
  
  function closeForm() {
    document.getElementById("myForm").style.display = "none";
  } 