// Load movies 
async function loadMovies() {
  const res = await fetch("/api/movies");
  const movies = await res.json();
  const tbody = document.getElementById("movieTableBody");

  if (movies.length === 0) {
    tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted">No movies yet. Add one above!</td></tr>`;
    return;
  }

  tbody.innerHTML = movies.map(m => `
    <tr>
      <td>${m.id}</td>
      <td>
        ${m.poster_url
          ? `<img src="${m.poster_url}" style="width:50px;height:70px;object-fit:cover;border-radius:4px;"
               onerror="this.src=''">`
          : ""}
      </td>
      <td><strong>${m.title}</strong></td>
      <td>${m.genre || "-"}</td>
      <td>${m.year || "-"}</td>
      <td>${m.rating ? "★".repeat(Math.round(m.rating)) : "-"}</td>
      <td>
        <!-- Edit button — fills the form above -->
        <button class="btn btn-sm btn-warning me-1" onclick="editMovie(${m.id})"> Edit</button>
        <!-- Delete button -->
        <button class="btn btn-sm btn-danger" onclick="deleteMovie(${m.id}, '${m.title}')"> Delete</button>
      </td>
    </tr>
  `).join("");
}

// Save 
async function saveMovie() {
  // Get values from the form
  const id          = document.getElementById("editId").value;
  const title       = document.getElementById("title").value.trim();
  const genre       = document.getElementById("genre").value.trim();
  const year        = document.getElementById("year").value;
  const description = document.getElementById("description").value.trim();
  const rating      = document.getElementById("rating").value;
  const poster_url  = document.getElementById("poster_url").value.trim();

  // Title is required
  if (!title) {
    alert("Please enter a movie title!");
    return;
  }

  const payload = { title, genre, year, description, rating, poster_url };

  let res;
  if (id) {
    // EDITING
    res = await fetch(`/api/movies/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  } else {
    //  ADDING
    res = await fetch("/api/movies", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
  }

  const data = await res.json();

  if (data.success) {
    resetForm();
    loadMovies();
  } else {
    alert("Error: " + (data.error || "Something went wrong"));
  }
}

// Fill form with movie data for editing
async function editMovie(id) {
  const res   = await fetch(`/api/movies/${id}`);
  const movie = await res.json();

  // Fill each form field with existing data
  document.getElementById("editId").value      = movie.id;
  document.getElementById("title").value       = movie.title;
  document.getElementById("genre").value       = movie.genre      || "";
  document.getElementById("year").value        = movie.year       || "";
  document.getElementById("description").value = movie.description|| "";
  document.getElementById("rating").value      = movie.rating     || "";
  document.getElementById("poster_url").value  = movie.poster_url || "";

  // Change form title to show editing
  document.getElementById("formTitle").textContent = ` Editing: ${movie.title}`;

  // Scroll up to the form
  window.scrollTo({ top: 0, behavior: "smooth" });
}
// Delete 
async function deleteMovie(id, title) {
  // Ask user to confirm before deleting
  if (!confirm(`Are you sure you want to delete "${title}"?`)) return;

  const res  = await fetch(`/api/movies/${id}`, { method: "DELETE" });
  const data = await res.json();

  if (data.success) {
    loadMovies();
  } else {
    alert("Delete failed: " + data.error);
  }
}
// Reset the form back to "Add" mode
function resetForm() {
  document.getElementById("editId").value      = "";
  document.getElementById("title").value       = "";
  document.getElementById("genre").value       = "";
  document.getElementById("year").value        = "";
  document.getElementById("description").value = "";
  document.getElementById("rating").value      = "";
  document.getElementById("poster_url").value  = "";
  document.getElementById("formTitle").textContent = "+ Add New Movie";
}
// Load movies 
loadMovies();