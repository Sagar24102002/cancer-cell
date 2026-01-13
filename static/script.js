
    
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Show loading state
            const button = document.getElementById('analyzeButton');
            button.textContent = 'Analyzing...';
            button.disabled = true;
            
            try {
                const formData = new FormData(form);
                
                const response = await fetch('/predict', {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                
                // Get the response HTML and replace the current page
                const html = await response.text();
                document.documentElement.innerHTML = html;
                
                // Update the URL to reflect the new page
                window.history.pushState({}, '', '/predict');
                
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while processing the image. Please try again.');
            } finally {
                if (button) {
                    button.textContent = 'Analyze Image';
                    button.disabled = false;
                }
            }
        });
    }
});

// Initialize highlight functionality if on result page
if (document.getElementById('highlightOverlay')) {
    initializeHighlightFunctionality();
}

// Remove the toggleHeatmap function and update the image controls
function initializeHighlightFunctionality() {
    const processedImg = document.getElementById('processedImg');
    const canvas = document.getElementById('highlightOverlay');
    const ctx = canvas.getContext('2d');
    let highlightEnabled = true;

    processedImg.onload = function() {
        canvas.width = processedImg.width;
        canvas.height = processedImg.height;
        drawHighlight();
    };

    function drawHighlight() {
        if (!highlightEnabled) {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            return;
        }

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = 'rgba(231, 76, 60, 0.3)';
        ctx.strokeStyle = '#e74c3c';
        ctx.lineWidth = 3;
        
        const regionData = window.regionData || [];
        
        regionData.forEach(region => {
            const centerX = region.x + region.width / 2;
            const centerY = region.y + region.height / 2;
            const radius = Math.max(region.width, region.height) / 2;

            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.stroke();
        });
    }

    window.toggleHighlight = function() {
        highlightEnabled = !highlightEnabled;
        drawHighlight();
    };
}

// Add this function for image validation
function validateImage(file) {
    // Check file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
        throw new Error('Invalid file type. Please upload JPG, JPEG or PNG images only.');
    }
    
    // Check file size (max 16MB)
    if (file.size > 16 * 1024 * 1024) {
        throw new Error('File size too large. Maximum size is 16MB.');
    }
}

// Update form submission handler
document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const imageFile = formData.get('image');
    const submitButton = e.target.querySelector('button[type="submit"]');
    
    try {
        // Validate image before submission
        validateImage(imageFile);
        
        // Show loading state
        submitButton.disabled = true;
        submitButton.textContent = 'Processing...';
        
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'An error occurred during processing');
        }
        
        // Get the response HTML and replace the current page
        const html = await response.text();
        document.documentElement.innerHTML = html;
        
        // Update the URL to reflect the new page
        window.history.pushState({}, '', '/predict');
        
    } catch (error) {
        alert(error.message);
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Analyze Image';
    }
});

// Add image preview functionality
document.getElementById('image').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        try {
            validateImage(file);
            
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('imagePreview');
                if (preview) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
            };
            reader.readAsDataURL(file);
        } catch (error) {
            alert(error.message);
            e.target.value = ''; // Clear the file input
        }
    }
});