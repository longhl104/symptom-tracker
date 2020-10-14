const allRanges = document.querySelectorAll(".range-wrap");
allRanges.forEach(wrap => {
  const range = wrap.querySelector(".range");
  const bubble = wrap.querySelector(".bubble");

  range.addEventListener("input", () => {
    setBubble(range, bubble);
  });
  setBubble(range, bubble);
});

function setBubble(range, bubble) {
  const val = range.value;
  const min = range.min ? range.min : 0;
  const max = range.max ? range.max : 100;
  const newVal = Number(((val - min) * 100) / (max - min));
  const severity = val == 0 ? "Not at all" : val == 1 ? "A little bit" : val == 2 ? "Somewhat" : val == 3 ? "Quite a bit" : "Very much"
  bubble.innerText = severity;

  const translateX = val == 0 ? '-10%' : val == 4 ? '-90%' : '-50%';

  // Shift the bubble to the left based on the current value of the range
  bubble.style.left = `calc(${newVal}% + (${8 - newVal * 0.15}px))`;
  bubble.style.transform = `translateX(${translateX})`;
}