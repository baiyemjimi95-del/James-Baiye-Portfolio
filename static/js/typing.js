// ============================================================
// typing.js - Premium Typing Animation
// ============================================================

document.addEventListener('DOMContentLoaded', function() {
    const typingElement = document.querySelector('.typing-text');
    if (!typingElement) return;

    const phrases = [
        'Software Engineer',
        'Data Scientist',
        'Machine Learning Developer',
        'Python & SQL Specialist',
        'Problem Solver',
        'Political Scientist',
        'Building Ideas Into Reality'
    ];

    let phraseIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let currentText = '';

    function type() {
        const currentPhrase = phrases[phraseIndex];
        
        if (isDeleting) {
            currentText = currentPhrase.substring(0, charIndex - 1);
            charIndex--;
        } else {
            currentText = currentPhrase.substring(0, charIndex + 1);
            charIndex++;
        }

        typingElement.textContent = currentText;

        if (!isDeleting && charIndex === currentPhrase.length) {
            isDeleting = true;
            setTimeout(type, 2500);
            return;
        }

        if (isDeleting && charIndex === 0) {
            isDeleting = false;
            phraseIndex = (phraseIndex + 1) % phrases.length;
            setTimeout(type, 500);
            return;
        }

        const speed = isDeleting ? 50 : 100;
        setTimeout(type, speed);
    }

    type();
});
