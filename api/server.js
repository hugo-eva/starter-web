// Backend API for Stripe subscription handling
// This is an example Node.js/Express server
const express = require('express');
const stripe = require('stripe')('sk_test_YOUR_STRIPE_SECRET_KEY'); // Replace with your actual secret key
const cors = require('cors');

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Plan configuration - should match frontend
const PLANS = {
  basic: {
    name: 'Basic',
    priceId: 'price_1234567890', // Replace with actual Stripe Price ID for Basic plan
    price: 7.99
  },
  pro: {
    name: 'Pro', 
    priceId: 'price_0987654321', // Replace with actual Stripe Price ID for Pro plan
    price: 10.99
  }
};

// Create subscription endpoint
app.post('/api/create-subscription', async (req, res) => {
  try {
    const { customerName, customerEmail, planId, quantity } = req.body;

    // Validate input
    if (!customerName || !customerEmail || !planId || !quantity) {
      return res.status(400).json({ 
        error: 'Missing required fields: customerName, customerEmail, planId, quantity' 
      });
    }

    // Find the plan
    const plan = Object.values(PLANS).find(p => p.priceId === planId);
    if (!plan) {
      return res.status(400).json({ error: 'Invalid plan selected' });
    }

    // Create or retrieve customer
    let customer;
    const existingCustomers = await stripe.customers.list({
      email: customerEmail,
      limit: 1,
    });

    if (existingCustomers.data.length > 0) {
      customer = existingCustomers.data[0];
    } else {
      customer = await stripe.customers.create({
        name: customerName,
        email: customerEmail,
      });
    }

    // Create the subscription
    const subscription = await stripe.subscriptions.create({
      customer: customer.id,
      items: [{
        price: planId,
        quantity: quantity,
      }],
      payment_behavior: 'default_incomplete',
      payment_settings: { save_default_payment_method: 'on_subscription' },
      expand: ['latest_invoice.payment_intent'],
    });

    res.json({
      subscriptionId: subscription.id,
      clientSecret: subscription.latest_invoice.payment_intent.client_secret,
    });

  } catch (error) {
    console.error('Subscription creation error:', error);
    res.status(500).json({ 
      error: error.message || 'Failed to create subscription' 
    });
  }
});

// Webhook endpoint for Stripe events
app.post('/api/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature'];
  const webhookSecret = 'whsec_YOUR_WEBHOOK_SECRET'; // Replace with your actual webhook secret

  let event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle the event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object;
      console.log('PaymentIntent was successful:', paymentIntent.id);
      // Handle successful payment here
      break;

    case 'invoice.payment_succeeded':
      const invoice = event.data.object;
      console.log('Invoice payment succeeded:', invoice.id);
      // Handle successful recurring payment here
      break;

    case 'invoice.payment_failed':
      const failedInvoice = event.data.object;
      console.log('Invoice payment failed:', failedInvoice.id);
      // Handle failed payment here (e.g., send email notification)
      break;

    case 'customer.subscription.deleted':
      const subscription = event.data.object;
      console.log('Subscription cancelled:', subscription.id);
      // Handle subscription cancellation here
      break;

    default:
      console.log(`Unhandled event type ${event.type}`);
  }

  res.json({ received: true });
});

// Get subscription details
app.get('/api/subscription/:id', async (req, res) => {
  try {
    const subscription = await stripe.subscriptions.retrieve(req.params.id);
    res.json(subscription);
  } catch (error) {
    res.status(404).json({ error: 'Subscription not found' });
  }
});

// Cancel subscription
app.post('/api/subscription/:id/cancel', async (req, res) => {
  try {
    const subscription = await stripe.subscriptions.update(req.params.id, {
      cancel_at_period_end: true
    });
    res.json(subscription);
  } catch (error) {
    res.status(500).json({ error: 'Failed to cancel subscription' });
  }
});

// Update subscription quantity
app.post('/api/subscription/:id/update', async (req, res) => {
  try {
    const { quantity } = req.body;
    
    const subscription = await stripe.subscriptions.retrieve(req.params.id);
    const updatedSubscription = await stripe.subscriptions.update(req.params.id, {
      items: [{
        id: subscription.items.data[0].id,
        quantity: quantity,
      }],
    });
    
    res.json(updatedSubscription);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update subscription' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

module.exports = app;