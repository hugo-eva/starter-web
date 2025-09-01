// Payment page functionality with Stripe integration
(function() {
  'use strict';

  // Configuration
  const STRIPE_PUBLIC_KEY = 'pk_test_YOUR_STRIPE_PUBLIC_KEY'; // Replace with your actual Stripe public key
  const API_BASE_URL = '/api'; // Replace with your actual API endpoint
  
  // Initialize Stripe
  const stripe = Stripe(STRIPE_PUBLIC_KEY);
  const elements = stripe.elements();

  // Plan configuration
  const PLANS = {
    basic: {
      name: 'Basic',
      price: 7.99,
      priceId: 'price_basic_monthly', // Replace with actual Stripe Price ID
      features: [
        'Content management',
        'Basic templates', 
        'Screen scheduling',
        'Email support'
      ]
    },
    pro: {
      name: 'Pro', 
      price: 10.99,
      priceId: 'price_pro_monthly', // Replace with actual Stripe Price ID
      features: [
        'Everything in Basic',
        'Advanced analytics',
        'Multi-user management', 
        'Custom branding',
        'API access',
        'Priority support'
      ]
    }
  };

  // State management
  let currentState = {
    selectedPlan: 'basic',
    screenCount: 1,
    currentStep: 'plan-selection'
  };

  // DOM elements
  const planOptions = document.querySelectorAll('.plan-option');
  const screenCountInput = document.getElementById('screen-count');
  const continueBtn = document.getElementById('continue-to-payment');
  const backBtn = document.getElementById('back-to-plans');
  const paymentForm = document.getElementById('payment-form-element');
  const submitBtn = document.getElementById('submit-payment');
  const retryBtn = document.getElementById('retry-payment');

  // Initialize payment page
  function init() {
    // Get plan from URL params if present
    const urlParams = new URLSearchParams(window.location.search);
    const planFromUrl = urlParams.get('plan');
    if (planFromUrl && PLANS[planFromUrl]) {
      currentState.selectedPlan = planFromUrl;
      selectPlan(planFromUrl);
    }

    setupEventListeners();
    setupStripeElements();
    updatePricingSummary();
  }

  // Event listeners
  function setupEventListeners() {
    // Plan selection
    planOptions.forEach(option => {
      option.addEventListener('click', () => {
        const plan = option.dataset.plan;
        selectPlan(plan);
      });
    });

    // Screen count input
    screenCountInput.addEventListener('input', () => {
      currentState.screenCount = parseInt(screenCountInput.value) || 1;
      updatePricingSummary();
    });

    // Navigation buttons
    continueBtn.addEventListener('click', () => {
      showStep('payment-form');
      updateOrderSummary();
    });

    backBtn.addEventListener('click', () => {
      showStep('plan-selection');
    });

    // Payment form submission
    paymentForm.addEventListener('submit', handlePaymentSubmit);

    // Retry payment
    retryBtn.addEventListener('click', () => {
      showStep('payment-form');
    });
  }

  // Setup Stripe Elements
  function setupStripeElements() {
    const style = {
      base: {
        color: '#1e293b',
        fontFamily: 'Inter, ui-sans-serif, system-ui, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#64748b'
        }
      },
      invalid: {
        color: '#ef4444',
        iconColor: '#ef4444'
      }
    };

    const cardElement = elements.create('card', { style });
    cardElement.mount('#card-element');

    // Handle real-time validation errors from the card Element
    cardElement.on('change', ({ error }) => {
      const displayError = document.getElementById('card-errors');
      if (error) {
        displayError.textContent = error.message;
      } else {
        displayError.textContent = '';
      }
    });

    // Store card element for later use
    window.cardElement = cardElement;
  }

  // Plan selection
  function selectPlan(planKey) {
    currentState.selectedPlan = planKey;
    
    // Update UI
    planOptions.forEach(option => {
      option.classList.toggle('selected', option.dataset.plan === planKey);
    });

    updatePricingSummary();
  }

  // Update pricing summary
  function updatePricingSummary() {
    const plan = PLANS[currentState.selectedPlan];
    const totalPrice = plan.price * currentState.screenCount;

    // Update plan selection summary
    document.getElementById('selected-plan-name').textContent = plan.name;
    document.getElementById('plan-price').textContent = `$${plan.price.toFixed(2)}/month per screen`;
    document.getElementById('screen-count-display').textContent = currentState.screenCount;
    document.getElementById('total-price').textContent = `$${totalPrice.toFixed(2)}`;
    
    // Update screen count input
    screenCountInput.value = currentState.screenCount;
  }

  // Update order summary in payment step
  function updateOrderSummary() {
    const plan = PLANS[currentState.selectedPlan];
    const totalPrice = plan.price * currentState.screenCount;
    const screenText = currentState.screenCount === 1 ? 'screen' : 'screens';

    document.getElementById('order-plan-name').textContent = `${plan.name} Plan`;
    document.getElementById('order-plan-price').textContent = `$${plan.price.toFixed(2)}/month per screen`;
    document.getElementById('order-screen-count').textContent = `${currentState.screenCount} ${screenText}`;
    document.getElementById('order-total').textContent = `$${totalPrice.toFixed(2)}/month`;
  }

  // Show specific step
  function showStep(stepId) {
    document.querySelectorAll('.payment-step').forEach(step => {
      step.classList.remove('active');
    });
    document.getElementById(stepId).classList.add('active');
    currentState.currentStep = stepId;
  }

  // Handle payment form submission
  async function handlePaymentSubmit(event) {
    event.preventDefault();
    setLoading(true);

    const customerName = document.getElementById('customer-name').value;
    const customerEmail = document.getElementById('customer-email').value;

    if (!customerName || !customerEmail) {
      showError('Please fill in all required fields.');
      setLoading(false);
      return;
    }

    try {
      // Create customer and subscription on your backend
      const response = await fetch(`${API_BASE_URL}/create-subscription`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          customerName,
          customerEmail,
          planId: PLANS[currentState.selectedPlan].priceId,
          quantity: currentState.screenCount
        }),
      });

      const { clientSecret, error } = await response.json();

      if (error) {
        throw new Error(error);
      }

      // Confirm payment with Stripe
      const { error: stripeError } = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: window.cardElement,
          billing_details: {
            name: customerName,
            email: customerEmail,
          },
        }
      });

      if (stripeError) {
        throw new Error(stripeError.message);
      }

      // Payment successful
      showStep('payment-success');
      
    } catch (error) {
      console.error('Payment error:', error);
      showError(error.message || 'An unexpected error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  }

  // Set loading state
  function setLoading(isLoading) {
    const buttonText = document.getElementById('button-text');
    const spinner = document.getElementById('spinner');
    
    if (isLoading) {
      buttonText.textContent = 'Processing...';
      spinner.classList.remove('hidden');
      submitBtn.disabled = true;
    } else {
      buttonText.textContent = 'Subscribe Now';
      spinner.classList.add('hidden');
      submitBtn.disabled = false;
    }
  }

  // Show error
  function showError(message) {
    document.getElementById('error-message').textContent = message;
    showStep('payment-error');
  }

  // Format currency
  function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(amount);
  }

  // Initialize when DOM is loaded
  document.addEventListener('DOMContentLoaded', init);

})();