addEventListener("pageshow", function(event) {
    if (event.persisted) {
        location.reload();
    }
});
if (!hasError) {
    confetti();
}