const toggleVisibility = (element, displayStyle) => {
    if (element) element.style.display = displayStyle;
};

const resetExercise = (exercise) => {
    exercise.querySelectorAll('input[type="checkbox"], input[type="text"]').forEach(input => {
        input.checked = false;
        input.disabled = false;
        input.value = '';
    });
    exercise.querySelectorAll('input[type="text"]').forEach(input => {
        input.classList.remove('good', 'bad');
    });
    exercise.classList.remove('pass', 'fail');
    toggleVisibility(exercise.querySelector('.solution'), 'none');
    toggleVisibility(exercise.querySelector('.hint'), 'block');
    toggleVisibility(exercise.querySelector('button.exercise-submit'), 'inline');
};

const validateExercise = (exercise, ul, status) => {
    exercise.classList.add(status ? 'pass' : 'fail');
    if (!status) {
        ul.querySelectorAll('input.good').forEach(checkbox => checkbox.checked = true);
    }
    const solution = exercise.querySelector('.solution');
    ul.querySelectorAll('input[type="checkbox"]').forEach(checkbox => checkbox.disabled = true);
    if (solution) solution.style.display = 'block';
    hints = exercise.querySelectorAll('.hint');
    hints.forEach(hint => hint.style.display = 'none');
};

const handleCheckboxChange = (exercise, event, ul) => {
    if (!event.target.matches('input[type="checkbox"]')) return;

    const isGood = event.target.classList.contains('good');
    const allGoodCheckboxes = ul.querySelectorAll('input.good');
    const allGoodCheckboxesChecked = ul.querySelectorAll('input.good:checked');

    if (allGoodCheckboxes.length === allGoodCheckboxesChecked.length) {
        validateExercise(exercise, ul, true);
    }
    if (event.target.checked && !isGood) {
        validateExercise(exercise, ul, false);
    }
};

const parseRegexString = (input) => {
    const delimiter = input[0];

    const sentinel = '§§§';
    input = input.replace(RegExp(`\\\\${delimiter}`, 'g'), sentinel);
    let parts = input.split(delimiter);
    parts = parts.map(part => part.replaceAll(sentinel, `\\${delimiter}`));

    const pattern = parts[1];
    const flags = parts.slice(3).join(delimiter);

    return {regex: RegExp(pattern, flags), replacement: parts[2]};
}

const validateAnswer = (value, answer) => {
    let isValid = false;
    if (answer.startsWith('/')) {
        const {regex, replacement} = parseRegexString(answer);
        isValid = regex.test(value);
    } else {
        isValid = value.trim().toLowerCase() === answer.toLowerCase();
    }
    return isValid;
};

const handleTextInput = (input) => {
    const answer = input.getAttribute('answer') || input.dataset.solution;
    input.classList.toggle('good', validateAnswer(input.value, answer));
    input.classList.remove('bad');
};

const handleSubmit = (exercise) => {
    const allInputs = exercise.querySelectorAll('input[type="text"]');
    const allGoodInputs = exercise.querySelectorAll('input.good');

    if (allInputs.length === allGoodInputs.length) {
        exercise.classList.add('pass');
    } else {
        exercise.classList.add('fail');
    }

    allInputs.forEach(input => {
        input.disabled = true;
        const answer = input.getAttribute('answer') || input.dataset.solution;
        if (!input.value) {
            if (answer.startsWith('/')) {
                const {replacement} = parseRegexString(answer);
                input.value = replacement;
            } else {
                input.value = answer;
            }
        }
        input.classList.toggle('bad', !validateAnswer(input.value, answer));
    });

    toggleVisibility(exercise.querySelector('.solution'), 'block');
    toggleVisibility(exercise.querySelector('.hint'), 'none');
    toggleVisibility(exercise.querySelector('button.exercise-submit'), 'none');
};

const installHandler = () => {
    document.querySelectorAll('.exercise').forEach(exercise => {
        const title = exercise.querySelector('.exercise-title')
        if (title) {
            title.addEventListener('click', () => resetExercise(exercise));
        }
    });

    document.querySelectorAll('.exercise.checkbox').forEach(exercise => {
        exercise.querySelectorAll('.exercise-list').forEach(ul => ul.addEventListener('change', event => handleCheckboxChange(exercise, event, ul)));
    });

    document.querySelectorAll('.exercise.fill-in-the-blank').forEach(exercise => {
        exercise.querySelectorAll('.text-with-gap').forEach(input =>
            input.addEventListener('input', () => handleTextInput(input)));
        exercise.querySelector('button.exercise-submit').addEventListener('click', () => handleSubmit(exercise));
    });
};

// Support for instant feature (navigation.instant)
if (typeof document$ !== 'undefined')
    document$.subscribe(installHandler);
else
    document.addEventListener("DOMContentLoaded", installHandler);