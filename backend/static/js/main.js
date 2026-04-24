let allMovies = [];

async function loadMovies() {
  const res = await fetch("/api/movies");
  allMovies = await res.json();
  displayMovies(allMovies);
}

function displayMovies(movies) {
  const grid = document.getElementById("movieGrid");

  if (movies.length === 0) {
    grid.innerHTML = `
      <div class="empty-state">
        <h4>No movies yet </h4>
        <p>Add some from the <a href="/admin">Admin Panel</a></p>
      </div>`;
    return;
  }

  grid.innerHTML = movies.map(movie => `
    <div class="movie-card">

      ${movie.poster_url
        ? `<img src="${movie.poster_url}" alt="${movie.title}"
             onerror="this.outerHTML='<div class=no-poster></div>'">`
        : `<div class="no-poster"></div>`
      }

      <!-- OVERLAY: fades in on hover -->
      <div class="card-overlay">
        <div class="overlay-title">${movie.title}</div>
        <div class="overlay-desc">${movie.description || "No description available."}</div>
      </div>

      <!-- BOTTOM: always visible -->
      <div class="card-info">
        <h6>${movie.title}</h6>
        <div class="card-meta">${movie.genre || "Unknown"} &bull; ${movie.year || "?"}</div>
        <div class="rating-stars">${getStars(movie.rating)}</div>
      </div>

    </div>
  `).join("");
}

function getStars(rating) {
  if (!rating) return "*****";
  const full  = Math.round(rating);
  const empty = 5 - full;
  return "*".repeat(full) + "*".repeat(empty);
}

function filterMovies() {
  const query = document.getElementById("searchInput").value.toLowerCase();
  const filtered = allMovies.filter(m =>
    m.title.toLowerCase().includes(query) ||
    (m.genre && m.genre.toLowerCase().includes(query))
  );
  displayMovies(filtered);
}

loadMovies();