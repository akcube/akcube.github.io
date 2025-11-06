/**
 * Image Handler JavaScript
 * Handles carousel navigation, lightbox, and lazy loading
 * Optimized for performance and accessibility
 */

(function() {
  'use strict';

  // ============================================
  // 1. Lightbox Functionality
  // ============================================

  function initLightbox() {
    // Create lightbox element if it doesn't exist
    let lightbox = document.getElementById('lightbox');
    if (!lightbox) {
      lightbox = document.createElement('div');
      lightbox.id = 'lightbox';
      lightbox.className = 'lightbox';
      lightbox.setAttribute('role', 'dialog');
      lightbox.setAttribute('aria-label', 'Image lightbox');
      lightbox.innerHTML = `
        <button class="lightbox-close" aria-label="Close lightbox">×</button>
        <img src="" alt="" />
      `;
      document.body.appendChild(lightbox);
    }

    const lightboxImg = lightbox.querySelector('img');
    const closeBtn = lightbox.querySelector('.lightbox-close');

    // Add click handlers to all zoomable images
    document.addEventListener('click', function(e) {
      const img = e.target.closest('.zoomable, .content-image');
      if (img && img.tagName === 'IMG') {
        e.preventDefault();
        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });

    // Close lightbox handlers
    function closeLightbox() {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function(e) {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });

    // Keyboard support
    document.addEventListener('keydown', function(e) {
      if (lightbox.classList.contains('active') && e.key === 'Escape') {
        closeLightbox();
      }
    });
  }

  // ============================================
  // 2. Lazy Loading Enhancement
  // ============================================

  function enhanceLazyLoading() {
    // Add 'loaded' class when images finish loading
    const lazyImages = document.querySelectorAll('img[loading="lazy"]');

    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.addEventListener('load', () => {
              img.classList.add('loaded');
            });
            if (img.complete) {
              img.classList.add('loaded');
            }
            observer.unobserve(img);
          }
        });
      });

      lazyImages.forEach(img => imageObserver.observe(img));
    } else {
      // Fallback for browsers without IntersectionObserver
      lazyImages.forEach(img => {
        img.addEventListener('load', () => {
          img.classList.add('loaded');
        });
        if (img.complete) {
          img.classList.add('loaded');
        }
      });
    }
  }

  // ============================================
  // 3. Carousel Functionality
  // ============================================

  const carousels = new Map();

  function initCarousel(carouselId) {
    const carousel = document.getElementById(carouselId);
    if (!carousel || carousels.has(carouselId)) return;

    const slidesContainer = carousel.querySelector('.carousel-slides');
    const prevBtn = carousel.querySelector('.carousel-prev');
    const nextBtn = carousel.querySelector('.carousel-next');
    const indicatorsContainer = carousel.querySelector('.carousel-indicators');
    const counterCurrent = carousel.querySelector('.current-slide');
    const counterTotal = carousel.querySelector('.total-slides');

    // Convert image-wrapper figures to carousel slides
    const figures = slidesContainer.querySelectorAll('.image-wrapper');
    if (figures.length === 0) return;

    // Wrap each figure in a carousel-slide div
    figures.forEach((figure, index) => {
      const slide = document.createElement('div');
      slide.className = 'carousel-slide';
      slide.setAttribute('role', 'tabpanel');
      slide.setAttribute('aria-label', `Slide ${index + 1} of ${figures.length}`);
      figure.parentNode.insertBefore(slide, figure);
      slide.appendChild(figure);
    });

    const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
    const totalSlides = slides.length;

    if (totalSlides === 0) return;

    // Initialize state
    let currentIndex = 0;
    let autoplayInterval = null;
    const autoplay = carousel.dataset.autoplay === 'true';
    const interval = parseInt(carousel.dataset.interval) || 5000;

    // Update counter
    if (counterTotal) counterTotal.textContent = totalSlides;
    if (counterCurrent) counterCurrent.textContent = '1';

    // Create indicators
    if (indicatorsContainer) {
      for (let i = 0; i < totalSlides; i++) {
        const indicator = document.createElement('button');
        indicator.className = 'carousel-indicator';
        indicator.setAttribute('role', 'tab');
        indicator.setAttribute('aria-label', `Go to slide ${i + 1}`);
        indicator.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
        if (i === 0) indicator.classList.add('active');
        indicator.addEventListener('click', () => goToSlide(i));
        indicatorsContainer.appendChild(indicator);
      }
    }

    // Navigation functions
    function updateCarousel(animate = true) {
      const offset = -currentIndex * 100;
      if (!animate || window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        slidesContainer.style.transition = 'none';
      } else {
        slidesContainer.style.transition = 'transform 0.5s ease-in-out';
      }
      slidesContainer.style.transform = `translateX(${offset}%)`;

      // Update indicators
      if (indicatorsContainer) {
        const indicators = indicatorsContainer.querySelectorAll('.carousel-indicator');
        indicators.forEach((indicator, index) => {
          const isActive = index === currentIndex;
          indicator.classList.toggle('active', isActive);
          indicator.setAttribute('aria-selected', isActive ? 'true' : 'false');
        });
      }

      // Update counter
      if (counterCurrent) {
        counterCurrent.textContent = (currentIndex + 1).toString();
      }

      // Update ARIA live region
      const liveRegion = carousel.querySelector('.carousel-counter');
      if (liveRegion) {
        liveRegion.setAttribute('aria-live', 'polite');
      }
    }

    function goToSlide(index) {
      currentIndex = (index + totalSlides) % totalSlides;
      updateCarousel();
      resetAutoplay();
    }

    function nextSlide() {
      goToSlide(currentIndex + 1);
    }

    function prevSlide() {
      goToSlide(currentIndex - 1);
    }

    function startAutoplay() {
      if (autoplay && !autoplayInterval) {
        autoplayInterval = setInterval(nextSlide, interval);
      }
    }

    function stopAutoplay() {
      if (autoplayInterval) {
        clearInterval(autoplayInterval);
        autoplayInterval = null;
      }
    }

    function resetAutoplay() {
      stopAutoplay();
      startAutoplay();
    }

    // Event listeners
    if (prevBtn) prevBtn.addEventListener('click', prevSlide);
    if (nextBtn) nextBtn.addEventListener('click', nextSlide);

    // Hide nav buttons if only one slide
    if (totalSlides <= 1) {
      if (prevBtn) prevBtn.style.display = 'none';
      if (nextBtn) nextBtn.style.display = 'none';
      if (indicatorsContainer) indicatorsContainer.style.display = 'none';
    }

    // Keyboard navigation
    carousel.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        nextSlide();
      }
    });

    // Touch/swipe support
    let touchStartX = 0;
    let touchEndX = 0;

    carousel.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    carousel.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    }, { passive: true });

    function handleSwipe() {
      const swipeThreshold = 50;
      const diff = touchStartX - touchEndX;

      if (Math.abs(diff) > swipeThreshold) {
        if (diff > 0) {
          nextSlide();
        } else {
          prevSlide();
        }
      }
    }

    // Pause autoplay on hover/focus
    carousel.addEventListener('mouseenter', stopAutoplay);
    carousel.addEventListener('mouseleave', startAutoplay);
    carousel.addEventListener('focusin', stopAutoplay);
    carousel.addEventListener('focusout', startAutoplay);

    // Start autoplay if enabled
    startAutoplay();

    // Initial update
    updateCarousel(false);

    // Store carousel instance
    carousels.set(carouselId, {
      element: carousel,
      goToSlide,
      nextSlide,
      prevSlide,
      startAutoplay,
      stopAutoplay
    });
  }

  // ============================================
  // 4. Initialize All Carousels
  // ============================================

  function initAllCarousels() {
    const carouselElements = document.querySelectorAll('.image-carousel');
    carouselElements.forEach(carousel => {
      initCarousel(carousel.id);
    });
  }

  // ============================================
  // 5. Expose to Global Scope
  // ============================================

  window.initCarousel = initCarousel;
  window.getCarousel = (id) => carousels.get(id);

  // ============================================
  // 6. Initialize on DOM Ready
  // ============================================

  function init() {
    initLightbox();
    enhanceLazyLoading();
    initAllCarousels();
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
