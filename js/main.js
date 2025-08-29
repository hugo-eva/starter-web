// Modern Web Solutions - Main JavaScript
$(document).ready(function() {
    
    // Animated counter for statistics
    function animateCounter(element, target) {
        let current = 0;
        const increment = target / 100;
        const timer = setInterval(function() {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.text(Math.floor(current));
        }, 20);
    }
    
    // Trigger counter animation when stats section is visible
    function checkStatsVisibility() {
        const statsSection = $('.stats-section');
        const sectionTop = statsSection.offset().top;
        const sectionHeight = statsSection.height();
        const windowTop = $(window).scrollTop();
        const windowHeight = $(window).height();
        
        if (windowTop + windowHeight > sectionTop && windowTop < sectionTop + sectionHeight) {
            $('.stat-number').each(function() {
                const $this = $(this);
                const target = parseInt($this.data('count'));
                if (!$this.hasClass('animated')) {
                    $this.addClass('animated');
                    animateCounter($this, target);
                }
            });
        }
    }
    
    // Smooth scrolling for navigation links
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        const target = $(this.getAttribute('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 800);
        }
    });
    
    // Active navigation highlighting
    $(window).on('scroll', function() {
        const scrollTop = $(window).scrollTop();
        
        $('section, .jumbotron').each(function() {
            const $this = $(this);
            const sectionTop = $this.offset().top - 100;
            const sectionHeight = $this.height();
            
            if (scrollTop >= sectionTop && scrollTop < sectionTop + sectionHeight) {
                const id = $this.attr('id');
                $('.navbar-nav li').removeClass('active');
                $(`.navbar-nav a[href="#${id}"]`).parent().addClass('active');
            }
        });
        
        checkStatsVisibility();
    });
    
    // Navbar background on scroll
    $(window).on('scroll', function() {
        if ($(window).scrollTop() > 50) {
            $('.navbar-inverse').addClass('scrolled');
        } else {
            $('.navbar-inverse').removeClass('scrolled');
        }
    });
    
    // Form validation and submission
    $('.navbar-form').on('submit', function(e) {
        e.preventDefault();
        
        const email = $(this).find('input[type="email"]').val();
        const password = $(this).find('input[type="password"]').val();
        
        if (!email || !password) {
            showNotification('Please fill in all fields', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showNotification('Please enter a valid email address', 'error');
            return;
        }
        
        // Simulate form submission
        const submitBtn = $(this).find('button[type="submit"]');
        const originalText = submitBtn.text();
        
        submitBtn.prop('disabled', true).text('Signing in...');
        
        setTimeout(function() {
            submitBtn.prop('disabled', false).text(originalText);
            showNotification('Welcome! You have successfully signed in.', 'success');
            $('.navbar-form')[0].reset();
        }, 2000);
    });
    
    // Email validation function
    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
    
    // Notification system
    function showNotification(message, type) {
        const notification = $(`
            <div class="notification notification-${type}">
                <div class="notification-content">
                    <span class="notification-message">${message}</span>
                    <button class="notification-close">&times;</button>
                </div>
            </div>
        `);
        
        $('body').append(notification);
        
        setTimeout(function() {
            notification.addClass('show');
        }, 100);
        
        notification.find('.notification-close').on('click', function() {
            hideNotification(notification);
        });
        
        setTimeout(function() {
            hideNotification(notification);
        }, 5000);
    }
    
    function hideNotification(notification) {
        notification.removeClass('show');
        setTimeout(function() {
            notification.remove();
        }, 300);
    }
    
    // Service card hover effects
    $('.service-card').on('mouseenter', function() {
        $(this).find('.service-icon').addClass('pulse');
    }).on('mouseleave', function() {
        $(this).find('.service-icon').removeClass('pulse');
    });
    
    // Add CSS for notifications
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                padding: 1rem;
                z-index: 9999;
                transform: translateX(100%);
                transition: transform 0.3s ease;
                max-width: 300px;
            }
            
            .notification.show {
                transform: translateX(0);
            }
            
            .notification-success {
                border-left: 4px solid #28a745;
            }
            
            .notification-error {
                border-left: 4px solid #dc3545;
            }
            
            .notification-content {
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .notification-close {
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                color: #6c757d;
                margin-left: 1rem;
            }
            
            .notification-close:hover {
                color: #333;
            }
            
            .navbar-inverse.scrolled {
                background: rgba(0, 0, 0, 0.95) !important;
                box-shadow: 0 2px 20px rgba(0,0,0,0.3);
            }
            
            .service-icon.pulse {
                animation: pulse 0.6s ease-in-out;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
        `)
        .appendTo('head');
    
    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();
    
    // Add loading animation to stats initially
    $('.stat-number').addClass('loading');
    
    // Remove loading class when counters start
    $('.stat-number').on('animationend', function() {
        $(this).removeClass('loading');
    });
    
    // Parallax effect for hero section
    $(window).on('scroll', function() {
        const scrolled = $(window).scrollTop();
        const parallax = $('.jumbotron');
        const speed = scrolled * 0.5;
        
        parallax.css('transform', `translateY(${speed}px)`);
    });
    
    // Add intersection observer for better performance
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        });
        
        $('.service-card, .stat-item').each(function() {
            observer.observe(this);
        });
    }
    
    // Mobile menu improvements
    $('.navbar-toggle').on('click', function() {
        $(this).toggleClass('active');
    });
    
    // Close mobile menu when clicking on a link
    $('.navbar-nav a').on('click', function() {
        if ($(window).width() < 768) {
            $('.navbar-collapse').collapse('hide');
            $('.navbar-toggle').removeClass('active');
        }
    });
    
    // Add some interactive elements
    $('.btn').on('click', function() {
        // Add ripple effect
        const $this = $(this);
        const ripple = $('<span class="ripple"></span>');
        
        $this.append(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
    
    // Add ripple effect CSS
    $('<style>')
        .prop('type', 'text/css')
        .html(`
            .btn {
                position: relative;
                overflow: hidden;
            }
            
            .ripple {
                position: absolute;
                border-radius: 50%;
                background: rgba(255,255,255,0.3);
                transform: scale(0);
                animation: ripple 0.6s linear;
                pointer-events: none;
            }
            
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `)
        .appendTo('head');
    
    console.log('Modern Web Solutions - Website loaded successfully!');
});
