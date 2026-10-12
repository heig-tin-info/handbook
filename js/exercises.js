// Interactive multiple-choice exercises.
//
// Under MkDocs, `mkdocs-plugin-exercises` rewrote the task lists of an
// exercise callout on the server. Zensical runs no MkDocs plugin, so the page
// arrives with the plain task list TMark writes: a `- [x]` is a checked,
// disabled box. This script turns each such list back into a quiz: the
// checked boxes are the expected answers, the student ticks, and the
// exercise says whether it passed as soon as it can tell.
//
//   - every expected answer ticked, nothing wrong  -> pass
//   - one wrong answer ticked                      -> fail, the expected
//                                                     answers are revealed
//
// The `??? solution` of the exercise stays hidden until then, and a button
// starts it over.

(() => {
  const SELECTOR = ".admonition.exercise, details.exercise";

  const setup = (exercise) => {
    if (exercise.dataset.quiz) return;
    const lists = exercise.querySelectorAll(":scope > ul.task-list");
    if (!lists.length) return;
    const inputs = [...exercise.querySelectorAll(
      ":scope > ul.task-list > li > label > input[type=checkbox]")];
    if (!inputs.some((input) => input.checked)) return;

    exercise.dataset.quiz = "pending";
    for (const input of inputs) {
      input.dataset.good = input.checked ? "1" : "0";
      input.checked = false;
      input.disabled = false;
      input.addEventListener("change", () => check(exercise, inputs));
      // The label holds the box only: a click on the answer's text ticks it.
      input.closest("li").addEventListener("click", (event) => {
        if (!input.disabled && !event.target.closest("label, a")) input.click();
      });
    }

    const reset = document.createElement("button");
    reset.type = "button";
    reset.className = "quiz-reset md-button";
    reset.textContent = "Recommencer";
    reset.addEventListener("click", () => {
      for (const input of inputs) {
        input.checked = false;
        input.disabled = false;
        input.closest("li").classList.remove("quiz-good", "quiz-bad", "quiz-missed");
      }
      exercise.dataset.quiz = "pending";
    });
    lists[lists.length - 1].after(reset);
  };

  const check = (exercise, inputs) => {
    const good = inputs.filter((input) => input.dataset.good === "1");
    const wrong = inputs.some((input) => input.checked && input.dataset.good === "0");
    const done = good.every((input) => input.checked);
    if (!wrong && !done) return;

    exercise.dataset.quiz = wrong ? "fail" : "pass";
    for (const input of inputs) {
      const item = input.closest("li");
      const isGood = input.dataset.good === "1";
      input.disabled = true;
      if (input.checked) item.classList.add(isGood ? "quiz-good" : "quiz-bad");
      else if (isGood) item.classList.add("quiz-missed");
    }
  };

  const install = () => document.querySelectorAll(SELECTOR).forEach(setup);

  // Instant navigation swaps the page without a load event.
  if (typeof document$ !== "undefined") document$.subscribe(install);
  else document.addEventListener("DOMContentLoaded", install);
})();
