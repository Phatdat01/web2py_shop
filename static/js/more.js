function purchase_action(event) {
    var form = event.target.closest('form');
    form.querySelector('input[name="purchase"]').value = "1";
    form.submit();
    event.preventDefault();
}

function changeQuantity(delta) {
    var input = event.target.parentNode.querySelector('input[name="quantity"]');
    var currentValue = parseInt(input.value, 10);
    var maxValue = parseInt(input.max, 10);   
    var newValue = currentValue + delta;
    if (newValue >= 1 && newValue <= maxValue) {
        input.value = newValue;
    }
}

function updateQuantity(id, numChange) {
    var formData = new FormData();
    formData.append('id', id); 
    formData.append('num_change', numChange);
    fetch("update", {
        method: 'POST',
        body: formData,
    })
    .then(data => {
        if (data) {
            console.log('Update successful');
        } else {
            console.error('Update failed');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function changeQuantityWithAjax(id, numChange) {
    changeQuantity(numChange)
    updateQuantity(id, numChange);
}