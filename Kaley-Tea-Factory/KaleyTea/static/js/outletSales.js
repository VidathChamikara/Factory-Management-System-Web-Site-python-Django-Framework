function openEditForm() {
  document.getElementById("editForm").style.display = "block";
}

function closeEditForm() {
  document.getElementById("editForm").style.display = "none";
}

function openDeleteForm() {
  document.getElementById("deleteForm").style.display = "block";
}

function closeDeleteForm() {
  document.getElementById("deleteForm").style.display = "none";
}

function openCheckoutForm() {
  document.getElementById("checkoutForm").style.display = "block";
}

function closeCheckoutForm() {
  document.getElementById("checkoutForm").style.display = "none";
}




function openGreenForm() {
  document.getElementById("greenForm").style.display = "block";
}

function closeGreenForm() {
  document.getElementById("greenForm").style.display = "none";
}

function openRedForm() {
  document.getElementById("redForm").style.display = "block";
}

function closeRedForm() {
  document.getElementById("redForm").style.display = "none";
}





function editPrice(id, name, category, weight, price) {
    document.getElementById("editid").value = id;
    document.getElementById("editidpass").innerHTML = id;
    document.getElementById("editname").innerHTML = name;
    document.getElementById("editcategory").innerHTML = category;
    document.getElementById("editweight").innerHTML = weight;
    document.getElementById("editprice").value = price;
}

function deletePrice(id, name, category, weight, price) {
    document.getElementById("deleteid").innerHTML = id;
    document.getElementById("deletename").innerHTML = name;
    document.getElementById("deletecategory").innerHTML = category;
    document.getElementById("deleteweight").innerHTML = weight;
    document.getElementById("deleteprice").innerHTML = price;
    document.getElementById("deleteidpass").value = id;
}

function removeFromCart(id, name, category, weight, price, qty, subtol) {
    document.getElementById("deleteid").innerHTML = id;
    document.getElementById("deletename").innerHTML = name;
    document.getElementById("deletecategory").innerHTML = category;
    document.getElementById("deleteweight").innerHTML = weight;
    document.getElementById("deleteprice").innerHTML = price;
    document.getElementById("deleteqty").innerHTML = qty;
    document.getElementById("deletesubtot").innerHTML = subtol;
    document.getElementById("deleteidpass").value = id;
}

