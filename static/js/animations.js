// ============================================================
// animations.js - Scroll Animations
// ============================================================

document.addEventListener('DOMContentLoaded', function() {

    // ===== PARALLAX ON MOUSE MOVE =====
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;
            
            const orbs = this.querySelectorAll('.orb');
            orbs.forEach((orb, i) => {
                const speed = 20 + i * 10;
                orb.style.transform = 	ranslate(px, px);
            });
        });
    }

    // ===== FLOATING TAGS ANIMATION =====
    const tags = document.querySelectorAll('.floating-tag');
    tags.forEach((tag, i) => {
        tag.style.animationDelay = (i * 0.5) + 's';
    });

    // ===== CARD HOVER EFFECT =====
    const cards = document.querySelectorAll('.glass-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});
