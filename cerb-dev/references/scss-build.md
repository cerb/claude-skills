
`features/cerberusweb.core/resources/css/cerb.css` is a **generated artifact**. Never edit it directly — your changes get blown away the next time someone rebuilds.

## Source Layout

```
install/extras/developers/css/cerb.css/
├── cerb.scss                # entry point — @imports each partial
├── theme/
│   └── cerb-theme.scss      # color tokens (--cerb-color-*), light + .dark
├── layout/
│   ├── cerb-base.scss       # element resets, base BUTTON, INPUT, etc.
│   ├── cerb-styles.scss     # most app styles, form-input-icon mixin
│   ├── cerb-cards.scss
│   ├── cerb-login.scss      # login flow shell (.cerb-login-*)
│   └── ...                  # one partial per major UI area
├── icons/glyphicons.scss
└── jquery/...
```

To add a new top-level area, create `layout/cerb-foo.scss` and add `@import "layout/cerb-foo.scss";` to `cerb.scss`.

## Build Command

```bash
composer build-css
```

That's a composer script defined in `composer.json` that runs the Dart Sass build with the correct source and output paths — use it instead of invoking `sass` directly so the paths stay in sync:

```json
"build-css": [
    "sass --no-source-map install/extras/developers/css/cerb.css/cerb.scss features/cerberusweb.core/resources/css/cerb.css"
]
```

Then `composer cache-clear` to drop compiled Smarty templates so updated `<link>` cache-busters take effect.

Dart Sass (`sass` from Homebrew or npm) must be on `PATH` — not old Ruby sass. There's no `package.json` or Gemfile checked in. For iterative work: `sass --watch install/extras/developers/css/cerb.css/cerb.scss:features/cerberusweb.core/resources/css/cerb.css`.

## Inline-SVG Background Images

For icons embedded in CSS (input field icons, button arrows, etc.) prefer data-URI SVGs over PNG assets — they scale crisply and survive dark mode without separate files.

Pattern in `layout/cerb-styles.scss`:

```scss
@mixin form-input-icon-svg($svg) {
    padding: 2px 2px 2px 25px;
    background: url("data:image/svg+xml;utf8,#{$svg}") no-repeat scroll 5px 50% var(--cerb-color-form-input-background);
}

$icon-svg-lock: "<svg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='rgb(136,136,136)' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><rect x='3' y='11' width='18' height='11' rx='2'/><path d='M7 11V7a5 5 0 0 1 10 0v4'/></svg>";

INPUT[type=password] {
    @include form-input-icon-svg($icon-svg-lock);
}
```

Rules:
- **Single-quote SVG attributes** so the outer `url("…")` double-quotes don't collide.
- **Avoid `#` literals** inside the data URI (it's the URL fragment delimiter). Use `rgb(r,g,b)` instead of `#aabbcc`.
- **`<` and `>` don't need encoding** for `image/svg+xml;utf8,...` in modern browsers (Chrome/Firefox/Safari all accept).
- **`currentColor` does *not* inherit** when an SVG is loaded as a `background-image` — it renders in its own context. Hard-code a theme-neutral stroke color, or use a `<mask>` with `background-color`. For *inline* `<svg>` (not background-image), `stroke="currentColor"` works fine.

## Button Reset Pattern

Browsers' native `<button>` chrome (especially Safari's gradient on `:active`) bleeds through unless explicitly killed:

```scss
.my-custom-button {
    appearance: none;
    -webkit-appearance: none;
    -webkit-tap-highlight-color: transparent;
    outline: none;
    /* ... custom background, border, etc. ... */

    &:hover:not(:disabled),
    &:focus:not(:disabled),
    &:active:not(:disabled) {
        background: var(--accent-hover);
        color: #ffffff;
    }

    &:focus-visible:not(:disabled) {
        box-shadow: 0 0 0 3px var(--accent-glow);
    }

    &:disabled {
        background: var(--accent);  /* don't rely on opacity alone */
        color: #ffffff;
        opacity: 0.7;
        cursor: not-allowed;
    }
}
```

Important: `layout/cerb-base.scss` defines a base `BUTTON:hover` that sets `color: var(--cerb-color-button-icon--hover)` (which resolves to blue in dark mode). If your custom hover state only overrides `background` and not `color`, the text will flash blue. Always set both.

For `:disabled`, set `background` explicitly — `opacity: 0.6` alone on a colored button over a contrasting card surface can read as "almost white" in the brief moment between click and navigation.
