// Auto-expand textarea functionality for EduChat
(function() {
    function autoExpandTextarea() {
        const textareas = document.querySelectorAll('.auto-expand-textarea');
        
        textareas.forEach(textarea => {
            // Reset height to get accurate scrollHeight
            textarea.style.height = '24px';
            
            // Set height based on content
            const scrollHeight = textarea.scrollHeight;
            const maxHeight = parseInt(window.getComputedStyle(textarea).maxHeight);
            
            if (scrollHeight > 24) {
                if (scrollHeight <= maxHeight) {
                    textarea.style.height = scrollHeight + 'px';
                    textarea.style.overflowY = 'hidden';
                } else {
                    textarea.style.height = maxHeight + 'px';
                    textarea.style.overflowY = 'auto';
                }
            } else {
                textarea.style.overflowY = 'hidden';
            }
        });
    }

    // Run on page load
    document.addEventListener('DOMContentLoaded', function() {
        autoExpandTextarea();
        
        // Attach event listeners
        document.addEventListener('input', function(e) {
            if (e.target.classList.contains('auto-expand-textarea')) {
                autoExpandTextarea();
            }
        });
        
        // Watch for changes (for Reflex state updates)
        const observer = new MutationObserver(autoExpandTextarea);
        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['value']
        });
    });

    // Also run periodically to catch any missed updates
    setInterval(autoExpandTextarea, 100);
})();
