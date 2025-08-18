// Main JavaScript functionality
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Add loading states to buttons
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                
                // Re-enable after 3 seconds (fallback)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 3000);
            }
        });
    });
    
    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add click analytics (if on profile page)
    const linkCards = document.querySelectorAll('.link-card');
    linkCards.forEach(card => {
        card.addEventListener('click', function() {
            // Add visual feedback
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
    
    // Enhanced form validation
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.style.borderColor = 'var(--danger)';
            } else {
                this.style.borderColor = 'var(--border-color)';
            }
        });
        
        input.addEventListener('input', function() {
            if (this.style.borderColor === 'var(--danger)' && this.value.trim()) {
                this.style.borderColor = 'var(--border-color)';
            }
        });
    });
    
    // Copy link functionality (if on profile page)
    const profileUrl = window.location.href;
    if (profileUrl.includes('/') && !profileUrl.includes('/edit')) {
        // Add copy button to profile
        const profileHeader = document.querySelector('.profile-header');
        if (profileHeader) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'btn btn-sm';
            copyBtn.style.position = 'absolute';
            copyBtn.style.top = '20px';
            copyBtn.style.right = '20px';
            copyBtn.style.background = 'rgba(255,255,255,0.2)';
            copyBtn.style.color = 'white';
            copyBtn.style.border = '1px solid rgba(255,255,255,0.3)';
            copyBtn.innerHTML = '<i class="fas fa-share"></i>';
            copyBtn.title = 'Copy profile link';
            
            copyBtn.addEventListener('click', function() {
                navigator.clipboard.writeText(profileUrl).then(() => {
                    this.innerHTML = '<i class="fas fa-check"></i>';
                    setTimeout(() => {
                        this.innerHTML = '<i class="fas fa-share"></i>';
                    }, 2000);
                });
            });
            
            profileHeader.appendChild(copyBtn);
        }
    }
    
    // Add hover effects for link cards
    const profileLinkCards = document.querySelectorAll('.link-card');
    profileLinkCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // Enhanced emoji selector
    const emojiSelect = document.querySelector('.emoji-select');
    if (emojiSelect) {
        emojiSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            this.style.background = `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`;
            this.style.color = 'white';
        });
    }
    
    // Add animation to feature cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    const animatedElements = document.querySelectorAll('.feature-card, .profile-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `message message-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        ${message}
        <button class="message-close" onclick="this.parentElement.remove()">×</button>
    `;
    
    let container = document.querySelector('.messages-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'messages-container';
        document.body.appendChild(container);
    }
    
    container.appendChild(notification);
    
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 5000);
}

// Analytics helper
function trackEvent(eventName, properties = {}) {
    console.log('Event tracked:', eventName, properties);
    // In a real app, you would send this to your analytics service
}