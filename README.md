# ophirstays.com

Static site (HTML/CSS) + one serverless function for the owner estimate form. No framework, no build step for Vercel.

## Edit
Pages are generated from `build.py` (shared header, footer, marks). Edit copy there, then run `python3 build.py`.
Styles: `assets/styles.css`. Form handler: `api/estimate.js`.

## Go live (about 30 minutes)
1. **GitHub:** create a private repo `ophir-stays-site`, upload this folder.
2. **Vercel:** vercel.com → sign in with GitHub → Add New → Project → import the repo → Deploy. Upgrade the team to Pro ($20/mo) before launch; Hobby is non-commercial.
3. **Domain:** Vercel → Project → Settings → Domains → add `ophirstays.com` and `www.ophirstays.com`. Vercel shows two DNS records. In GoDaddy → My Products → DNS for ophirstays.com: add the A record (`@` → Vercel's IP) and the CNAME (`www` → `cname.vercel-dns.com`). Delete GoDaddy's default "Parked" A record. Live within an hour.
4. **stayophir.com:** in Vercel add it too and set it to redirect to ophirstays.com (or use GoDaddy forwarding, 301).
5. **Form email:** resend.com → sign up → Domains → add ophirstays.com → copy its DNS records into GoDaddy → verify. Create an API key. In Vercel → Settings → Environment Variables add:
   - `RESEND_API_KEY` = the key
   - `OWNER_INBOX` = casey@ophirstays.com
   - `FROM_ADDRESS` = `Ophir Stays <hello@ophirstays.com>`
   Redeploy. Submit a test request on /owners.

## Photos (the most important part)
Every photo is a file in `assets/photos/`. Save your photo over the placeholder with the **same name** and it appears everywhere. Shoot landscape, at least 2400 px wide, natural light, no filters.

| File | Shot | Shape |
|---|---|---|
| hero-ski.jpg | Skier in powder at Purgatory, morning light | wide 16:7 |
| hero-fireplace.jpg | Great room, fire lit, dusk, blankets | wide 16:7 |
| hero-bike.jpg | Rider on singletrack, golden hour | wide 16:7 |
| hero-spa.jpg | Steaming hot tub facing the mountains | wide 16:7 |
| hero-golf.jpg | Fairway under the cliffs | wide 16:7 |
| hero-coffee.jpg | Barista pour or a cup on a Main Ave counter | wide 16:7 |
| ski, spa, golf, bike, coffee, fireplace .jpg | Tighter detail shots of each | 4:3 |
| ophir.jpg | The town of Ophir or Ophir Pass | 4:3 |
| home-1.jpg | Exterior of your best Collection home | 4:3 |
| casey.jpg | Portrait of you, outdoors | 4:5 |
| journal-1/2/3.jpg | Trail, river, a home at dusk | 4:3 |

Only use photos you took, paid for, or have written permission to use.

## Homes (The Collection)
In `build.py`, find `HOMES = [`. Copy the sample block for each signed home: slug, name, area, beds, baths, sleeps, one-line description, 4–6 features and a sample trip. Set `sample=False`.
Save 5 photos per home in `assets/photos/homes/` as `<slug>-1.jpg` … `-5.jpg`: 1 exterior or view, 2 great room, 3 kitchen, 4 primary bedroom, 5 hot tub or deck. Landscape, 2400 px wide, shot by your photographer.
**Before launch set `SHOW_SAMPLES = False`.** With no real homes yet, the site shows a "Founding homes · Apply" panel instead. Get each owner's written OK before publishing their home.

## Journal
Add a post by copying the `post_body` block in `build.py`, changing the text and path, and adding it to the list at the bottom. Two posts a month.

## Before launch
- Replace the portrait placeholder on /about with a real photo (`assets/casey.jpg`, 1200×1500).
- Have a lawyer confirm the guarantee summary on /owners matches the owner agreement.
- Fonts: Holtwood One SC stands in for the Mesa wordmark font until its license is cleared.

## The app (v1)
Booking -> trip -> AI welcome email -> guest pre-trip page -> AI itinerary + team tasks -> Casey approves -> guest sees the plan.
- Guest page: `/trip/<token>` (trip.html + api/trip.js)
- Admin: `/admin` (admin.html + api/admin.js), password = `ADMIN_PASSWORD`
- Hostaway webhook: `/api/hostaway?secret=<HOSTAWAY_WEBHOOK_SECRET>` (api/hostaway.js)
- Database schema: `supabase/schema.sql`
Env vars: SUPABASE_URL, SUPABASE_SECRET_KEY, ANTHROPIC_API_KEY, ADMIN_PASSWORD, RESEND_API_KEY, OWNER_INBOX, FROM_ADDRESS, (later) HOSTAWAY_WEBHOOK_SECRET, ANTHROPIC_MODEL.

## Payments (Stripe)
- `api/checkout.js` creates a Stripe Checkout session for fixed-price offers (packages and add-ons).
- `api/stripe-webhook.js` marks the payment paid, upgrades the package, re-plans with AI and emails Casey to approve.
- Env: `STRIPE_SECRET_KEY` (sk_test_… then sk_live_…), `STRIPE_WEBHOOK_SECRET` (whsec_…).
- Webhook endpoint: https://ophirstays.com/api/stripe-webhook, event `checkout.session.completed`.

## Charging guests for partner bookings (bikes, skis, rafting, golf, massage)
1. Run the v1.4 `charges` block from supabase/schema.sql once.
2. In admin, open the trip, fill in "Charge the guest": item, amount, optional note, then "Send to guest".
3. The guest gets an email and a Confirm button on their trip page; they pay through Stripe.
4. When they pay you get a "Paid" email and a task to confirm with the partner. Pay the partner its net rate.
Cancel an unpaid charge with its Cancel button.

## Ask Ophir (guest Q&A)

The guest trip page has an "Ask Ophir" box once the trip is planned. It answers from the home's `house_notes`, the itinerary, the forecast, your restaurant list and stable Durango knowledge. Door code and Wi-Fi are only available to it from arrival day.

- Anything it can't answer from the data (house details not in `house_notes`, bookings, changes, refunds) or anything urgent (no heat, a leak, a lockout, an alarm) creates a task for Casey and emails `OWNER_INBOX`. Urgent ones are marked URGENT and due in 15 minutes.
- The limit is 20 questions per trip per day. Every question and answer is saved in `messages` with subject "Ask Ophir" and shows in the admin trip detail.
- Answers are only as good as `house_notes`. Fill it in for every home: hot tub, thermostat, trash day, parking, checkout steps.
- No new SQL or env vars are needed.
