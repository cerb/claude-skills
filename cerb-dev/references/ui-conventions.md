# UI Conventions

## Confirmation Dialogs

**Never use the browser-native `confirm()`.** Always use `confirmPopup()` from `libs/devblocks/resources/js/devblocks.js`:

```javascript
confirmPopup(
    'Title',          // dialog title (default: 'Confirm')
    'Are you sure?',  // message body
    function() {      // OK callback
        // proceed
    },
    function() {      // optional Cancel callback
    }
);
```

`confirm()` blocks the browser's main thread, is unstyled, and cannot be used inside iframes on some browsers. `confirmPopup()` is the platform-standard modal.
