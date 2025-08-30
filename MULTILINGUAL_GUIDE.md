# Multilingual Structure Guide - Lumy TV

## Overview
This website supports multiple languages with SEO-friendly separate HTML files for each language.

## Current Languages
- **Portuguese (PT)** - Default language (root directory)
- **English (EN)** - Located in `/en/` subdirectory

## Directory Structure
```
/
├── index.html (Portuguese - default)
├── contact/index.html (Portuguese)
├── pricing/index.html (Portuguese)
├── partners/index.html (Portuguese)
├── use-cases/index.html (Portuguese)
└── en/
    ├── index.html (English)
    ├── contact/index.html (English)
    ├── pricing/index.html (English)
    ├── partners/index.html (English)
    └── use-cases/index.html (English)
```

## SEO Implementation
- Each page includes proper `hreflang` tags pointing to all language versions
- English is set as the default language (`hreflang="x-default"`)
- Sitemap.xml includes all language versions with proper hreflang annotations
- Each language has its own canonical URLs

## Language Switcher
- Simple HTML-based language switcher in the navigation
- No JavaScript dependency for SEO efficiency
- Styled with CSS for consistent appearance

## Adding New Languages
To add a new language (e.g., Spanish):

1. Create new directory: `/es/`
2. Copy all HTML files from `/en/` to `/es/`
3. Translate all content in the new files
4. Update `hreflang` tags in ALL existing files to include the new language
5. Update sitemap.xml to include the new language pages
6. Update language switcher in all pages

## Image Placeholders
All images have been replaced with descriptive placeholders:
- Main hero image: Dashboard interface mockup
- Feature icons: Various functional icons (CMS, Automation, IFTTT, etc.)
- Use case images: Industry-specific imagery descriptions

## Technical Notes
- JavaScript automatically detects language for pricing format and theme toggle text
- CSS includes styles for language switcher and image placeholders
- All pages maintain the same functionality across languages