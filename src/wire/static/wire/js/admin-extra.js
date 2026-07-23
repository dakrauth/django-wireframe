"use strict";

document.addEventListener("DOMContentLoaded", (event) => {
    document.querySelectorAll("textarea.monospace-textarea").forEach((e) => {
        e.value = JSON.stringify(JSON.parse(e.value), null, 4);
    });
});
