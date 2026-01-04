// Global variables
let currentSlide = 0;
let slides = [];
let totalSlides = 0;
let slideCounter = null;
let totalSlidesCounter = null;
let autoPlayInterval = null;
let isAutoPlaying = true;
let isMuted = false;
let backgroundMusic = null;
let slideStartTime = Date.now();
let pauseStartTime = 0;
let totalPausedTime = 0;
const loadedSlides = new Set(); // Track which slides have been loaded

function handleFirstInteraction() {
    if (backgroundMusic && !isMuted) {
        backgroundMusic.play().catch(e => {
            console.log('Audio play failed:', e);
        });
    }
}

function initializeAudio() {
    const container = document.querySelector('.slideshow-container');
    const musicUrl = container ? container.getAttribute('data-music') : null;
    
    if (!musicUrl || musicUrl === 'null' || musicUrl === '') {
        return; // No music file provided
    }
    
    try {
        backgroundMusic = new Audio(musicUrl);
        backgroundMusic.loop = true;
        backgroundMusic.volume = 0.3;
        backgroundMusic.preload = 'auto';
        
        // Preload the audio file
        backgroundMusic.load();
        
        // Add event listeners
        backgroundMusic.addEventListener('canplaythrough', () => {
            // Audio loaded and ready
        });
        
        backgroundMusic.addEventListener('error', (e) => {
            console.error('Audio loading error:', backgroundMusic.error);
        });
    } catch (e) {
        console.error('Error creating audio object:', e);
    }
}

// Get language from container
function getLanguage() {
    const container = document.querySelector('.slideshow-container');
    return container ? container.getAttribute('data-lang') || 'en' : 'en';
}

// Initialize everything
function initialize() {
    // Initialize DOM references
    slides = document.querySelectorAll('.slide');
    totalSlides = slides.length;
    slideCounter = document.getElementById('current-slide');
    totalSlidesCounter = document.getElementById('total-slides');
    
    if (totalSlides === 0) {
        console.error('No slides found!');
        return;
    }
    
    initializeAudio();
    updateTotalSlidesCounter();
    setupInitialSlides();
    startAutoPlay();
    
    const lang = getLanguage();
    const playPauseText = document.getElementById('auto-play-text');
    if (playPauseText) {
        playPauseText.textContent = lang === 'fa' ? 'توقف' : 'Pause';
    }
    
    // Initialize mute button text
    const muteText = document.getElementById('mute-text');
    if (muteText && backgroundMusic) {
        muteText.textContent = lang === 'fa' ? 'بی‌صدا' : 'Mute';
    } else if (muteText && !backgroundMusic) {
        muteText.textContent = lang === 'fa' ? 'صدا' : 'Mute';
    }
    
    // Check if user has recently interacted via profile page
    const lastInteraction = sessionStorage.getItem('userInteracted');
    const currentTime = Date.now();
    const thirtySecondsAgo = currentTime - 30000;
    
    // Also check URL parameter as backup
    const urlParams = new URLSearchParams(window.location.search);
    const autoplayParam = urlParams.get('autoplay');
    
    if ((lastInteraction && parseInt(lastInteraction) > thirtySecondsAgo) || autoplayParam === 'true') {
        // User came from profile page recently, start music immediately
        if (backgroundMusic && !isMuted) {
            // Try to start music immediately
            const startMusic = () => {
                backgroundMusic.play().then(() => {
                    // Only clear after music starts successfully
                    sessionStorage.removeItem('userInteracted');
                }).catch(e => {
                    // Try again after a short delay
                    setTimeout(() => {
                        backgroundMusic.play().then(() => {
                            sessionStorage.removeItem('userInteracted');
                        }).catch(e2 => {
                            // Silent fail on retry
                        });
                    }, 1000);
                });
            };
            
            // Start immediately
            startMusic();
        } else {
            sessionStorage.removeItem('userInteracted');
        }
    } else {
        // Wait for first interaction
        document.addEventListener('click', handleFirstInteraction, { once: true });
    }
}

function toggleAutoPlay() {
    isAutoPlaying = !isAutoPlaying;
    const autoPlayText = document.getElementById('auto-play-text');
    const lang = getLanguage();
    
    if (isAutoPlaying) {
        // Resume autoplay
        slideStartTime = Date.now();
        pauseStartTime = 0;
        totalPausedTime = 0;
        startAutoPlay();
        if (autoPlayText) {
            autoPlayText.textContent = lang === 'fa' ? 'توقف' : 'Pause';
        }
    } else {
        // Pause autoplay - use stopAutoPlay to ensure interval is cleared
        stopAutoPlay();
        if (autoPlayText) {
            autoPlayText.textContent = lang === 'fa' ? 'پخش' : 'Play';
        }
    }
}

function updateTotalSlidesCounter() {
    if (totalSlidesCounter) {
        totalSlidesCounter.textContent = totalSlides;
    }
}

function setupInitialSlides() {
    slides.forEach((slide, index) => {
        slide.style.transition = 'transform 0.6s ease-in-out, opacity 0.6s ease-in-out';
        if (index === 0) {
            slide.classList.add('active');
            slide.style.transform = 'translateX(0)';
            // Load first slide immediately
            loadSlideMedia(index);
        } else {
            slide.style.transform = 'translateX(100%)';
        }
    });
    
    if (slideCounter) {
        slideCounter.textContent = '1';
    }
    
    // Preload next slide for smooth transition
    if (totalSlides > 1) {
        preloadSlide(1);
    }
}

// Load media for a specific slide
function loadSlideMedia(index) {
    if (index < 0 || index >= totalSlides || loadedSlides.has(index)) {
        return; // Already loaded or invalid index
    }
    
    const slide = slides[index];
    if (!slide) return;
    
    // Find media element (img or video)
    const img = slide.querySelector('img[data-src]');
    const video = slide.querySelector('video[data-src]');
    
    if (img) {
        const dataSrc = img.getAttribute('data-src');
        if (dataSrc) {
            img.src = dataSrc;
            img.removeAttribute('data-src');
            loadedSlides.add(index);
        }
    }
    
    if (video) {
        const dataSrc = video.getAttribute('data-src');
        if (dataSrc) {
            video.src = dataSrc;
            video.removeAttribute('data-src');
            video.load(); // Load video
            loadedSlides.add(index);
        }
    }
}

// Preload a slide (for smooth transitions)
function preloadSlide(index) {
    if (index < 0 || index >= totalSlides) return;
    loadSlideMedia(index);
}

// Preload adjacent slides for smooth navigation
function preloadAdjacentSlides(currentIndex) {
    // Preload next slide
    const nextIndex = (currentIndex + 1) % totalSlides;
    preloadSlide(nextIndex);
    
    // Preload previous slide
    const prevIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    preloadSlide(prevIndex);
}

function showSlide(index, direction = 'next') {
    const currentActiveSlide = document.querySelector('.slide.active');
    const newSlide = slides[index];
    
    if (currentActiveSlide === newSlide) return;
    
    // Load media for the new slide if not already loaded
    loadSlideMedia(index);
    
    // Prepare new slide position
    newSlide.style.transform = direction === 'next' ? 'translateX(100%)' : 'translateX(-100%)';
    
    // Trigger reflow
    void newSlide.offsetHeight;
    
    // Start transition
    currentActiveSlide?.classList.remove('active');
    currentActiveSlide?.classList.add('transition-out');
    newSlide.classList.add('active');
    
    // Set final positions
    currentActiveSlide && (currentActiveSlide.style.transform = direction === 'next' ? 'translateX(-100%)' : 'translateX(100%)');
    newSlide.style.transform = 'translateX(0)';
    
    // Update counter
    if (slideCounter) {
        slideCounter.textContent = index + 1;
    }
    
    // Preload adjacent slides for smooth future navigation
    preloadAdjacentSlides(index);
    
    // Clean up classes after transition
    setTimeout(() => {
        currentActiveSlide?.classList.remove('transition-out');
    }, 600);
}

const SLIDE_DURATION = 7000; // 7 seconds

function startAutoPlay() {
    stopAutoPlay(); // Clear any existing interval
    
    // Start interval
    autoPlayInterval = setInterval(nextSlide, SLIDE_DURATION);
}

function stopAutoPlay() {
    // Clear the interval and ensure it's null
    if (autoPlayInterval !== null) {
        clearInterval(autoPlayInterval);
        autoPlayInterval = null;
    }
}

function nextSlide() {
    console.log('startProgressBar called');
    // First stop any existing progress bar
    stopProgressBar();
    
    const progressBar = document.querySelector('.progress-bar');
    if (!progressBar) {
        console.log('startProgressBar: Progress bar element not found!');
        return;
    }
    
    // Clear any existing transition timeout from stopProgressBar
    if (stopProgressBar.restoreTransitionTimeout) {
        clearTimeout(stopProgressBar.restoreTransitionTimeout);
        stopProgressBar.restoreTransitionTimeout = null;
    }
    
    // Ensure progress bar starts from 0% - reset transition and width
    progressBar.style.transition = 'none';
    progressBar.style.width = '0%';
    progressBar.style.removeProperty('width');
    progressBar.style.width = '0%';
    // Force a reflow
    void progressBar.offsetWidth;
    
    // Restore transitions for smooth animation
    const computedStyle = window.getComputedStyle(progressBar);
    const transitionFromCSS = computedStyle.transition;
    progressBar.style.transition = transitionFromCSS || 'width 0.1s linear';
    
    // Mark progress bar as active
    progressBarActive = true;
    
    // Reset start time to now
    progressBarStartTime = Date.now();
    console.log('startProgressBar: Progress bar reset to 0%, starting new interval');
    
    // Update progress bar smoothly
    // Create the interval and store the reference immediately
    progressBarInterval = setInterval(() => {
        // Check if progress bar is still active (flag-based check)
        if (!progressBarActive) {
            console.log('startProgressBar: Interval callback detected inactive flag, stopping');
            return;
        }
        
        const elapsed = Date.now() - progressBarStartTime;
        const progress = Math.min(elapsed / SLIDE_DURATION, 1);
        progressBar.style.width = `${progress * 100}%`;
        
        if (progress >= 1) {
            clearInterval(progressBarInterval);
            progressBarInterval = null;
            progressBarActive = false;
        }
    }, 50); // Update every 50ms for smooth animation
    console.log('startProgressBar: New interval created:', progressBarInterval);
}

function nextSlide() {
    // Only advance if autoplay is active
    // This prevents the interval from advancing slides when paused
    if (!isAutoPlaying || !autoPlayInterval) {
        return;
    }
    
    const nextIndex = (currentSlide + 1) % totalSlides;
    showSlide(nextIndex, 'next');
    currentSlide = nextIndex;
    
    // Reset pause tracking
    slideStartTime = Date.now();
    pauseStartTime = 0;
    totalPausedTime = 0;
    
    // The interval will continue calling this function
    // No need to restart autoplay here since the interval is already running
}

function previousSlide() {
    const prevIndex = (currentSlide - 1 + totalSlides) % totalSlides;
    showSlide(prevIndex, 'prev');
    currentSlide = prevIndex;
    
    // Reset pause tracking when manually advancing
    slideStartTime = Date.now();
    pauseStartTime = 0;
    totalPausedTime = 0;
    
    // If autoplay was active but interval is missing, restart it
    if (isAutoPlaying && !autoPlayInterval) {
        startAutoPlay(); // Restart autoplay if it was stopped
    }
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight') {
        nextSlide();
    } else if (e.key === 'ArrowLeft') {
        previousSlide();
    }
});

function goHome(lang) {
    const container = document.querySelector('.slideshow-container');
    if (!container) return;
    const slug = container.getAttribute('slug');
    if (!slug) return;
    // Use unified URL with lang parameter
    window.location.href = `/slideshows/${slug}/?lang=${lang}`;
}

function toggleMute() {
    if (!backgroundMusic) {
        return; // No background music available
    }
    
    isMuted = !isMuted;
    const muteText = document.getElementById('mute-text');
    const lang = getLanguage();
    
    if (isMuted) {
        // Mute: pause the music
        backgroundMusic.pause();
        if (muteText) {
            muteText.textContent = lang === 'fa' ? 'صدا' : 'Unmute';
        }
    } else {
        // Unmute: play the music
        if (muteText) {
            muteText.textContent = lang === 'fa' ? 'بی‌صدا' : 'Mute';
        }
        const playPromise = backgroundMusic.play();
        if (playPromise !== undefined) {
            playPromise.catch(e => {
                console.error('Audio play failed:', e);
                // If play fails, revert to muted state
                isMuted = true;
                if (muteText) {
                    muteText.textContent = lang === 'fa' ? 'صدا' : 'Unmute';
                }
            });
        }
    }
}

function pauseAutoPlay() {
    // Use stopAutoPlay to ensure proper cleanup
    stopAutoPlay();
    
    // Record pause start time
    pauseStartTime = Date.now();
}

// Make functions globally accessible for onclick handlers
window.toggleMute = toggleMute;
window.toggleAutoPlay = toggleAutoPlay;
window.goHome = goHome;
window.nextSlide = nextSlide;
window.previousSlide = previousSlide;

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
} else {
    // DOM is already ready
    initialize();
}