# Image Optimization & Carousel Features

This document describes the new image handling features added to the Hugo site for better SEO, performance, and user experience.

## Features Implemented

### 1. Automatic Image Optimization (All Images)

All markdown images are now automatically enhanced with:

- **Responsive Sizing**: Images scale properly on all devices
- **Lazy Loading**: Images load only when needed, improving page load time
- **SEO Optimization**:
  - Structured data (Schema.org ImageObject)
  - Proper alt attributes for accessibility
  - Width/height attributes when available
- **Click-to-Zoom**: Click any image to view it in a lightbox
- **Consistent Styling**: All images have uniform border-radius, shadows, and hover effects

**No changes needed!** All existing markdown images like:
```markdown
![Alt text](/images/my-image.png)
```
Will automatically get these enhancements.

### 2. Image Carousel/Gallery

For multiple related images, you can now create a carousel using the `carousel` shortcode.

#### Basic Usage

```markdown
{{< carousel >}}
![Image 1 alt text](/images/image1.png "Optional caption 1")
![Image 2 alt text](/images/image2.png "Optional caption 2")
![Image 3 alt text](/images/image3.png "Optional caption 3")
{{< /carousel >}}
```

#### Advanced Usage with Parameters

```markdown
{{< carousel autoplay="true" interval="5000" indicators="true" counter="true" >}}
![Image 1](/images/image1.png)
![Image 2](/images/image2.png)
![Image 3](/images/image3.png)
{{< /carousel >}}
```

**Parameters:**
- `autoplay`: Enable automatic slide progression (default: `false`)
- `interval`: Time between slides in milliseconds (default: `5000`)
- `indicators`: Show dot indicators below carousel (default: `true`)
- `counter`: Show "1 / 3" style counter (default: `true`)

#### Carousel Features

- **Navigation**: Previous/Next arrow buttons
- **Indicators**: Clickable dots to jump to specific slides
- **Keyboard Support**: Left/Right arrow keys to navigate
- **Touch/Swipe**: Swipe left/right on mobile devices
- **Autoplay**: Optional automatic progression
- **Accessible**: Full ARIA labels and keyboard navigation
- **Responsive**: Works perfectly on mobile, tablet, and desktop

### 3. Lightbox Functionality

All images (both standalone and in carousels) support click-to-zoom:

- Click any image to view it full-screen
- Click outside the image or press `Escape` to close
- Works on all devices

## Technical Details

### File Structure

```
├── assets/
│   ├── css/
│   │   └── custom-images.css       # All image and carousel styles
│   └── js/
│       └── image-handler.js        # Carousel and lightbox JavaScript
├── layouts/
│   ├── _default/
│   │   ├── baseof.html            # Base template with custom partials
│   │   ├── single.html            # Single page layout
│   │   └── _markup/
│   │       └── render-image.html  # Image render hook (auto-applied)
│   ├── partials/
│   │   ├── custom-head.html       # CSS injection
│   │   └── custom-footer.html     # JS injection
│   └── shortcodes/
│       └── carousel.html          # Carousel shortcode
└── hugo.toml                      # Updated with customCSS and customJS
```

### SEO Benefits

1. **Structured Data**: All images include Schema.org ImageObject markup
2. **Alt Attributes**: Preserved from markdown for screen readers and SEO
3. **Lazy Loading**: Improves Core Web Vitals (LCP, CLS)
4. **Responsive Images**: Proper sizing hints for faster rendering
5. **Semantic HTML**: Uses `<figure>` and `<figcaption>` elements

### Performance Optimizations

1. **Lazy Loading**: Images load only when scrolled into view
2. **Minified Assets**: CSS and JS are minified and fingerprinted
3. **Efficient JavaScript**: No external dependencies, vanilla JS
4. **Reduced Motion Support**: Respects `prefers-reduced-motion`
5. **Intersection Observer**: Modern browser API for efficient lazy loading

### Accessibility

1. **ARIA Labels**: Full support for screen readers
2. **Keyboard Navigation**: All carousel controls accessible via keyboard
3. **Focus Management**: Proper focus indicators
4. **Alt Text**: Preserved and used throughout
5. **Semantic HTML**: Proper use of `<figure>`, `<img>`, `role` attributes

### Browser Support

- **Modern Browsers**: Full feature support (Chrome, Firefox, Safari, Edge)
- **Older Browsers**: Graceful degradation (images still display, just without enhancements)
- **Mobile**: Full touch/swipe support

## Migration Guide

### For Existing Content

**Good news!** No changes needed. All existing markdown images will automatically:
- Be properly sized and styled
- Have lazy loading enabled
- Be clickable for lightbox viewing
- Include proper SEO attributes

### For New Content

#### Single Images (Recommended)
Just use standard markdown:
```markdown
![Descriptive alt text](/images/my-image.png "Optional caption")
```

#### Multiple Related Images
Use the carousel shortcode:
```markdown
{{< carousel >}}
![Image 1](/images/img1.png)
![Image 2](/images/img2.png)
![Image 3](/images/img3.png)
{{< /carousel >}}
```

## Customization

### Styling

To customize image or carousel styles, edit:
```
assets/css/custom-images.css
```

Key CSS classes:
- `.content-image` - All content images
- `.image-carousel` - Carousel container
- `.carousel-slide` - Individual slides
- `.carousel-nav` - Navigation buttons
- `.lightbox` - Lightbox modal

### Behavior

To customize carousel or lightbox behavior, edit:
```
assets/js/image-handler.js
```

## Testing

To test locally:
```bash
hugo server -D
```

Visit your site and:
1. Check that single images are properly styled and clickable
2. Create a test post with a carousel
3. Test navigation (arrows, dots, keyboard, swipe)
4. Test lightbox functionality
5. Check mobile responsiveness

## Google Search Console

After deploying, monitor:
1. **Core Web Vitals**: Should see improvements in LCP (Largest Contentful Paint)
2. **Mobile Usability**: Images should be properly sized
3. **Structured Data**: Check for ImageObject detection
4. **Page Speed**: Should see faster load times

## Questions?

If you have questions about using these features, refer to:
- Hugo Documentation: https://gohugo.io/content-management/shortcodes/
- This file for usage examples
- The CSS/JS files for implementation details
