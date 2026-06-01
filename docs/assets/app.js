// Day 30. Portfolio front-end. Tag filter only.
const $ = (sel, root = document) => root.querySelector(sel);
const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

function activateFilter(tag) {
  $$(".filter-chip").forEach(c => c.classList.toggle("active",
    c.dataset.filter === tag));
  const cards = $$(".card[data-tags]");
  for (const card of cards) {
    const tags = (card.dataset.tags || "").split(",").map(s => s.trim());
    const show = tag === "all" || tags.includes(tag);
    card.style.display = show ? "" : "none";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  $$(".filter-chip[data-filter]").forEach(c => {
    c.addEventListener("click", () => activateFilter(c.dataset.filter));
  });
});
