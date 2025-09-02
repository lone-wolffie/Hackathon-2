let currentIndex = 0;
let recipes = [];

const prevBtn = document.getElementById("prevBtn");
const nextBtn = document.getElementById("nextBtn");
const container = document.getElementById("recipeCards");

// Hide buttons initially
prevBtn.style.display = "none";
nextBtn.style.display = "none"; 

document.getElementById("searchBtn").addEventListener("click", async () => {
  nextBtn.style.display = "none";
  prevBtn.style.display = "none";
  container.innerHTML = '<h3 class="search-message">Searching for recipes...</h3>';

  
  const ingredients = document.getElementById("ingredientsInput").value;
  const response = await fetch("/recommend", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ingredients })
  });
  recipes = await response.json();
  currentIndex = 0;
  
  if (recipes.length > 0) {
    showRecipe(currentIndex);
    prevBtn.style.display = "inline-block";
    nextBtn.style.display = "inline-block";
  } else {
    container.innerHTML = "<h4>No recipes found. Try different ingredients.</h4>";
  }
});

prevBtn.addEventListener("click", () => {
  if (recipes.length > 0) {
    currentIndex = (currentIndex - 1 + recipes.length) % recipes.length;
    showRecipe(currentIndex);
  }
});

nextBtn.addEventListener("click", () => {
  if (recipes.length > 0) {
    currentIndex = (currentIndex + 1) % recipes.length;
    showRecipe(currentIndex);
  }
});

function showRecipe(index) {
  const container = document.getElementById("recipeCards");
  const recipe = recipes[index];
  
  const ingredientsList = recipe.ingredients.map(i => `<li>${i}</li>`).join("");
  const stepsList = recipe.steps.map((s, i) => `<li>${s}</li>`).join("");
  
  
  container.innerHTML = `
    <div class="card">
      <h3>${recipe.title}</h3>
      <p><strong>Ready in:</strong> ${recipe.readyInMinutes} minutes</p>
      <p><strong>Calories:</strong> ${recipe.calories}</p>
      <h4>Ingredients:</h4>
      <ul>${ingredientsList}</ul>
      <h4>Steps:</h4>
      <ol>${stepsList}</ol>
    </div>
  `;

  
}
