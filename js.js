/* =====================================================
   🚀 NEXSKOOL MARKDOWN SYSTEM - JAVASCRIPT GLOBAL
   Version complète pour fiches auteurs français
   ===================================================== */

document.addEventListener('DOMContentLoaded', function() {
    console.log('🎨 NexSkool System - Démarrage...');

    // =====================================================
    // 🎯 NAVIGATION ET SCROLL SMOOTH
    // =====================================================

    // Smooth scroll pour les liens d'ancrage
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });

                    // Ajouter classe active au lien cliqué
                    document.querySelectorAll('.sommaire a').forEach(link => {
                        link.classList.remove('active');
                    });
                    this.classList.add('active');
                }
            });
        });
        console.log('✅ Smooth scroll initialisé');
    }

    // Détection de la section visible pour navigation active
    function initActiveNavigation() {
        const sections = document.querySelectorAll('.section-block[id]');
        const navLinks = document.querySelectorAll('.sommaire a[href^="#"]');

        if (sections.length === 0 || navLinks.length === 0) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');

                    // Retirer active de tous les liens
                    navLinks.forEach(link => link.classList.remove('active'));

                    // Ajouter active au lien correspondant
                    const activeLink = document.querySelector(`.sommaire a[href="#${id}"]`);
                    if (activeLink) {
                        activeLink.classList.add('active');
                    }
                }
            });
        }, {
            threshold: 0.3,
            rootMargin: '-100px 0px -50% 0px'
        });

        sections.forEach(section => observer.observe(section));
        console.log('✅ Navigation active initialisée');
    }

    // =====================================================
    // 🎪 ANIMATIONS AU SCROLL
    // =====================================================

    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    entry.target.classList.add('animated');
                }
            });
        }, observerOptions);

        // Observer tous les éléments avec animation
        const animatedElements = document.querySelectorAll(`
            .section-block,
            .stat-card,
            .timeline-item,
            .anecdote-bloc,
            .citation,
            .citation-center,
            .alert,
            .note,
            .success-box,
            .warning-box,
            .info-box,
            .error-box,
            .NexSchool
        `);

        animatedElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });

        console.log(`✅ ${animatedElements.length} éléments observés pour animations`);
    }

    // =====================================================
    // 📊 ANIMATION DES PROGRESS BARS
    // =====================================================

    function initProgressBars() {
        const progressBars = document.querySelectorAll('.progress-fill');

        if (progressBars.length === 0) return;

        const progressObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const progressFill = entry.target;
                    const targetWidth = progressFill.style.width || '0%';

                    // Animation de la barre
                    progressFill.style.width = '0%';
                    setTimeout(() => {
                        progressFill.style.width = targetWidth;
                    }, 200);

                    // Ne plus observer cet élément
                    progressObserver.unobserve(progressFill);
                }
            });
        }, { threshold: 0.5 });

        progressBars.forEach(bar => {
            progressObserver.observe(bar);
        });

        console.log(`✅ ${progressBars.length} barres de progression initialisées`);
    }

    // =====================================================
    // 🎭 EFFETS HOVER AVANCÉS
    // =====================================================

    function initHoverEffects() {
        // Effet de particle au survol des badges
        document.querySelectorAll('.emoji-badge').forEach(badge => {
            badge.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-3px) scale(1.1)';
            });

            badge.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Effet de hover sur les cartes
        document.querySelectorAll('.stat-card, .timeline-item').forEach(card => {
            card.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            });

            card.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0) scale(1)';
            });
        });

        // Effet sur les sections
        document.querySelectorAll('.section-block').forEach(section => {
            section.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });

            section.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });

        console.log('✅ Effets hover initialisés');
    }

    // =====================================================
    // 🎨 GESTION DES DÉTAILS/SUMMARY
    // =====================================================

    function initDetailsToggle() {
        const details = document.querySelectorAll('.section-block');

        details.forEach(detail => {
            const summary = detail.querySelector('summary');
            if (!summary) return;

            // Forcer la fermeture au début
            detail.removeAttribute('open');

            summary.addEventListener('click', function(e) {
                e.preventDefault();

                const isOpen = detail.hasAttribute('open');

                if (isOpen) {
                    // Fermer avec animation
                    const content = detail.querySelector('.contenu-section');
                    if (content) {
                        content.style.maxHeight = content.scrollHeight + 'px';
                        content.style.opacity = '1';

                        requestAnimationFrame(() => {
                            content.style.maxHeight = '0';
                            content.style.opacity = '0';
                        });

                        setTimeout(() => {
                            detail.removeAttribute('open');
                        }, 300);
                    }
                } else {
                    // Ouvrir avec animation
                    detail.setAttribute('open', '');
                    const content = detail.querySelector('.contenu-section');
                    if (content) {
                        content.style.maxHeight = '0';
                        content.style.opacity = '0';

                        requestAnimationFrame(() => {
                            content.style.maxHeight = content.scrollHeight + 'px';
                            content.style.opacity = '1';
                        });

                        setTimeout(() => {
                            content.style.maxHeight = 'none';
                        }, 300);
                    }
                }
            });
        });

        console.log(`✅ ${details.length} sections détails initialisées`);
    }

    // =====================================================
    // 📱 GESTION RESPONSIVE
    // =====================================================

    function initResponsive() {
        function handleResize() {
            const isMobile = window.innerWidth <= 768;

            // Ajuster la navigation mobile
            const sommaire = document.querySelector('.sommaire');
            if (sommaire) {
                if (isMobile) {
                    sommaire.classList.add('mobile-nav');
                } else {
                    sommaire.classList.remove('mobile-nav');
                }
            }

            // Réajuster les progress bars
            document.querySelectorAll('.progress-fill').forEach(bar => {
                const width = bar.style.width;
                bar.style.transition = 'none';
                bar.style.width = width;
                setTimeout(() => {
                    bar.style.transition = 'width 1s ease';
                }, 10);
            });
        }

        window.addEventListener('resize', handleResize);
        handleResize(); // Appel initial

        console.log('✅ Gestion responsive initialisée');
    }

    // =====================================================
    // 🎯 EASTER EGGS ET INTERACTIONS SPÉCIALES
    // =====================================================

    function initEasterEggs() {
        // Double-clic sur le titre pour animation spéciale
        const title = document.querySelector('h1');
        if (title) {
            title.addEventListener('dblclick', function() {
                this.style.animation = 'none';
                setTimeout(() => {
                    this.style.animation = 'gradientShift 1s ease-in-out, bounce 0.6s ease-in-out';
                }, 10);

                // Effet confetti
                createConfetti();
            });
        }

        // Konami Code (↑↑↓↓←→←→BA)
        let konamiCode = [];
        const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
                               'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'KeyB', 'KeyA'];

        document.addEventListener('keydown', function(e) {
            konamiCode.push(e.code);
            if (konamiCode.length > konamiSequence.length) {
                konamiCode.shift();
            }

            if (konamiCode.join(',') === konamiSequence.join(',')) {
                activatePartyMode();
                konamiCode = [];
            }
        });

        console.log('✅ Easter eggs activés (essayez de double-cliquer sur le titre !)');
    }

    function createConfetti() {
        const colors = ['#fc8f56', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0'];

        for (let i = 0; i < 50; i++) {
            const confetti = document.createElement('div');
            confetti.innerHTML = ['🎉', '✨', '🎊', '⭐', '🌟'][Math.floor(Math.random() * 5)];
            confetti.style.position = 'fixed';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.top = '-10px';
            confetti.style.fontSize = '20px';
            confetti.style.zIndex = '9999';
            confetti.style.pointerEvents = 'none';
            confetti.style.animation = `fall ${2 + Math.random() * 3}s linear forwards`;

            document.body.appendChild(confetti);

            setTimeout(() => {
                if (confetti.parentNode) {
                    confetti.parentNode.removeChild(confetti);
                }
            }, 5000);
        }
    }

    function activatePartyMode() {
        document.body.style.filter = 'hue-rotate(0deg)';
        let hue = 0;

        const partyInterval = setInterval(() => {
            hue += 10;
            document.body.style.filter = `hue-rotate(${hue}deg)`;

            if (hue >= 360) {
                document.body.style.filter = 'none';
                clearInterval(partyInterval);
            }
        }, 100);

        createConfetti();
        console.log('🎊 PARTY MODE ACTIVATED! 🎊');
    }

    // =====================================================
    // 🔧 UTILITAIRES
    // =====================================================

    function addUtilityCSS() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fall {
                from {
                    transform: translateY(-100vh) rotate(0deg);
                    opacity: 1;
                }
                to {
                    transform: translateY(100vh) rotate(360deg);
                    opacity: 0;
                }
            }

            .mobile-nav {
                flex-direction: column;
                gap: 0.5rem;
            }

            .mobile-nav a {
                text-align: center;
                width: 100%;
            }

            .animated {
                /* Classe ajoutée après animation */
            }
        `;
        document.head.appendChild(style);
    }

    // =====================================================
    // 🚀 INITIALISATION PRINCIPALE
    // =====================================================

    function init() {
        console.log('🎨 Initialisation du système NexSkool...');

        // Ajouter CSS utilitaires
        addUtilityCSS();

        // Initialiser tous les modules
        initSmoothScroll();
        initActiveNavigation();
        initScrollAnimations();
        initProgressBars();
        initHoverEffects();
        initDetailsToggle();
        initResponsive();
        initEasterEggs();

        // Ouvrir automatiquement la première section après un délai
        setTimeout(() => {
            const firstSection = document.querySelector('.section-block[id="presentation"]');
            if (firstSection) {
                const summary = firstSection.querySelector('summary');
                if (summary) {
                    summary.click();
                }
            }
        }, 1000);

        console.log('🎉 NexSkool System entièrement chargé !');
        console.log('💡 Astuce : Double-cliquez sur le titre pour une surprise !');
    }

    // Lancer l'initialisation
    init();
});

// =====================================================
// 🌟 FONCTIONS GLOBALES EXPORTÉES
// =====================================================

window.NexSkool = {
    // Fonction pour créer des confettis à la demande
    confetti: function() {
        const colors = ['#fc8f56', '#4CAF50', '#2196F3', '#FF9800', '#9C27B0'];

        for (let i = 0; i < 30; i++) {
            const confetti = document.createElement('div');
            confetti.innerHTML = ['🎉', '✨', '🎊', '⭐', '🌟'][Math.floor(Math.random() * 5)];
            confetti.style.position = 'fixed';
            confetti.style.left = Math.random() * 100 + 'vw';
            confetti.style.top = '-10px';
            confetti.style.fontSize = '20px';
            confetti.style.zIndex = '9999';
            confetti.style.pointerEvents = 'none';
            confetti.style.animation = `fall ${2 + Math.random() * 3}s linear forwards`;

            document.body.appendChild(confetti);

            setTimeout(() => {
                if (confetti.parentNode) {
                    confetti.parentNode.removeChild(confetti);
                }
            }, 5000);
        }
    },

    // Fonction pour animer une progress bar
    animateProgress: function(selector, targetPercent) {
        const progressFill = document.querySelector(selector);
        if (progressFill) {
            progressFill.style.width = '0%';
            setTimeout(() => {
                progressFill.style.width = targetPercent + '%';
            }, 100);
        }
    },

    // Fonction pour scroller vers une section
    scrollTo: function(sectionId) {
        const target = document.getElementById(sectionId);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
};
