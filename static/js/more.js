function changeQuantity(delta) {
    var input = event.target.parentNode.querySelector('input[name="quantity"]');
    var currentValue = parseInt(input.value, 10);
    var maxValue = parseInt(input.max, 10);   
    var newValue = currentValue + delta;
    if (newValue >= 1 && newValue <= maxValue) {
        input.value = newValue;
    }
}

function updateQuantity(id, delta) {
    var formData = new FormData();
    formData.append('id', id); 
    formData.append('delta', delta);
    fetch("update", {
        method: 'POST',
        body: formData,
    })
    .then(data => {
        if (data) {
            // Update the UI or show a success message
            console.log('Update successful');
        } else {
            // Handle error
            console.error('Update failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function changeQuantityWithAjax(id, delta) {
    changeQuantity(delta)
    updateQuantity(delta);
}