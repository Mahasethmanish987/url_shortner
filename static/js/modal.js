// Show QR Code Modal
function showQRCode(shortCode) {
    console.log('showQRCode called with:', shortCode);
    
    const modal = document.getElementById('qrModal');
    console.log('Modal element:', modal);
    
    if (!modal) {
        console.error('❌ qrModal element not found!');
        alert('Modal not found. Check if qr_modal.html is included in the template.');
        return;
    }
    
    // Show modal and set the URL text
    modal.style.display = 'block';
    console.log('Modal display set to block');
    
    const qrUrlElement = document.getElementById('qrUrl');
    if (qrUrlElement) {
        qrUrlElement.textContent = window.location.origin + '/' + shortCode;
        console.log('QR URL set to:', qrUrlElement.textContent);
    } else {
        console.error('❌ qrUrl element not found!');
    }
    
    // Reset modal state
    const loading = document.getElementById('qrLoading');
    const content = document.getElementById('qrContent');
    const error = document.getElementById('qrError');
    const download = document.getElementById('downloadQR');
    
    if (loading && content && error && download) {
        loading.style.display = 'flex';
        content.style.display = 'none';
        error.style.display = 'none';
        download.style.display = 'none';
        console.log('Modal state reset - showing loading');
    } else {
        console.error('❌ One or more modal elements not found!');
        console.log('Loading:', loading, 'Content:', content, 'Error:', error, 'Download:', download);
    }
    
    // ✅ FIXED: Updated fetch URL to match your Django URL structure
    const qrApiUrl = '/shortner/qr/' + shortCode + '/';
    console.log('Fetching QR from:', qrApiUrl);
    
    fetch(qrApiUrl)
        .then(response => {
            console.log('Fetch response status:', response.status);
            if (!response.ok) throw new Error('Failed to generate QR code');
            return response.blob();
        })
        .then(blob => {
            console.log('QR blob received:', blob);
            const imageUrl = URL.createObjectURL(blob);
            const qrImage = document.getElementById('qrImage');
            
            if (qrImage) {
                qrImage.src = imageUrl;
                console.log('QR image src set');
            } else {
                console.error('❌ qrImage element not found!');
            }
            
            // Show QR content and hide loading
            if (loading && content && download) {
                loading.style.display = 'none';
                content.style.display = 'flex';
                download.style.display = 'inline-flex';
                console.log('Showing QR content');
            }
            
            // Setup download button
            const downloadBtn = document.getElementById('downloadQR');
            if (downloadBtn) {
                downloadBtn.onclick = function() {
                    const link = document.createElement('a');
                    link.href = imageUrl;
                    link.download = 'qr-code-' + shortCode + '.png';
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                };
                console.log('Download button setup complete');
            }
        })
        .catch(error => {
            console.error('QR generation error:', error);
            if (loading && error) {
                loading.style.display = 'none';
                error.style.display = 'block';
                console.log('Showing error state');
            }
        });
}

// Close Modal Function
function closeModal() {
    console.log('closeModal called');
    const modal = document.getElementById('qrModal');
    if (modal) {
        console.log('Modal found, setting display to none');
        modal.style.display = 'none';
        console.log('Modal hidden');
    } else {
        console.error('❌ Modal not found in closeModal!');
    }
}

// Initialize event listeners when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOMContentLoaded - Initializing modal listeners');
    
    const modal = document.getElementById('qrModal');
    console.log('Modal on DOM load:', modal);
    
    if (!modal) {
        console.error('❌ qrModal not found during initialization!');
        return;
    }
    
    // Close when clicking X button
    const closeX = document.querySelector('.modal-close');
    console.log('Close X button element:', closeX);
    if (closeX) {
        closeX.addEventListener('click', function() {
            console.log('X button clicked!');
            closeModal();
        });
        console.log('Close X button listener added');
    } else {
        console.error('❌ .modal-close element not found!');
    }
    
    // Close when clicking Close button
    const closeBtn = document.querySelector('.modal-close-btn');
    console.log('Close button element:', closeBtn);
    if (closeBtn) {
        closeBtn.addEventListener('click', function() {
            console.log('Close button clicked!');
            closeModal();
        });
        console.log('Close button listener added');
    } else {
        console.error('❌ .modal-close-btn element not found!');
    }
    
    // Close when clicking outside the modal
    modal.addEventListener('click', function(event) {
        console.log('Modal clicked, target:', event.target);
        if (event.target === modal) {
            console.log('Outside click detected');
            closeModal();
        }
    });
    console.log('Outside click listener added');
    
    // Close with Escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && modal.style.display === 'block') {
            console.log('Escape key pressed');
            closeModal();
        }
    });
    console.log('Escape key listener added');
    
    console.log('Modal initialization complete');
});