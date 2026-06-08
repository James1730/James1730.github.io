"""
Build Sundays website V4 with Annie's curated image categories.
6 sections: Hero Slider, Best Sellers, Factory, Client Partnerships, Logistics, Certificates
Plus the 252-product catalog.
"""
import json
from html import escape

# Load products
with open('data/categorized-products.json', 'r', encoding='utf-8') as f:
    products = json.load(f)

CAT_ORDER = [
    'Pool Table', 'Snooker Table', 'Multi-function Pool Table',
    'Coin Operated Pool Table', 'Chinese Billiard Table',
    'Customized Billiard Table', 'Glass Pool Table', 'MDF Pool Table',
    'Billiard Accessories'
]

total = sum(len(products[c]) for c in CAT_ORDER if c in products)
num_cats = len(CAT_ORDER)

# Build category buttons — default to Pool Table
DEFAULT_CAT = 'Pool Table'
default_count = len(products.get(DEFAULT_CAT, []))
cat_buttons = '<button class="cat-btn" onclick="filterCat(\'all\',this)">All<span class="cat-count">{}</span></button>'.format(total)
for cat in CAT_ORDER:
    if cat in products and len(products[cat]) > 0:
        active = ' active' if cat == DEFAULT_CAT else ''
        cat_buttons += '<button class="cat-btn{}" onclick="filterCat(\'{}\',this)">{}<span class="cat-count">{}</span></button>'.format(
            active, escape(cat), escape(cat), len(products[cat]))

# Build product cards — hide non-default categories
product_cards = ''
for cat in CAT_ORDER:
    if cat not in products:
        continue
    for p in products[cat]:
        hidden = ' hidden' if cat != DEFAULT_CAT else ''
        product_cards += '<a class="p-card{}" href="{}" target="_blank" rel="noopener" data-cat="{}"><div class="p-img"><img src="{}" alt="{}" loading="lazy" onerror="this.src=\'https://sc02.alicdn.com/kf/A266d87002c594a26b5fee969b9f02ec4A.png\'"></div><div class="p-body"><h3>{}</h3><div class="p-price">{}</div><div class="p-moq">MOQ: 1 set</div></div></a>\n'.format(
            hidden, escape(p['url']), escape(cat), escape(p['image']), escape(p['name']), escape(p['name']), escape(p['price']))

# Image CDN URLs (from see_image uploads)
IMAGES = {
    # 首页轮播图 (removed hero1 Dynaspheres per Annie's request)
    'hero2': 'https://sc02.alicdn.com/kf/A5bcf5314b3554e23a2b1df8bfd8ecdc43.png',  # Snooker + accessories
    'hero3': 'https://sc02.alicdn.com/kf/A4b49cca6d2d748088fff7946bfc9c3feZ.png',  # Customized pool table
    'hero4': 'https://sc02.alicdn.com/kf/A7b287a1b380c4247b7982aeb7dd217b7c.png',  # SDAiS Platinum balls

    # 常卖的款式
    'best1': 'https://sc02.alicdn.com/kf/A5f9ebfe00b9b4b7080ed6893b0cd509cC.png',  # Club snooker
    'best2': 'https://sc02.alicdn.com/kf/A92fc751f4e464294a04330ee2f2f6f4d8.png',  # SDAiS LED pool table
    'best3': 'https://sc02.alicdn.com/kf/Adcc83ac77a6f432dacc30a79a1409bb5g.png',  # White table angle 2
    'best4': 'https://sc02.alicdn.com/kf/A7b87430db0134c1381374e32c930e386D.png',  # Classic gold-leg snooker

    # 工厂
    'fac1': 'https://sc02.alicdn.com/kf/A4bfde35e22454ae6ad12fd00ced0ebe8C.png',  # Wood stacking
    'fac2': 'https://sc02.alicdn.com/kf/A95ec7f5f425546d2a5d12a197b7115bbJ.png',  # Table legs batch
    'fac3': 'https://sc02.alicdn.com/kf/A677d7f3c34b6402083ada352c75d8625M.png',  # White legs + castings
    'fac4': 'https://sc02.alicdn.com/kf/A74832d556f3a41f18a32fc38e57263413.png',  # Factory panorama
    'fac5': 'https://sc02.alicdn.com/kf/Ab3f8556de7584ed08613565f14dc8976j.png',  # Showroom with clients (NEW)

    # 外国客户合作
    'cli1': 'https://sc02.alicdn.com/kf/A4aca7b627d034867b18df607217642a4V.png',  # European group SDAiS
    'cli2': 'https://sc02.alicdn.com/kf/Aca34dcac59b74d25ad41c0083ed304d7c.png',  # Trade show group
    'cli3': 'https://sc02.alicdn.com/kf/A36e8f2bd92a04b7286b66fa05574bd75u.png',  # Contract signing
    'cli4': 'https://sc02.alicdn.com/kf/Adc5adbd3a7534ad8a35b104ab0de65b6N.png',  # Container loading group
    'cli5': 'https://sc02.alicdn.com/kf/Afc03288afbbd46d29b098ac4145d1f17N.png',  # African clients SDAiS
    'cli6': 'https://sc02.alicdn.com/kf/A4ed972203583418fa37856dbb96fd8bfr.png',  # Gold table legs batch (NEW)

    # 物流
    'ship': 'https://sc02.alicdn.com/kf/A1cdaa1f8016a4f3f8489e8cca1f49ce9X.png',

    # 证书
    'cert': 'https://sc02.alicdn.com/kf/A28eb205c1dba4cd5a8560650e1d523day.png',

    # New Hero Slides
    'hero5': 'https://sc02.alicdn.com/kf/Ab6bef6b51420430cb34202b7ac6efea7H.png',  # Generation 4 blue
    'hero6': 'https://sc02.alicdn.com/kf/Aac9764b0571e4213be5d0b545fa0c99cR.png',  # Generation 4 gray
    'hero7': 'https://sc02.alicdn.com/kf/A1ced8e8c98e743cf886a88531be3add5U.png',  # Customized Pool Table banner

    # Logo
    'logo': 'https://sc02.alicdn.com/kf/A266d87002c594a26b5fee969b9f02ec4A.png',
}

I = IMAGES

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sundays Billiard — Pool Table & Snooker Table Manufacturer in China | Factory Direct Since 2005</title>
    <meta name="description" content="Guangzhou billiard table factory since 2005. Custom pool tables, snooker tables, coin-operated tables & accessories. ISO 9001, SGS, SMETA certified. 8,000m² factory, export to 50+ countries. OEM/ODM welcome. Get quote today.">
    <meta name="keywords" content="pool table manufacturer, billiard table factory, snooker table supplier, pool table China, custom pool table, coin operated pool table, billiard table wholesale, OEM pool table, pool table factory Guangzhou, commercial billiard table, Sundays billiard, SDAiS, wholesale pool tables USA, billiard suppliers Europe, pool table manufacturer Middle East">
    <meta name="author" content="Guangzhou Wanjin Sports Equipment Co., Ltd.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://james1730.github.io/">
    <link rel="alternate" hreflang="en" href="https://james1730.github.io/">
    <link rel="alternate" hreflang="x-default" href="https://james1730.github.io/">


    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://james1730.github.io/">
    <meta property="og:title" content="Sundays Billiard — Professional Pool Table Manufacturer | Factory Direct Since 2005">
    <meta property="og:description" content="19+ years billiard table manufacturing. Custom pool tables, snooker tables & accessories. ISO 9001 certified, 8,000m² factory, 50+ countries. Get factory-direct quote.">
    <meta property="og:image" content="{I['hero3']}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="Sundays Billiard">
    <meta property="og:locale" content="en_US">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Sundays Billiard — Pool Table Manufacturer in China">
    <meta name="twitter:description" content="Factory direct billiard tables since 2005. Custom pool tables, snooker tables. ISO certified, 8,000m² factory. Get quote today.">
    <meta name="twitter:image" content="{I['hero3']}">

    <!-- Structured Data - Organization -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": "Sundays Billiard",
      "alternateName": ["Guangzhou Wanjin Sports Equipment Co., Ltd.", "SDAiS"],
      "url": "https://james1730.github.io/",
      "logo": "{I['logo']}",
      "description": "Professional billiard table manufacturer in Guangzhou, China since 2005. Specializing in pool tables, snooker tables, coin-operated tables & accessories.",
      "foundingDate": "2005",
      "address": {{
        "@type": "PostalAddress",
        "addressLocality": "Guangzhou",
        "addressRegion": "Guangdong",
        "addressCountry": "CN"
      }},
      "contactPoint": {{
        "@type": "ContactPoint",
        "telephone": "+86-18824156040",
        "contactType": "sales",
        "email": "sundaysbilliard@hotmail.com",
        "availableLanguage": ["English", "Chinese"]
      }},
      "sameAs": [
        "https://gzsundays.en.alibaba.com/",
        "https://www.facebook.com/sundaysbilliard"
      ],
      "hasOfferCatalog": {{
        "@type": "OfferCatalog",
        "name": "Billiard Tables & Accessories",
        "itemListElement": [
          {{"@type": "Offer", "itemOffered": {{"@type": "Product", "name": "Pool Tables"}}}},
          {{"@type": "Offer", "itemOffered": {{"@type": "Product", "name": "Snooker Tables"}}}},
          {{"@type": "Offer", "itemOffered": {{"@type": "Product", "name": "Coin Operated Pool Tables"}}}},
          {{"@type": "Offer", "itemOffered": {{"@type": "Product", "name": "Billiard Accessories"}}}}
        ]
      }}
    }}
    </script>

    <link rel="icon" type="image/png" href="{I['logo']}">
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
        :root{{
            --gold:#C9A96E;--gold-light:#D4B87A;--gold-dark:#A68B5B;
            --black:#090909;--black2:#111;--black3:#181818;--black4:#222;
            --gray:#888;--gray-light:#bbb;--white:#f0f0f0;
            --ff-h:'Playfair Display',serif;--ff-b:'Inter',sans-serif;
            --ease:all .4s cubic-bezier(.25,.46,.45,.94);
        }}
        html{{scroll-behavior:smooth;font-size:16px}}
        body{{font-family:var(--ff-b);background:var(--black);color:var(--white);line-height:1.6;overflow-x:hidden}}
        img{{max-width:100%;display:block}}
        a{{text-decoration:none;color:inherit}}

        /* NAV */
        .nav{{position:fixed;top:0;left:0;right:0;z-index:100;padding:22px 50px;display:flex;align-items:center;justify-content:space-between;transition:var(--ease)}}
        .nav.scrolled{{background:rgba(255,255,255,.97);backdrop-filter:blur(20px);padding:14px 50px;border-bottom:1px solid rgba(0,0,0,.08);box-shadow:0 2px 12px rgba(0,0,0,.06)}}
        .nav.scrolled .nav-links a{{color:#111}}
        .nav.scrolled .nav-links a:hover{{color:var(--gold)}}
        .nav.scrolled .nav-cta{{border-color:#111!important;color:#111!important}}
        .nav.scrolled .nav-cta:hover{{background:#111!important;color:#fff!important}}
        .nav-logo img{{height:60px;transition:var(--ease)}}
        .nav.scrolled .nav-logo img{{height:46px}}
        .nav-links{{display:flex;gap:32px;align-items:center}}
        .nav-links a{{font-size:.78rem;font-weight:400;letter-spacing:2.5px;text-transform:uppercase;color:var(--gray-light);transition:var(--ease)}}
        .nav-links a:hover{{color:var(--gold)}}
        .nav-cta{{padding:10px 26px!important;border:1px solid var(--gold)!important;color:var(--gold)!important;transition:var(--ease)!important}}
        .nav-cta:hover{{background:var(--gold)!important;color:var(--black)!important}}
        .hamburger{{display:none;cursor:pointer;flex-direction:column;gap:5px;z-index:102}}
        .hamburger span{{width:24px;height:1.5px;background:var(--gold);transition:var(--ease)}}

        /* HERO SLIDER */
        .hero-slider{{position:relative;width:100%;overflow:hidden;max-height:680px}}
        .slides{{display:flex;transition:transform .6s ease}}
        .slide{{min-width:100%;position:relative}}
        .slide img{{width:100%;height:680px;object-fit:cover;display:block}}
        .slider-btn{{position:absolute;top:50%;transform:translateY(-50%);background:rgba(0,0,0,.5);color:var(--gold);border:1px solid var(--gold);width:48px;height:48px;font-size:1.2rem;cursor:pointer;z-index:10;transition:var(--ease);display:flex;align-items:center;justify-content:center}}
        .slider-btn:hover{{background:var(--gold);color:var(--black)}}
        .slider-prev{{left:20px}}
        .slider-next{{right:20px}}
        .slider-dots{{position:absolute;bottom:20px;left:50%;transform:translateX(-50%);display:flex;gap:10px;z-index:10}}
        .slider-dot{{width:12px;height:12px;border-radius:50%;border:2px solid var(--gold);background:transparent;cursor:pointer;transition:var(--ease)}}
        .slider-dot.active{{background:var(--gold)}}

        /* STATS */
        .stats{{padding:48px 50px;border-top:1px solid rgba(201,169,110,.12);border-bottom:1px solid rgba(201,169,110,.12);background:var(--black2)}}
        .stats-inner{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:30px;text-align:center}}
        .stat-n{{font-family:var(--ff-h);font-size:2.6rem;font-weight:700;color:var(--gold);line-height:1}}
        .stat-l{{font-size:.72rem;letter-spacing:2px;text-transform:uppercase;color:var(--gray);margin-top:6px}}

        /* SECTIONS */
        .sec{{padding:100px 50px}}
        .sec-head{{text-align:center;margin-bottom:50px}}
        .sec-tag{{font-size:.68rem;letter-spacing:4px;text-transform:uppercase;color:var(--gold);margin-bottom:14px}}
        .sec-title{{font-family:var(--ff-h);font-size:clamp(1.8rem,3.5vw,2.8rem);font-weight:600;line-height:1.2;margin-bottom:16px}}
        .sec-desc{{font-size:1rem;font-weight:300;color:var(--gray);max-width:600px;margin:0 auto;line-height:1.8}}
        .gold-bar{{width:50px;height:2px;background:var(--gold);margin:18px auto 0}}

        /* BEST SELLERS */
        .bestsellers{{background:var(--black)}}
        .bs-grid{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:16px}}
        .bs-item{{overflow:hidden;border-radius:3px;position:relative;background:var(--black2)}}
        .bs-item img{{width:100%;aspect-ratio:1/1;object-fit:contain;padding:10%;transition:transform .5s ease;filter:brightness(.9)}}
        .bs-item:hover img{{transform:scale(1.05);filter:brightness(1)}}
        .bs-label{{position:absolute;bottom:0;left:0;right:0;padding:16px;background:linear-gradient(to top,rgba(0,0,0,.75),transparent);font-family:var(--ff-h);font-size:.9rem;color:var(--white);letter-spacing:1px}}

        /* FACTORY */
        .factory{{background:var(--black2)}}
        .fac-grid{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(2,1fr);gap:16px}}
        .fac-grid .g-item:first-child{{grid-column:span 2}}
        .g-item{{overflow:hidden;border-radius:3px;position:relative;cursor:pointer}}
        .g-item img{{width:100%;aspect-ratio:16/9;object-fit:cover;transition:transform .5s ease,filter .5s ease;filter:brightness(.85)}}
        .fac-grid .g-item:first-child img{{aspect-ratio:21/9}}
        .g-item:hover img{{transform:scale(1.04);filter:brightness(1)}}
        .g-caption{{position:absolute;bottom:0;left:0;right:0;padding:14px 16px;background:linear-gradient(to top,rgba(0,0,0,.7),transparent);font-size:.78rem;color:var(--white);letter-spacing:1px;opacity:0;transition:var(--ease)}}
        .g-item:hover .g-caption{{opacity:1}}

        /* CLIENTS */
        .clients{{background:var(--black)}}
        .cli-grid{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
        .cli-grid .g-item img{{aspect-ratio:4/3;object-fit:cover}}

        /* CLIENT REVIEWS */
        .reviews{{background:var(--black);padding:80px 50px}}
        .rev-grid{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:24px}}
        .rev-card{{background:var(--black2);border:1px solid rgba(201,169,110,.12);border-radius:12px;overflow:hidden;position:relative}}
        .rev-img{{width:100%;height:200px;object-fit:cover}}
        .rev-body{{padding:24px 28px 28px}}
        .rev-stars{{color:#F5A623;font-size:1rem;margin-bottom:12px;letter-spacing:2px}}
        .rev-text{{color:var(--gray);font-size:.88rem;line-height:1.7;margin-bottom:20px;font-style:italic}}
        .rev-author{{display:flex;align-items:center;gap:12px}}
        .rev-avatar{{width:44px;height:44px;border-radius:50%;background:var(--gold);color:var(--black);display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1rem}}
        .rev-name{{color:#fff;font-weight:600;font-size:.9rem}}
        .rev-country{{color:var(--gray);font-size:.78rem}}
        .rev-quote{{position:absolute;top:8px;right:16px;font-size:2.5rem;color:rgba(201,169,110,.15);font-family:Georgia,serif}}
        .rev-body{{position:relative}}

        /* FAQ */
        .faq-section{{background:var(--black2);padding:80px 50px}}
        .faq-wrap{{max-width:900px;margin:0 auto}}
        .faq-item{{border-bottom:1px solid rgba(201,169,110,.1);overflow:hidden}}
        .faq-q{{display:flex;justify-content:space-between;align-items:center;padding:22px 0;cursor:pointer;color:#fff;font-size:1rem;font-weight:500;transition:color .3s}}
        .faq-q:hover{{color:var(--gold)}}
        .faq-q .faq-icon{{font-size:1.3rem;color:var(--gold);transition:transform .3s;flex-shrink:0;margin-left:16px}}
        .faq-item.open .faq-icon{{transform:rotate(45deg)}}
        .faq-a{{max-height:0;overflow:hidden;transition:max-height .4s ease,padding .4s ease;padding:0 0}}
        .faq-item.open .faq-a{{max-height:300px;padding:0 0 22px 0}}
        .faq-a p{{color:var(--gray);font-size:.88rem;line-height:1.8;margin:0}}

        /* SHIPPING & CERT (side by side) */
        .ship-cert{{background:var(--black2);padding:80px 50px}}
        .sc-wrap{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:40px}}
        .sc-box{{text-align:center}}
        .sc-box{{display:flex;flex-direction:column}}
        .sc-box img{{width:100%;flex:1;object-fit:cover;border-radius:4px}}
        .sc-box h3{{font-family:var(--ff-h);font-size:1.2rem;color:var(--gold);margin-bottom:16px;letter-spacing:2px}}

        /* PRODUCTS CATALOG */
        .catalog{{background:var(--black)}}
        .cat-bar{{display:flex;justify-content:center;gap:6px;margin-bottom:24px;flex-wrap:wrap;max-width:1200px;margin-left:auto;margin-right:auto}}
        .cat-btn{{padding:9px 22px;border:1px solid rgba(201,169,110,.2);background:transparent;color:var(--gray-light);font-family:var(--ff-b);font-size:.72rem;letter-spacing:1.5px;text-transform:uppercase;cursor:pointer;transition:var(--ease);white-space:nowrap}}
        .cat-btn:hover,.cat-btn.active{{background:var(--gold);color:var(--black);border-color:var(--gold)}}
        .cat-count{{font-size:.6rem;opacity:.7;margin-left:4px}}
        .catalog-grid{{max-width:1280px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:20px}}
        .p-card{{background:var(--black3);border:1px solid rgba(201,169,110,.06);overflow:hidden;transition:var(--ease);cursor:pointer;text-decoration:none;color:inherit;display:block}}
        .p-card:hover{{border-color:rgba(201,169,110,.22);transform:translateY(-5px);box-shadow:0 16px 40px rgba(0,0,0,.5)}}
        .p-card.hidden{{display:none}}
        .p-img{{width:100%;aspect-ratio:1/1;overflow:hidden;background:var(--black4)}}
        .p-img img{{width:100%;height:100%;object-fit:cover;transition:transform .5s ease}}
        .p-card:hover .p-img img{{transform:scale(1.06)}}
        .p-body{{padding:16px 18px}}
        .p-body h3{{font-size:.82rem;font-weight:500;line-height:1.4;margin-bottom:8px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.3em}}
        .p-price{{font-family:var(--ff-h);font-size:1rem;font-weight:600;color:var(--gold)}}
        .p-moq{{font-size:.68rem;color:var(--gray);margin-top:2px}}
        .product-count{{text-align:center;margin-bottom:20px;font-size:.78rem;color:var(--gray);letter-spacing:1px}}

        /* CONTACT */
        .contact{{background:var(--black2)}}
        .contact-wrap{{max-width:1060px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:70px}}
        .c-block{{margin-bottom:28px}}
        .c-block h4{{font-family:var(--ff-h);font-size:1rem;color:var(--gold);margin-bottom:10px}}
        .c-block p,.c-block a{{font-size:.88rem;color:var(--gray-light);line-height:1.8}}
        .c-block a:hover{{color:var(--gold)}}
        .c-block i{{color:var(--gold);width:20px;margin-right:8px}}
        .c-form{{display:flex;flex-direction:column;gap:16px}}
        .c-form input,.c-form textarea,.c-form select{{width:100%;background:var(--black);border:1px solid rgba(201,169,110,.18);color:var(--white);padding:14px 18px;font-family:var(--ff-b);font-size:.88rem;outline:none;transition:var(--ease)}}
        .c-form input:focus,.c-form textarea:focus,.c-form select:focus{{border-color:var(--gold)}}
        .c-form textarea{{resize:vertical;min-height:110px}}
        .c-row{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}

        /* FOOTER */
        .footer{{border-top:1px solid rgba(201,169,110,.1);padding:50px 50px 24px;background:var(--black)}}
        .footer-inner{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:40px;margin-bottom:40px}}
        .footer-brand p{{color:var(--gray);font-size:.82rem;line-height:1.8;margin-top:14px}}
        .footer-col h4{{font-family:var(--ff-h);font-size:.95rem;color:var(--gold);margin-bottom:16px}}
        .footer-col a{{display:block;font-size:.82rem;color:var(--gray);margin-bottom:8px;transition:var(--ease)}}
        .footer-col a:hover{{color:var(--gold);padding-left:4px}}
        .f-social{{display:flex;gap:14px;margin-top:18px}}
        .f-social a{{width:52px;height:52px;border:1px solid rgba(255,255,255,.15);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.4rem;transition:var(--ease)}}
        .f-social a.wa{{color:#25D366;border-color:rgba(37,211,102,.3)}} .f-social a.wa:hover{{background:#25D366;color:#fff}}
        .f-social a.fb{{color:#1877F2;border-color:rgba(24,119,242,.3)}} .f-social a.fb:hover{{background:#1877F2;color:#fff}}
        .f-social a.ali{{color:#FF6A00;border-color:rgba(255,106,0,.3)}} .f-social a.ali:hover{{background:#FF6A00;color:#fff}}
        .f-social a.em{{color:#EA4335;border-color:rgba(234,67,53,.3)}} .f-social a.em:hover{{background:#EA4335;color:#fff}}
        .footer-bottom{{text-align:center;padding-top:24px;border-top:1px solid rgba(201,169,110,.08);font-size:.72rem;color:#555}}

        /* LIGHTBOX */
        .lb{{position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,.96);display:none;align-items:center;justify-content:center;cursor:pointer}}
        .lb.show{{display:flex}}
        .lb img{{max-width:92%;max-height:90vh;object-fit:contain}}
        .lb-x{{position:absolute;top:24px;right:28px;color:#fff;font-size:1.8rem;cursor:pointer}}

        /* RESPONSIVE */
        @media(max-width:1024px){{
            .nav{{padding:14px 28px}}.sec{{padding:70px 28px}}
            .catalog-grid{{grid-template-columns:repeat(3,1fr)}}
            .bs-grid{{grid-template-columns:repeat(2,1fr)}}
            .stats-inner{{grid-template-columns:repeat(2,1fr)}}
            .footer-inner{{grid-template-columns:repeat(2,1fr)}}
            .cli-grid{{grid-template-columns:repeat(2,1fr)}}
            .rev-grid{{grid-template-columns:repeat(2,1fr)}}
            .sc-wrap{{grid-template-columns:1fr}}
        }}
        @media(max-width:768px){{
            .nav{{padding:12px 20px}}
            .nav-links{{position:fixed;top:0;right:-100%;width:80%;height:100vh;background:var(--black2);flex-direction:column;justify-content:center;gap:28px;transition:right .4s ease;z-index:101}}
            .nav-links.open{{right:0}}
            .hamburger{{display:flex}}
            .sec{{padding:56px 18px}}
            .catalog-grid{{grid-template-columns:repeat(2,1fr);gap:12px}}
            .contact-wrap{{grid-template-columns:1fr;gap:36px}}
            .stats-inner{{grid-template-columns:repeat(2,1fr);gap:20px}}
            .footer-inner{{grid-template-columns:1fr;gap:24px}}
            .fac-grid{{grid-template-columns:1fr}}
            .fac-grid .g-item:first-child{{grid-column:span 1}}
            .cli-grid{{grid-template-columns:1fr}}
            .rev-grid{{grid-template-columns:1fr}}
            .cat-bar{{gap:4px}}.cat-btn{{padding:7px 14px;font-size:.65rem}}
            .c-row{{grid-template-columns:1fr}}
            .ship-cert{{padding:56px 18px}}
            .bs-grid{{grid-template-columns:1fr 1fr}}
        }}
        @media(max-width:480px){{
            .catalog-grid{{grid-template-columns:1fr 1fr;gap:10px}}
            .p-body{{padding:12px 14px}}
            .p-body h3{{font-size:.75rem}}
            .bs-grid{{grid-template-columns:1fr}}
        }}
    </style>
</head>
<body>

<!-- NAV -->
<nav class="nav" id="navbar">
    <a href="#" class="nav-logo"><img src="{I['logo']}" alt="Sundays"></a>
    <div class="nav-links" id="navLinks">
        <a href="#bestsellers">Best Sellers</a>
        <a href="#factory">Factory</a>
        <a href="#clients">Clients</a>
        <a href="blog.html">Blog</a>
        <a href="#products">Products</a>
        <a href="#contact" class="nav-cta">Get Quote</a>
    </div>
    <div class="hamburger" id="hamburger"><span></span><span></span><span></span></div>
</nav>

<!-- HERO SLIDER -->
<section class="hero-slider" id="heroSlider">
    <div class="slides" id="slides">
        <div class="slide"><img src="{I['hero3']}" alt="Customized Pool Table"></div>
        <div class="slide"><img src="{I['hero4']}" alt="SDAiS Platinum Billiard Balls"></div>
        <div class="slide"><img src="{I['hero5']}" alt="Generation 4 Pool Table - Blue"></div>
        <div class="slide"><img src="{I['hero6']}" alt="Generation 4 Pool Table - Gray"></div>
        <div class="slide"><img src="{I['hero7']}" alt="Customized Pool Table - 8ft 9ft"></div>
    </div>
    <button class="slider-btn slider-prev" onclick="slideMove(-1)"><i class="fas fa-chevron-left"></i></button>
    <button class="slider-btn slider-next" onclick="slideMove(1)"><i class="fas fa-chevron-right"></i></button>
    <div class="slider-dots" id="sliderDots">
        <span class="slider-dot active" onclick="slideTo(0)"></span>
        <span class="slider-dot" onclick="slideTo(1)"></span>
        <span class="slider-dot" onclick="slideTo(2)"></span>
        <span class="slider-dot" onclick="slideTo(3)"></span>
        <span class="slider-dot" onclick="slideTo(4)"></span>
    </div>
</section>

<!-- STATS -->
<div class="stats">
    <div class="stats-inner">
        <div><div class="stat-n">19+</div><div class="stat-l">Years Experience</div></div>
        <div><div class="stat-n">50+</div><div class="stat-l">Countries Exported</div></div>
        <div><div class="stat-n">10,000+</div><div class="stat-l">Tables Per Year</div></div>
        <div><div class="stat-n">8,000</div><div class="stat-l">m&sup2; Factory</div></div>
    </div>
</div>

<!-- BEST SELLERS -->
<section class="sec bestsellers" id="bestsellers">
    <div class="sec-head">
        <div class="sec-tag">Best Sellers</div>
        <h2 class="sec-title">Our Most Popular Models</h2>
        <p class="sec-desc">Championship-grade tables trusted by clubs and venues worldwide.</p>
        <div class="gold-bar"></div>
    </div>
    <div class="bs-grid">
        <div class="bs-item" onclick="openLB(this)"><img src="{I['best1']}" alt="Professional Snooker Table"><div class="bs-label">Professional Club Snooker</div></div>
        <div class="bs-item" onclick="openLB(this)"><img src="{I['best2']}" alt="Sundays Tournament Table"><div class="bs-label">Tournament Pool Table</div></div>
        <div class="bs-item" onclick="openLB(this)"><img src="{I['best3']}" alt="Sundays Competition Table"><div class="bs-label">Competition Series</div></div>
        <div class="bs-item" onclick="openLB(this)"><img src="{I['best4']}" alt="Classic Gold-Leg Snooker"><div class="bs-label">Classic Gold-Leg Snooker</div></div>
    </div>
</section>

<!-- FACTORY -->
<section class="sec factory" id="factory">
    <div class="sec-head">
        <div class="sec-tag">Our Factory</div>
        <h2 class="sec-title">8,000 m&sup2; of Craftsmanship</h2>
        <p class="sec-desc">From raw timber to finished tables &mdash; everything under one roof.</p>
        <div class="gold-bar"></div>
    </div>
    <div class="fac-grid">
        <div class="g-item" onclick="openLB(this)"><img src="{I['fac4']}" alt="Factory panorama"><div class="g-caption">Factory Panorama &mdash; 8,000 m&sup2;</div></div>
        <div class="g-item" onclick="openLB(this)"><img src="{I['fac1']}" alt="Wood processing"><div class="g-caption">Solid Hardwood Processing</div></div>
        <div class="g-item" onclick="openLB(this)"><img src="{I['fac2']}" alt="Table legs production"><div class="g-caption">Mass Production &mdash; Table Legs</div></div>
        <div class="g-item" onclick="openLB(this)"><img src="{I['fac3']}" alt="Leg castings"><div class="g-caption">Precision Leg Casting</div></div>
        <div class="g-item" onclick="openLB(this)"><img src="{I['cli6']}" alt="Production line"><div class="g-caption">Mass Production &mdash; Gold Legs</div></div>
    </div>
</section>

<!-- CLIENT PARTNERSHIPS -->
<section class="sec clients" id="clients">
    <div class="sec-head">
        <div class="sec-tag">Global Partners</div>
        <h2 class="sec-title">Trusted by Clients Worldwide</h2>
        <p class="sec-desc">Building lasting partnerships across 50+ countries.</p>
        <div class="gold-bar"></div>
    </div>
    <div class="cli-grid">
        <div class="g-item" onclick="openLB(this)"><img src="{I['cli1']}" alt="European clients at SDAiS showroom"><div class="g-caption">European Partners &mdash; Showroom Visit</div></div>
        <div class="g-item" onclick="openLB(this)"><img src="{I['cli2']}" alt="Trade show meeting"><div class="g-caption">Trade Show &mdash; Industry Exhibition</div></div>
        <div class="g-item" onclick="openLB(this)"><img src="{I['cli3']}" alt="Contract signing"><div class="g-caption">Signing Partnership Agreement</div></div>
        <div class="g-item" onclick="openLB(this)"><img src="{I['cli4']}" alt="Container loading"><div class="g-caption">Container Loading &mdash; Ready to Ship</div></div>
        <div class="g-item" onclick="openLB(this)"><img src="{I['cli5']}" alt="African clients at SDAiS"><div class="g-caption">African Partners &mdash; Factory Tour</div></div>
        <div class="g-item" onclick="openLB(this)"><img src="{I['fac5']}" alt="Showroom with clients"><div class="g-caption">Showroom Visit &mdash; Client Meeting</div></div>
    </div>
</section>

<!-- SHIPPING & CERTIFICATES -->
<div class="ship-cert">
    <div class="sc-wrap">
        <div class="sc-box">
            <h3>Shipping &amp; Logistics</h3>
            <img src="{I['ship']}" alt="Package and Shipment" onclick="openLB(this.parentElement)">
        </div>
        <div class="sc-box">
            <h3>Certifications</h3>
            <img src="{I['cert']}" alt="Certificates" onclick="openLB(this.parentElement)">
        </div>
    </div>
</div>

<!-- PRODUCTS CATALOG -->
<section class="sec catalog" id="products">
    <div class="sec-head">
        <div class="sec-tag">Product Catalog</div>
        <h2 class="sec-title">{total}+ Products, {num_cats} Categories</h2>
        <p class="sec-desc">Browse our complete range. Click any product for details on Alibaba.</p>
        <div class="gold-bar"></div>
    </div>
    <div class="cat-bar">{cat_buttons}</div>
    <div class="product-count" id="productCount">Showing {default_count} of {total} products</div>
    <div class="catalog-grid" id="catalogGrid">
{product_cards}
    </div>
</section>

<!-- GLOBAL PRESENCE -->
<section class="sec global" style="background:var(--black2)">
    <div class="sec-head">
        <div class="sec-tag">Global Presence</div>
        <h2 class="sec-title">Serving Markets <span style="color:var(--gold)">Globally</span></h2>
        <p class="sec-desc">Over 19 years of expertise in meeting the quality standards of various international markets.</p>
        <div class="gold-bar"></div>
    </div>
    <div style="max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(4,1fr);gap:30px;text-align:center">
        <div><i class="fas fa-flag-usa" style="font-size:2.5rem;color:var(--gold);margin-bottom:15px"></i><h4 style="font-family:var(--ff-h);font-size:1.1rem;margin-bottom:10px">North America</h4><p style="font-size:.8rem;color:var(--gray)">Top supplier for clubs in USA & Canada. Compliance with local wood standards.</p></div>
        <div><i class="fas fa-euro-sign" style="font-size:2.5rem;color:var(--gold);margin-bottom:15px"></i><h4 style="font-family:var(--ff-h);font-size:1.1rem;margin-bottom:10px">Europe</h4><p style="font-size:.8rem;color:var(--gray)">Partnered with distributors in UK, Spain, France, and Germany. CE certified components.</p></div>
        <div><i class="fas fa-mosque" style="font-size:2.5rem;color:var(--gold);margin-bottom:15px"></i><h4 style="font-family:var(--ff-h);font-size:1.1rem;margin-bottom:10px">Middle East</h4><p style="font-size:.8rem;color:var(--gray)">Supplying luxury hotels and clubs in UAE, Saudi Arabia, and Qatar.</p></div>
        <div><i class="fas fa-globe-asia" style="font-size:2.5rem;color:var(--gold);margin-bottom:15px"></i><h4 style="font-family:var(--ff-h);font-size:1.1rem;margin-bottom:10px">Oceania & Asia</h4><p style="font-size:.8rem;color:var(--gray)">Established network in Australia and Southeast Asia. Built for tropical climates.</p></div>
    </div>
</section>

<!-- LATEST FROM BLOG -->
<section class="sec blog-preview">
    <div class="sec-head">
        <div class="sec-tag">Insights</div>
        <h2 class="sec-title">Latest from <span style="color:var(--gold)">Our Blog</span></h2>
        <p class="sec-desc">Expert guides and factory updates to help your billiard business grow.</p>
        <div class="gold-bar"></div>
    </div>
    <div style="max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:30px">
        <a href="blog-buying-guide.html" style="background:var(--black2);border:1px solid rgba(201,169,110,.1);border-radius:12px;overflow:hidden;transition:var(--ease);display:block">
            <img src="https://sc02.alicdn.com/kf/A5f9ebfe00b9b4b7080ed6893b0cd509cC.png" alt="Billiard buying guide" style="width:100%;height:180px;object-fit:cover">
            <div style="padding:20px"><div style="font-size:.65rem;color:var(--gold);margin-bottom:8px">BUYING GUIDE</div><h4 style="font-family:var(--ff-h);font-size:1rem;line-height:1.4;margin-bottom:10px">Complete Commercial Billiard Table Buying Guide</h4><p style="font-size:.78rem;color:var(--gray)">Learn what separates a competition-grade table from a consumer model...</p></div>
        </a>
        <a href="blog-sourcing-china.html" style="background:var(--black2);border:1px solid rgba(201,169,110,.1);border-radius:12px;overflow:hidden;transition:var(--ease);display:block">
            <img src="https://sc02.alicdn.com/kf/A74832d556f3a41f18a32fc38e57263413.png" alt="Sourcing billiard tables from China" style="width:100%;height:180px;object-fit:cover">
            <div style="padding:20px"><div style="font-size:.65rem;color:var(--gold);margin-bottom:8px">FACTORY SOURCING</div><h4 style="font-family:var(--ff-h);font-size:1rem;line-height:1.4;margin-bottom:10px">How to Source Billiard Tables from China: Step-by-Step</h4><p style="font-size:.78rem;color:var(--gray)">MOQ negotiation, quality inspection checklists, and logistics tips...</p></div>
        </a>
        <a href="blog-sustainability.html" style="background:var(--black2);border:1px solid rgba(201,169,110,.1);border-radius:12px;overflow:hidden;transition:var(--ease);display:block">
            <img src="https://sc02.alicdn.com/kf/A4bfde35e22454ae6ad12fd00ced0ebe8C.png" alt="Sustainability in Manufacturing" style="width:100%;height:180px;object-fit:cover">
            <div style="padding:20px"><div style="font-size:.65rem;color:var(--gold);margin-bottom:8px">SUSTAINABILITY</div><h4 style="font-family:var(--ff-h);font-size:1rem;line-height:1.4;margin-bottom:10px">Sustainable Billiard Manufacturing: Our Commitment</h4><p style="font-size:.78rem;color:var(--gray)">How Sundays Billiard is reducing waste and using eco-friendly materials...</p></div>
        </a>
    </div>
    <div style="text-align:center;margin-top:40px"><a href="blog.html" class="nav-cta" style="border:1px solid var(--gold);padding:12px 30px;color:var(--gold);font-weight:600;text-transform:uppercase;font-size:.75rem">View All Articles</a></div>
</section>

<!-- CONTACT -->

<section class="sec contact" id="contact">
    <div class="sec-head">
        <div class="sec-tag">Get In Touch</div>
        <h2 class="sec-title">Start Your Order Today</h2>
        <p class="sec-desc">1 table or 1,000 &mdash; competitive quote within 24 hours.</p>
        <div class="gold-bar"></div>
    </div>
    <div class="contact-wrap">
        <div>
            <div class="c-block"><h4>Factory Address</h4><p><i class="fas fa-map-marker-alt"></i>Guangzhou, Guangdong, China</p></div>
            <div class="c-block"><h4>WhatsApp</h4><p><a href="https://wa.me/8618824156040" target="_blank"><i class="fab fa-whatsapp"></i>+86 188 2415 6040</a></p></div>
            <div class="c-block"><h4>Email</h4><p><a href="mailto:sundaysbilliard@hotmail.com"><i class="fas fa-envelope"></i>sundaysbilliard@hotmail.com</a></p></div>
            <div class="c-block"><h4>Alibaba Store</h4><p><a href="https://gzsundays.en.alibaba.com/" target="_blank"><i class="fas fa-store"></i>gzsundays.en.alibaba.com</a></p></div>
            <div class="c-block"><h4>Business Hours</h4><p><i class="fas fa-clock"></i>Mon &ndash; Sat: 9:00 AM &ndash; 6:00 PM (GMT+8)</p></div>
        </div>
        <form class="c-form" id="inquiryForm" action="https://formsubmit.co/sundaysbilliard@hotmail.com" method="POST">
            <input type="hidden" name="_subject" value="New Inquiry from Sundays Billiard Website">
            <input type="hidden" name="_next" value="https://james1730.github.io/#contact">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="_template" value="table">
            <input type="text" name="_honey" style="display:none">
            <div class="c-row"><input type="text" name="name" placeholder="Your Name *" required><input type="email" name="email" placeholder="Email *" required></div>
            <div class="c-row"><input type="text" name="company" placeholder="Company"><input type="tel" name="phone" placeholder="Phone / WhatsApp"></div>
            <input type="text" name="country" placeholder="Country / Region" style="width:100%;padding:13px 18px;border:1px solid rgba(201,169,110,.2);border-radius:6px;background:rgba(255,255,255,.04);color:var(--white);font-family:var(--ff-b);font-size:.85rem;margin-bottom:0">
            <select name="product_interest"><option value="" disabled selected>Product Interest</option><option>Pool Tables</option><option>Snooker Tables</option><option>Coin-Operated Tables</option><option>Multi-function Tables</option><option>Glass Pool Tables</option><option>MDF Pool Tables</option><option>Chinese Billiard Tables</option><option>Billiard Accessories</option><option>Complete Club Setup</option><option>OEM / ODM Project</option></select>
            <textarea name="message" placeholder="Requirements: quantity, specs, destination country..." rows="4"></textarea>
            <button type="submit" id="submitBtn" class="btn btn-gold" style="display:inline-block;padding:15px 40px;font-family:var(--ff-b);font-size:.78rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;cursor:pointer;transition:var(--ease);border:none;background:var(--gold);color:var(--black);width:100%">Send Inquiry</button>
            <p style="text-align:center;margin-top:12px;font-size:.75rem;color:var(--gray)">Or contact us directly via <a href="https://wa.me/8618824156040" target="_blank" style="color:#25D366;font-weight:600">WhatsApp</a> &bull; <a href="mailto:sundaysbilliard@hotmail.com" style="color:var(--gold);font-weight:600">Email</a></p>
        </form>
        <!-- Success Modal -->
        <div id="successModal" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.8);z-index:10000;align-items:center;justify-content:center">
            <div style="background:var(--black3);border:1px solid var(--gold);border-radius:16px;padding:50px;max-width:500px;text-align:center">
                <div style="font-size:3rem;margin-bottom:16px">&#10003;</div>
                <h3 style="font-family:var(--ff-h);color:var(--gold);font-size:1.5rem;margin-bottom:12px">Inquiry Sent!</h3>
                <p style="color:var(--gray-light);font-size:.9rem;line-height:1.7">Thank you for your interest. Our team will reply within <strong style="color:var(--gold)">24 hours</strong>.</p>
                <p style="color:var(--gray);font-size:.8rem;margin-top:12px">You can also reach us on <a href="https://wa.me/8618824156040" target="_blank" style="color:#25D366">WhatsApp</a> for faster response.</p>
                <button onclick="document.getElementById('successModal').style.display='none'" style="margin-top:24px;padding:12px 36px;background:var(--gold);color:var(--black);border:none;border-radius:8px;font-weight:600;cursor:pointer;font-size:.85rem">OK</button>
            </div>
        </div>
    </div>
</section>

<!-- CLIENT REVIEWS -->
<section class="reviews">
    <div class="sec-head">
        <div class="sec-tag">Client Reviews</div>
        <h2 class="sec-title">What Our Clients <span style="color:var(--gold)">Say</span></h2>
        <p class="sec-desc">Real feedback from clubs, distributors and wholesalers who trust Sundays for their billiard tables.</p>
    </div>
    <div class="rev-grid">
        <div class="rev-card">
            <img class="rev-img" src="https://s.alicdn.com/@sc04/kf/Ha836ef46720c4fa2bf64f80b91c39ee8e/Guangzhou-Billiard-Table-Factory-Snooker-Billiard-Tables.jpg_480x480.jpg" alt="Snooker Table">
            <div class="rev-body">
            <div class="rev-quote">&ldquo;</div>
            <div class="rev-stars">&starf;&starf;&starf;&starf;&starf;</div>
            <div class="rev-text">We ordered 30 snooker tables for our club chain. The slate quality is exceptional &mdash; perfectly leveled and consistent across every table. Sundays handled the bulk order flawlessly, delivered on time, and even helped with custom logo engraving. Highly recommended for commercial projects.</div>
            <div class="rev-author">
                <div class="rev-avatar">DM</div>
                <div><div class="rev-name">David Mitchell</div><div class="rev-country">&#127468;&#127463; United Kingdom</div></div>
            </div>
            </div>
        </div>
        <div class="rev-card">
            <img class="rev-img" src="https://sc04.alicdn.com/kf/Hdaf4a29a88b846348a23bf1343e7b237u/Luxury-Pool-Table-Multi-Game-Solid-Wood.png" alt="Gold Armor Pool Table">
            <div class="rev-body">
            <div class="rev-quote">&ldquo;</div>
            <div class="rev-stars">&starf;&starf;&starf;&starf;&starf;</div>
            <div class="rev-text">As a distributor, I&rsquo;ve worked with many factories. Sundays stands out &mdash; their build quality is on par with European brands at half the cost. The solid wood craftsmanship on their Gold Armor series is remarkable. Already placed our third repeat order.</div>
            <div class="rev-author">
                <div class="rev-avatar">JV</div>
                <div><div class="rev-name">Jean-Pierre Vasquez</div><div class="rev-country">&#127466;&#127480; Spain</div></div>
            </div>
            </div>
        </div>
        <div class="rev-card">
            <img class="rev-img" src="https://s.alicdn.com/@sc04/kf/H918abede96b44376a1be698b1d5bec091/Coin-operated-Billiard-Table-Business-Type-Commercial.png_480x480.jpg" alt="Coin Operated Pool Table">
            <div class="rev-body">
            <div class="rev-quote">&ldquo;</div>
            <div class="rev-stars">&starf;&starf;&starf;&starf;&starf;</div>
            <div class="rev-text">The coin-operated tables we purchased are built like tanks &mdash; heavy-duty, smooth ball return, and the felt quality is excellent. Our entertainment venues have been running them for 2 years with zero maintenance issues. Factory communication was professional throughout.</div>
            <div class="rev-author">
                <div class="rev-avatar">AO</div>
                <div><div class="rev-name">Ahmed Osman</div><div class="rev-country">&#127462;&#127466; UAE</div></div>
            </div>
            </div>
        </div>
        <div class="rev-card">
            <img class="rev-img" src="https://s.alicdn.com/@sc04/kf/H72d7a91052f146ceb65473ec8cdfb7948/Sdais-4G-Pool-Table-Billiard-Table-Colorful.jpg_480x480.jpg" alt="Customized Pool Table">
            <div class="rev-body">
            <div class="rev-quote">&ldquo;</div>
            <div class="rev-stars">&starf;&starf;&starf;&starf;&starf;</div>
            <div class="rev-text">We needed custom-colored pool tables for a hotel project. Sundays matched our RAL color samples perfectly and delivered 15 tables within 45 days. The packaging was impeccable &mdash; not a single scratch after a 40-day sea shipment. Outstanding service from Annie&rsquo;s team.</div>
            <div class="rev-author">
                <div class="rev-avatar">SK</div>
                <div><div class="rev-name">Samuel Kofi</div><div class="rev-country">&#127468;&#127469; Ghana</div></div>
            </div>
            </div>
        </div>
        <div class="rev-card">
            <img class="rev-img" src="https://sc04.alicdn.com/kf/H861546d082364a52aec612a4f00dea6bG/Factory-Wholesale-Crystal-Sdais-Billiard-Balls-5.png" alt="SDAiS Billiard Balls">
            <div class="rev-body">
            <div class="rev-quote">&ldquo;</div>
            <div class="rev-stars">&starf;&starf;&starf;&starf;&starf;</div>
            <div class="rev-text">The SDAiS Platinum billiard balls are a game-changer. Perfect roundness, consistent weight, and the colors stay vibrant even after months of heavy use. We&rsquo;ve now switched our entire stock to SDAiS. Great value compared to Belgian brands.</div>
            <div class="rev-author">
                <div class="rev-avatar">RN</div>
                <div><div class="rev-name">Roberto Nascimento</div><div class="rev-country">&#127463;&#127479; Brazil</div></div>
            </div>
            </div>
        </div>
        <div class="rev-card">
            <img class="rev-img" src="https://s.alicdn.com/@sc04/kf/Hd82ea5034c5a4e4385d6d1f60bc312cdt/Indoor-Simple-Standard-7ft-8ft-9ft-Multi.png_480x480.jpg" alt="Multi-function Pool Table">
            <div class="rev-body">
            <div class="rev-quote">&ldquo;</div>
            <div class="rev-stars">&starf;&starf;&starf;&starf;&starf;</div>
            <div class="rev-text">Visited the Sundays factory in Guangzhou &mdash; truly impressive. 8,000 m&sup2; facility with modern equipment and strict quality control. Ordered a full container of multi-function tables for our Australian market. ISO and SGS certified, exactly what our importers require.</div>
            <div class="rev-author">
                <div class="rev-avatar">MC</div>
                <div><div class="rev-name">Michael Chen</div><div class="rev-country">&#127462;&#127482; Australia</div></div>
            </div>
            </div>
        </div>
    </div>
</section>

<!-- FAQ -->
<section class="faq-section">
    <div class="sec-head">
        <div class="sec-tag">FAQ</div>
        <h2 class="sec-title">Frequently Asked <span style="color:var(--gold)">Questions</span></h2>
    </div>
    <div class="faq-wrap">
        <div class="faq-item">
            <div class="faq-q" onclick="toggleFaq(this)">What is the MOQ (Minimum Order Quantity)?<span class="faq-icon">+</span></div>
            <div class="faq-a"><p>Our standard MOQ is 1 set for sample orders. For bulk production orders, we recommend a minimum of 5 sets per model to optimize shipping costs. Mixed models are welcome in the same container.</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-q" onclick="toggleFaq(this)">What materials are your billiard tables made of?<span class="faq-icon">+</span></div>
            <div class="faq-a"><p>We use premium solid hardwood (ash, oak, mahogany) for frames and legs, natural slate from Brazil or China (25mm&ndash;50mm thickness) for playing surfaces, and tournament-grade wool/nylon blend cloth. All hardware is stainless steel or heavy-duty zinc alloy.</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-q" onclick="toggleFaq(this)">Can you customize tables with our brand logo and colors?<span class="faq-icon">+</span></div>
            <div class="faq-a"><p>Absolutely! We offer full OEM/ODM customization including custom wood finishes (RAL color matching), logo engraving on rails and legs, branded cloth printing, and custom packaging with your brand identity. Send us your design brief and we&rsquo;ll provide a free mockup.</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-q" onclick="toggleFaq(this)">What is the production lead time?<span class="faq-icon">+</span></div>
            <div class="faq-a"><p>Standard models: 15&ndash;25 days. Customized orders: 30&ndash;45 days depending on complexity. Sample orders can be expedited to 7&ndash;10 days. We provide weekly production progress photos and updates.</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-q" onclick="toggleFaq(this)">How do you handle shipping and packaging?<span class="faq-icon">+</span></div>
            <div class="faq-a"><p>Tables are disassembled and packed with multi-layer protection: EPE foam wrapping, reinforced cardboard, corner protectors, and wooden crating for slate. We support FOB Guangzhou, CIF, and door-to-door delivery. A 40ft container fits approximately 16&ndash;20 standard pool tables.</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-q" onclick="toggleFaq(this)">Do you have quality certifications?<span class="faq-icon">+</span></div>
            <div class="faq-a"><p>Yes. Our factory holds ISO 9001:2015 quality management certification, SGS inspection reports, SMETA ethical trade audit, and OEKO-TEX 100 certification for cloth materials. We welcome third-party inspections and factory audits.</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-q" onclick="toggleFaq(this)">What is your warranty and after-sales policy?<span class="faq-icon">+</span></div>
            <div class="faq-a"><p>We offer a 3-year warranty on frame and slate, 1-year warranty on cloth and accessories. Spare parts are available for purchase at any time. Our after-sales team responds within 24 hours and provides video guidance for installation and maintenance.</p></div>
        </div>
        <div class="faq-item">
            <div class="faq-q" onclick="toggleFaq(this)">Can I visit your factory before placing an order?<span class="faq-icon">+</span></div>
            <div class="faq-a"><p>Of course! We welcome factory visits and can arrange pickup from Guangzhou Baiyun Airport or Guangzhou South Railway Station. Our 8,000 m&sup2; showroom displays over 50 table models. Contact us to schedule a visit &mdash; we host international buyers regularly.</p></div>
        </div>
    </div>
</section>

<!-- FOOTER -->
<footer class="footer">
    <div class="footer-inner">
        <div class="footer-brand">
            <img src="{I['logo']}" alt="Sundays" style="height:36px">
            <p>Professional billiard table manufacturer based in Guangzhou, China. Serving the global market since 2005.</p>
            <div class="f-social">
                <a class="wa" href="https://wa.me/8618824156040" target="_blank"><i class="fab fa-whatsapp"></i></a>
                <a class="fb" href="https://www.facebook.com/sundaysbilliard" target="_blank"><i class="fab fa-facebook-f"></i></a>
                <a class="ali" href="https://gzsundays.en.alibaba.com/" target="_blank"><i class="fas fa-store"></i></a>
                <a class="em" href="mailto:sundaysbilliard@hotmail.com"><i class="fas fa-envelope"></i></a>
            </div>
        </div>
        <div class="footer-col"><h4>Products</h4><a href="#products">Pool Tables</a><a href="#products">Snooker Tables</a><a href="#products">Coin-Operated</a><a href="#products">Accessories</a></div>
        <div class="footer-col"><h4>Company</h4><a href="#bestsellers">Best Sellers</a><a href="#factory">Factory Tour</a><a href="#clients">Client Partners</a><a href="blog.html">Blog</a><a href="#contact">Contact</a></div>
        <div class="footer-col"><h4>Services</h4><a href="#contact">OEM Manufacturing</a><a href="#contact">ODM Design</a><a href="#contact">Custom Branding</a><a href="#contact">Club Setup</a></div>
    </div>
    <div class="footer-bottom">&copy; 2025 Sundays Billiard Tables. All Rights Reserved. Guangzhou Wanjin Sports Equipment Co., Ltd.</div>
</footer>

<!-- LIGHTBOX -->
<div class="lb" id="lb" onclick="closeLB()"><span class="lb-x">&times;</span><img id="lbImg" src="" alt=""></div>

<script>
// NAV
window.addEventListener('scroll',function(){{document.getElementById('navbar').classList.toggle('scrolled',scrollY>60)}});
document.getElementById('hamburger').addEventListener('click',function(){{document.getElementById('navLinks').classList.toggle('open')}});
document.querySelectorAll('.nav-links a').forEach(function(a){{a.addEventListener('click',function(){{document.getElementById('navLinks').classList.remove('open')}})}});

// HERO SLIDER
var slideIdx=0, slideCount=5, autoSlide;
function slideTo(n){{slideIdx=n;document.getElementById('slides').style.transform='translateX(-'+(slideIdx*100)+'%)';document.querySelectorAll('.slider-dot').forEach(function(d,i){{d.classList.toggle('active',i===slideIdx)}})}}
function slideMove(d){{slideTo((slideIdx+d+slideCount)%slideCount)}}
function startAuto(){{autoSlide=setInterval(function(){{slideMove(1)}},4500)}}
function stopAuto(){{clearInterval(autoSlide)}}
document.getElementById('heroSlider').addEventListener('mouseenter',stopAuto);
document.getElementById('heroSlider').addEventListener('mouseleave',startAuto);
startAuto();

// LIGHTBOX
function openLB(el){{var img=el.querySelector('img');if(img){{document.getElementById('lbImg').src=img.src;document.getElementById('lb').classList.add('show');document.body.style.overflow='hidden'}}}}
function closeLB(){{document.getElementById('lb').classList.remove('show');document.body.style.overflow=''}}
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeLB()}});

// FORM - Formspree AJAX submit
var iqForm=document.getElementById('inquiryForm');
if(iqForm){{iqForm.addEventListener('submit',function(e){{
    e.preventDefault();
    var btn=document.getElementById('submitBtn');
    btn.textContent='Sending...';btn.disabled=true;
    var data=new FormData(iqForm);
    fetch('https://formsubmit.co/ajax/sundaysbilliard@hotmail.com',{{method:'POST',body:data,headers:{{'Accept':'application/json'}}}})
    .then(function(r){{
        if(r.ok){{
            document.getElementById('successModal').style.display='flex';
            iqForm.reset();
        }}else{{
            alert('Something went wrong. Please try WhatsApp or email instead.');
        }}
        btn.textContent='Send Inquiry';btn.disabled=false;
    }})
    .catch(function(){{
        alert('Network error. Please try WhatsApp or email instead.');
        btn.textContent='Send Inquiry';btn.disabled=false;
    }});
}});}}

// PRODUCT FILTER
function filterCat(cat,btn){{
    document.querySelectorAll('.cat-btn').forEach(function(b){{b.classList.remove('active')}});
    btn.classList.add('active');
    var cards=document.querySelectorAll('.p-card');
    var count=0;
    for(var i=0;i<cards.length;i++){{
        if(cat==='all'||cards[i].getAttribute('data-cat')===cat){{cards[i].classList.remove('hidden');count++;}}
        else{{cards[i].classList.add('hidden');}}
    }}
    document.getElementById('productCount').textContent='Showing '+count+' of {total} products';
}}
</script>

<!-- WHATSAPP FLOATING BUTTON -->
<style>
#waFloat{{position:fixed;z-index:9999;cursor:pointer;user-select:none;text-decoration:none}}
#waFloat .wa-circle{{width:68px;height:68px;border-radius:18px;background:#25D366;display:flex;align-items:center;justify-content:center;transition:transform .2s;animation:wa-bob 3s ease-in-out infinite}}
#waFloat:hover .wa-circle{{transform:scale(1.12);filter:drop-shadow(0 10px 28px rgba(37,211,102,.75))}}
#waFloat .wa-tooltip{{position:absolute;right:78px;top:50%;transform:translateY(-50%);background:#fff;color:#111;font-size:.82rem;font-weight:700;padding:7px 14px;border-radius:8px;white-space:nowrap;opacity:0;pointer-events:none;transition:opacity .2s;box-shadow:0 2px 10px rgba(0,0,0,.12)}}
#waFloat:hover .wa-tooltip{{opacity:1}}
@keyframes wa-bob{{0%,100%{{filter:drop-shadow(0 6px 18px rgba(37,211,102,.5))}}50%{{filter:drop-shadow(0 10px 32px rgba(37,211,102,.8))}}}}
</style>
<a id="waFloat" href="https://wa.me/8618824156040?text=Hello%20Sundays!%20I%20am%20interested%20in%20your%20billiard%20products." target="_blank">
    <div class="wa-circle">
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24" fill="white"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
    </div>
    <span class="wa-tooltip">Chat on WhatsApp</span>
</a>
<script>
// FAQ TOGGLE
function toggleFaq(el){{var item=el.parentElement;item.classList.toggle('open')}}

// WHATSAPP FLOAT - bounce around screen like screensaver
var waBtn=document.getElementById('waFloat');
var waX=window.innerWidth-100, waY=window.innerHeight-100;
var waVX=(Math.random()>0.5?1:-1)*(0.8+Math.random()*0.8);
var waVY=(Math.random()>0.5?1:-1)*(0.8+Math.random()*0.8);
var waPaused=false;
function waAnimate(){{
    if(!waPaused){{
        waX+=waVX; waY+=waVY;
        var maxX=window.innerWidth-68, maxY=window.innerHeight-68;
        if(waX<=0){{waX=0;waVX=Math.abs(waVX)}}
        if(waX>=maxX){{waX=maxX;waVX=-Math.abs(waVX)}}
        if(waY<=0){{waY=0;waVY=Math.abs(waVY)}}
        if(waY>=maxY){{waY=maxY;waVY=-Math.abs(waVY)}}
        waBtn.style.left=waX+'px';
        waBtn.style.top=waY+'px';
    }}
    requestAnimationFrame(waAnimate);
}}
waBtn.addEventListener('mouseenter',function(){{waPaused=true}});
waBtn.addEventListener('mouseleave',function(){{waPaused=false}});
waAnimate();
</script>

</body>
</html>''')

print(f"Done! index.html built successfully")
print(f"Products: {total}")
print(f"Categories: {num_cats}")

import os
print(f"File size: {os.path.getsize('index.html')/1024:.0f} KB")
