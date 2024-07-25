function changeQuantity(delta) {
            // Get the input element
            var input = event.target.parentNode.querySelector('input[name="quantity"]');
            var currentValue = parseInt(input.value, 10);
            var maxValue = parseInt(input.max, 10);
            
            // Update the value based on the delta
            var newValue = currentValue + delta;
            
            // Ensure the new value is within the valid range
            if (newValue >= 1 && newValue <= maxValue) {
                input.value = newValue;
            }
        }