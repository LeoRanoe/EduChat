// Auto-scroll to bottom when new messages appear with smooth behavior
(function() {
  let lastMessageCount = 0;
  let isUserScrolling = false;
  let scrollTimeout;
  let lastScrollHeight = 0;
  let streamingCheckInterval;
  
  function scrollToBottom(force = false, instant = false) {
    const chatContainer = document.querySelector('[data-chat-container]');
    if (!chatContainer) return;
    
    // Check if user is scrolled near bottom (within 150px for better UX)
    const isNearBottom = chatContainer.scrollHeight - chatContainer.scrollTop - chatContainer.clientHeight < 150;
    
    // Only auto-scroll if user is near bottom or force is true
    if (isNearBottom || force || !isUserScrolling) {
      requestAnimationFrame(() => {
        chatContainer.scrollTo({
          top: chatContainer.scrollHeight,
          behavior: instant ? 'auto' : 'smooth'
        });
      });
    }
  }
  
  // Detect user scrolling
  function handleScroll() {
    const chatContainer = document.querySelector('[data-chat-container]');
    if (!chatContainer) return;
    
    const isAtBottom = chatContainer.scrollHeight - chatContainer.scrollTop - chatContainer.clientHeight < 10;
    
    // If user scrolls to bottom, stop marking as user scrolling
    if (isAtBottom) {
      isUserScrolling = false;
      return;
    }
    
    isUserScrolling = true;
    clearTimeout(scrollTimeout);
    
    // Reset after 1.5 seconds of no scrolling
    scrollTimeout = setTimeout(() => {
      isUserScrolling = false;
    }, 1500);
  }
  
  // Check for streaming content updates
  function checkForStreamingUpdates() {
    const chatContainer = document.querySelector('[data-chat-container]');
    if (!chatContainer) return;
    
    // If content height changed, scroll (streaming in progress)
    if (chatContainer.scrollHeight !== lastScrollHeight) {
      lastScrollHeight = chatContainer.scrollHeight;
      scrollToBottom(false, false);
    }
  }
  
  // Watch for new messages with improved detection
  const observer = new MutationObserver((mutations) => {
    let shouldScroll = false;
    
    mutations.forEach(mutation => {
      mutation.addedNodes.forEach(node => {
        // Check if a message bubble was added
        if (node.nodeType === 1 && 
            (node.classList?.contains('message-bubble') || 
             node.querySelector?.('.message-bubble'))) {
          shouldScroll = true;
        }
      });
      
      // Also check for content changes (like when thinking indicator is replaced)
      if (mutation.type === 'characterData' || mutation.type === 'childList') {
        const target = mutation.target;
        if (target.nodeType === 1 && 
            (target.classList?.contains('message-bubble') || 
             target.closest?.('.message-bubble'))) {
          shouldScroll = true;
        }
      }
    });
    
    if (shouldScroll) {
      const messages = document.querySelectorAll('.message-bubble');
      if (messages.length >= lastMessageCount) {
        lastMessageCount = messages.length;
        // Small delay to ensure content is rendered
        setTimeout(() => scrollToBottom(true), 100);
      }
    }
  });
  
  // Start observing when page loads
  function init() {
    const chatContainer = document.querySelector('[data-chat-container]');
    if (chatContainer) {
      // Add scroll listener
      chatContainer.addEventListener('scroll', handleScroll, { passive: true });
      
      // Start observing for changes
      observer.observe(chatContainer, {
        childList: true,
        subtree: true,
        characterData: true,
        attributes: true,
        attributeFilter: ['class']
      });
      
      lastMessageCount = document.querySelectorAll('.message-bubble').length;
      lastScrollHeight = chatContainer.scrollHeight;
      
      // Start checking for streaming updates every 100ms
      if (streamingCheckInterval) {
        clearInterval(streamingCheckInterval);
      }
      streamingCheckInterval = setInterval(checkForStreamingUpdates, 100);
      
      // Initial scroll to bottom
      setTimeout(() => scrollToBottom(true, true), 100);
    } else {
      // Retry if container not found yet
      setTimeout(init, 100);
    }
  }
  
  // Initialize based on document state
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
  
  // Re-initialize on Reflex page changes
  window.addEventListener('load', init);
})();
