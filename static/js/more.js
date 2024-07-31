
function changeAllRow() {
    var rows = document.querySelectorAll('tr'); // Select all rows
    var th_row = rows[0].querySelector('input[name="check"]');
    var currentValue = th_row.value;

    // Toggle the value
    var newValue = currentValue === "0" ? "1" : "0";
    th_row.value = newValue;

    Array.prototype.slice.call(rows, 1).forEach(function(row) {
        var hiddenRowInput = row.querySelector('input[name="check"]');
        hiddenRowInput.value = newValue;

        if (newValue === "1") {
            row.style.backgroundColor = 'gray';
        } else {
            row.style.backgroundColor = '';
        }
    });
}

function changeRowColorAndCheck(cartId) {
    var button = document.getElementById('btn_' + cartId);
    var td = button.parentElement;
    var tr = td.parentElement;
    tr.style.backgroundColor = 'gray';
    var hiddenInput = document.getElementById('check_' + cartId);
    if (hiddenInput.value === "0") {
        tr.style.backgroundColor = 'gray';
        hiddenInput.value = "1";
    } else {
        tr.style.backgroundColor = '';
        hiddenInput.value = "0";
    }
}

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
    changeQuantity(numChange);
    updateQuantity(id, numChange);
}