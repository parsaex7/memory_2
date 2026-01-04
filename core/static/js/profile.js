function startSlideshow(lang, slug) {
    // Set a timestamp to indicate user has recently interacted
    const timestamp = Date.now().toString();
    sessionStorage.setItem('userInteracted', timestamp);
    
    // Get the main content container
    const content = document.querySelector('.memorial-container') || document.body;
    
    // Add fade-out transition
    content.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    content.style.opacity = '0';
    content.style.transform = 'translateY(-20px)';
    
    // Redirect after fade completes - use unified URL with lang parameter
    setTimeout(() => {
        window.location.href = `/slideshows/${slug}/show/?lang=${lang}&autoplay=true`;
    }, 500);
}

function switchLanguage(lang, slug) {
    // Update active language button
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    // Redirect to the same page in selected language using unified URL
    window.location.href = `/slideshows/${slug}/?lang=${lang}`;
}

// Function to update the photo (utility function)
function updatePhoto(imageUrl) {
    const photoFrame = document.querySelector('.photo-frame');
    if (photoFrame) {
        photoFrame.innerHTML = `<img src="${imageUrl}" alt="Memorial photo">`;
    }
}

// Function to update person details (utility function)
function updatePersonDetails(name, birthDate, deathDate) {
    const nameEl = document.querySelector('.person-name');
    const datesEl = document.querySelector('.life-dates');
    const birthDeathEl = document.querySelector('.birth-death');
    
    if (nameEl) nameEl.textContent = name;
    if (datesEl) datesEl.textContent = `${birthDate.split(' ')[2]} - ${deathDate.split(' ')[2]}`;
    if (birthDeathEl) birthDeathEl.innerHTML = `Born: ${birthDate}<br>Passed: ${deathDate}`;
}