document.addEventListener('DOMContentLoaded', function() {
    const textarea = document.querySelector('.autoResize');
    textarea.style.height = 'auto';  // Reset the height to auto to calculate the new height properly
    textarea.style.height = (textarea.scrollHeight + 4) + 'px';  // Set the height to the scrollHeight
    textarea.addEventListener('input', function() {
        this.style.height = 'auto';  // Reset the height to auto to calculate the new height properly
        this.style.height = (this.scrollHeight + 4) + 'px';  // Set the height to the scrollHeight
    });
});