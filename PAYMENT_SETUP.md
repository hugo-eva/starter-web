# Lumy TV Payment System Setup

This document explains how to set up the Stripe payment system for Lumy TV's device-based subscription pricing.

## Overview

The payment system implements a DisplayNow.io-style pricing model:
- **Basic Plan**: $7.99 per screen per month
- **Pro Plan**: $10.99 per screen per month
- **Enterprise**: Custom pricing (contact sales)

## Frontend Implementation

### Files Created/Modified:
1. `pricing/index.html` - Updated pricing page with new device-based plans
2. `payment/index.html` - New payment page with Stripe integration
3. `assets/js/payment.js` - Payment page functionality
4. `assets/js/main.js` - Updated pricing calculator
5. `assets/css/styles.css` - Added payment page styles

### Key Features:
- Device count selector with real-time price calculation
- Stripe Elements integration for secure payment processing
- Responsive design for mobile and desktop
- Multi-step payment flow (plan selection → payment → confirmation)

## Backend API

### Files Created:
1. `api/server.js` - Express.js server with Stripe integration
2. `api/package.json` - Node.js dependencies

### API Endpoints:
- `POST /api/create-subscription` - Create new subscription
- `POST /api/webhook` - Handle Stripe webhooks
- `GET /api/subscription/:id` - Get subscription details
- `POST /api/subscription/:id/cancel` - Cancel subscription
- `POST /api/subscription/:id/update` - Update subscription quantity

## Setup Instructions

### 1. Stripe Account Setup

1. Create a Stripe account at https://stripe.com
2. Get your API keys from the Stripe Dashboard
3. Create Products and Prices in Stripe:

#### Basic Plan Product:
```
Name: Basic Plan
Description: Essential digital signage features
```

#### Basic Plan Price:
```
Price: $7.99 USD
Billing: Monthly
Type: Recurring
```

#### Pro Plan Product:
```
Name: Pro Plan  
Description: Advanced features for growing businesses
```

#### Pro Plan Price:
```
Price: $10.99 USD
Billing: Monthly
Type: Recurring
```

### 2. Frontend Configuration

Update `assets/js/payment.js`:

```javascript
// Replace with your actual Stripe public key
const STRIPE_PUBLIC_KEY = 'pk_test_YOUR_ACTUAL_PUBLIC_KEY';

// Update with your actual Stripe Price IDs
const PLANS = {
  basic: {
    priceId: 'price_YOUR_BASIC_PRICE_ID', 
    // ... rest of config
  },
  pro: {
    priceId: 'price_YOUR_PRO_PRICE_ID',
    // ... rest of config
  }
};
```

### 3. Backend Configuration

1. Install dependencies:
```bash
cd api
npm install
```

2. Update `api/server.js`:
```javascript
// Replace with your actual Stripe secret key
const stripe = require('stripe')('sk_test_YOUR_ACTUAL_SECRET_KEY');

// Update webhook secret
const webhookSecret = 'whsec_YOUR_ACTUAL_WEBHOOK_SECRET';

// Update Price IDs to match your Stripe configuration
const PLANS = {
  basic: {
    priceId: 'price_YOUR_BASIC_PRICE_ID',
    // ...
  },
  pro: {
    priceId: 'price_YOUR_PRO_PRICE_ID', 
    // ...
  }
};
```

3. Set up environment variables (create `.env` file):
```
STRIPE_SECRET_KEY=sk_test_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
PORT=3000
```

4. Start the server:
```bash
npm start
# or for development
npm run dev
```

### 4. Webhook Configuration

1. In Stripe Dashboard, go to Developers → Webhooks
2. Add endpoint: `https://yourdomain.com/api/webhook`
3. Select events to listen for:
   - `payment_intent.succeeded`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.deleted`

### 5. Testing

1. Use Stripe's test mode and test cards:
   - Success: `4242424242424242`
   - Decline: `4000000000000002`
   - 3D Secure: `4000002500003155`

2. Test the payment flow:
   - Visit `/payment/?plan=basic` or `/payment/?plan=pro`
   - Select device count
   - Enter test payment details
   - Verify subscription creation in Stripe Dashboard

## Security Considerations

1. **Never expose secret keys** in frontend code
2. **Validate all inputs** on the backend
3. **Verify webhook signatures** to ensure requests are from Stripe
4. **Use HTTPS** in production
5. **Implement proper error handling** and logging
6. **Store sensitive data securely** (consider using environment variables)

## Production Deployment

1. Replace test keys with live keys
2. Update webhook endpoints to production URLs
3. Configure proper SSL certificates
4. Set up monitoring and alerting
5. Test thoroughly with real payment methods

## Additional Features to Consider

1. **Proration handling** for mid-cycle plan changes
2. **Dunning management** for failed payments
3. **Customer portal** for self-service subscription management
4. **Usage-based billing** for overages
5. **Multi-currency support**
6. **Tax calculation** integration
7. **Coupon/discount codes**

## Support

For Stripe-related issues, refer to:
- [Stripe Documentation](https://stripe.com/docs)
- [Stripe Support](https://support.stripe.com)

For implementation questions, check the code comments and console logs for debugging information.