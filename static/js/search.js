const sdgs = [
  { number: 1, title: "1. No Poverty" },
  { number: 2, title: "2. Zero Hunger" },
  { number: 3, title: "3. Good Health and Well-being" },
  { number: 4, title: "4. Quality Education" },
  { number: 5, title: "5. Gender Equality" },
  { number: 6, title: "6. Clean Water and Sanitation" },
  { number: 7, title: "7. Affordable and Clean Energy" },
  { number: 8, title: "8.Decent Work and Economic Growth" },
  { number: 9, title: "9.Industry, Innovation and Infrastructure" },
  { number: 10, title: "10. Reduced Inequalities" },
  { number: 11, title: "11. Sustainable Cities and Communities" },
  { number: 12, title: "12. Responsible Consumption and Production" },
  { number: 13, title: "13. Climate Action" },
  { number: 14, title: "14. Life Below Water" },
  { number: 15, title: "15. Life on Land" },
  { number: 16, title: "16. Peace, Justice and Strong Institutions" },
  { number: 17, title: "17. Partnerships for the Goals" }
];

const searchBox = document.getElementById("location");
const resultsDiv = document.getElementById("results");

searchBox.addEventListener("input", () => {

    const keyword = searchBox.value.toLowerCase().trim();
    resultsDiv.innerHTML = "";
    if(keyword == "")return;

    const filtered = sdgs.filter(item => item.title.toLowerCase().includes(keyword)); 

    filtered.forEach(item =>{
        const div = document.createElement('div');
        div.textContent = `${item.title}`;
        div.className = "result-item";

        div.addEventListener("click", () =>{
            window.location.href = `/sdg/${item.number}`;
            searchBox.value = item.title; 
             resultsDiv.innerHTML = ""; 
        })
         
        resultsDiv.appendChild(div);
    });
    resultsDiv.style.display = filtered.length ? "block" : "none";

});
searchBox.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    const keyword = searchBox.value.toLowerCase().trim();
    if (keyword === "") return;

    const filtered = sdgs.filter(item => item.title.toLowerCase().includes(keyword));
    
    if (filtered.length > 0) {
      
      window.location.href = `/sdg/${filtered[0].number}`;
      searchBox.value = filtered[0].title;
      resultsDiv.innerHTML = "";
    }
  }
});
document.addEventListener("click", (e) => {
  if (!searchBox.contains(e.target) && !resultsDiv.contains(e.target)) {
    resultsDiv.innerHTML = "";
    resultsDiv.style.display = "none";
  }
});
