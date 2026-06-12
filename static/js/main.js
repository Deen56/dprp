document.addEventListener('DOMContentLoaded', function () {
    const radios = document.querySelectorAll('.answer-radio');
    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const progressPercent = document.getElementById('progress-percent');
    const totalQuestions = 15;

    function updateProgress() {
        // Count how many questions have been answered
        const answered = new Set();
        radios.forEach(radio => {
            if (radio.checked) {
                answered.add(radio.name);
            }
        });

        const count = answered.size;
        const percent = Math.round((count / totalQuestions) * 100);

        // Update progress bar
        progressBar.style.width = percent + '%';
        progressText.textContent = count + ' of ' + totalQuestions + ' answered';
        progressPercent.textContent = percent + '%';

        // Change color as progress increases
        if (percent < 40) {
            progressBar.style.backgroundColor = '#00d4ff';
        } else if (percent < 80) {
            progressBar.style.backgroundColor = '#ffc107';
        } else {
            progressBar.style.backgroundColor = '#28a745';
        }

        // Highlight answered question cards
        radios.forEach(radio => {
            if (radio.checked) {
                const card = document.getElementById('qcard-' + radio.name);
                if (card) card.classList.add('answered');
            }
        });
    }

    // Listen for any radio button change
    radios.forEach(radio => {
        radio.addEventListener('change', updateProgress);
    });

    // Validate all questions answered before submit
    const form = document.getElementById('assessment-form');
    const warning = document.getElementById('submit-warning');

    form.addEventListener('submit', function (e) {
        const answered = new Set();
        radios.forEach(radio => {
            if (radio.checked) answered.add(radio.name);
        });

        if (answered.size < totalQuestions) {
            e.preventDefault();
            warning.style.display = 'block';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });
});