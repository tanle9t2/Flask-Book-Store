const TIME_OUT = 50;
const placeHolderAttribute = ["Nhap ten san pham", "Nhap barcode"]
let fetchOption = 0;
let currentTimeOutId;

const productSearchBox = document.querySelector('.product-search-box');
const dropDownBtn = document.querySelector(".dropdown-btn");
const restoreOrderBtn = document.querySelector(".restore-btn");
const updateBtn = document.querySelector(".update-btn");

const orderContainer = document.querySelector(".order-container");
const productContainer = document.querySelector(".product-container");

let initialOrderItemsState = {};
let currentOrderItemsState = {};

const fetchProductByBarcode = async function () {
    console.log("Fetching by barcode");
    //Logic................
}
const fetchProductByName = async function () {
    console.log("Fetching by name");
    //Logic................
}
const productFetchingFunction = [fetchProductByName, fetchProductByBarcode];

productSearchBox.addEventListener("input", function () {
    clearTimeout(currentTimeOutId);
    currentTimeOutId = setTimeout(function () {
        productFetchingFunction[fetchOption]();
    }, TIME_OUT);
});
dropDownBtn.addEventListener("click", function (e) {
    e.preventDefault();
    const target = e.target.closest('.dropdown-item');
    if (!target) return;
    fetchOption = +e.target.getAttribute("id");
    productSearchBox.setAttribute("placeholder", placeHolderAttribute[fetchOption]);
});

productContainer.addEventListener("click", function (e) {
    const productItem = e.target.closest(".product-item");
    if (!productItem) return;
    const id = productItem.getAttribute("id");

    if (currentOrderItemsState[id]) {
        const input = orderContainer.querySelector(`[input-id="${id}"]`);
        currentOrderItemsState[id]['qty'] = +input.value + 1;
    } else {
        currentOrderItemsState[id] = {
            'book_id': id,
            'price': productItem.querySelector(".product-price").textContent.split(".")[0].trim(),
            'discount': productItem.querySelector(".discount").textContent,
            'title': productItem.querySelector(".product-name").textContent,
            'qty': 1
        };
    }

    renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]));
});

orderContainer.addEventListener("click", function (e) {
    const removeBtn = e.target.closest(".remove-order-item-btn");
    const incrementBtn = e.target.closest(".increment-qty-btn");
    const decrementBtn = e.target.closest(".decrement-qty-btn");
    const id = e.target.closest(".order-item")?.getAttribute("id");
    let isTriggered = false;

    if (removeBtn) {
        if (Object.keys(currentOrderItemsState).length === 1) {
            alert('the order must have at least 1 item');
            return;
        }
        delete currentOrderItemsState[+id];
        isTriggered ||= true;
    }
    if (incrementBtn) {
        const input = incrementBtn.previousElementSibling;
        currentOrderItemsState[+id]['qty'] = +input.value + 1;
        isTriggered ||= true;
    }
    if (decrementBtn) {
        const input = decrementBtn.nextElementSibling;
        currentOrderItemsState[+id]['qty'] = input.value > 1 ? +input.value - 1 : input.value;
        isTriggered ||= true;
    }
    isTriggered && renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]));
});

orderContainer.addEventListener("change", function (e) {
    const input = e.target;
    if (input.value == 0 || input.value == '') input.value = 1;

    currentOrderItemsState[+input.getAttribute("input-id")]['qty'] = +input.value;
    renderOrderItem(Object.entries(currentOrderItemsState).map(item => item[1]))
})

restoreOrderBtn.addEventListener("click", () => {
    renderOrderItem(Object.entries(initialOrderItemsState).map(item => item[1]))
    currentOrderItemsState = JSON.parse(JSON.stringify(initialOrderItemsState));
});

updateBtn.addEventListener("click", async function (e) {
    updateBtn.classList.remove("bg-blue")
    updateBtn.classList.add("btn-disable")
    updateBtn.disabled = true
    restoreOrderBtn.classList.remove("bg-red")
    restoreOrderBtn.classList.add("btn-disable")
    restoreOrderBtn.disabled = true
    let msg = 'Successfully updated';

    try {
        const res = await fetch(`/api/v1/order/${+updateBtn.getAttribute("order-id")}/update`, {
            method: "POST",
            body: JSON.stringify(Object.values(currentOrderItemsState)),
            headers: {
                'Content-Type': 'application/json'
            }
        });
        if (!res.ok) throw new Error("Something went wrong");
        initialOrderItemsState = JSON.parse(JSON.stringify(currentOrderItemsState));

    } catch (err) {
        msg = err.message;
    } finally {
        Toastify({
            text: msg,
            duration: 3000,
            // destination: "https://github.com/apvarun/toastify-js",
            newWindow: true,
            close: true,
            gravity: "top", // `top` or `bottom`
            position: "center", // `left`, `center` or `right`
            stopOnFocus: true, // Prevents dismissing of toast on hover
            style: {
                background: "#6cbf6c",
            }
        }).showToast();
        updateBtn.classList.add("bg-blue")
        updateBtn.classList.remove("btn-disable")
        updateBtn.disabled = false
        restoreOrderBtn.classList.add("bg-red")
        restoreOrderBtn.classList.remove("btn-disable")
        restoreOrderBtn.disabled = false
    }
})

const renderOrderItem = function (books) {
    const orderList = orderContainer.querySelector(".order-list");
    orderList.innerHTML = '';
    const html = books.map(book => `
        <tr class="order-item" id="${book.book_id}">
            <th scope="row">
                <div class="media align-items-center">
                    <div class="media-body text-left text-truncate book-item">
                        <span class="name mb-0 text-sm text-center w-100">${book.title}</span>
                    </div>
                </div>
            </th>
            <td class="budget text-center">
                ${book.price} VNĐ
            </td>
            <td>
                <span class="badge badge-dot mr-4 text-center w-100">
                <span class="status text-center">${book.discount}</span>
                </span>
            </td>
            <td>
                <div class="d-flex justify-content-center">
                    <div class="d-flex justify-content-between align-content-center w-100">
                        <span class="cursor-pointer decrement-qty-btn">-</span>
                        <input input-id="${book.book_id}" inputmode="numeric"
                               oninput="this.value = this.value.replace(/\\D+/g, '')"
                               class="text-center" value="${book.qty}">
                        <span class="cursor-pointer increment-qty-btn">+</span>
                    </div>
                </div>
            </td>
            <td>
                <div class="d-flex align-items-center w-100 justify-content-center">
                    <span class="completion mr-2">${+book.price * +book.qty}</span>
                </div>
            </td>
            <td class="text-right remove-order-item-btn">
                <div class="dropdown">
                    <a class="btn btn-sm btn-icon-only text-light cursor-pointer"  role="button">
                        <i class="fa fa-window-close" aria-hidden="true"></i>
                    </a>
                </div>
            </td>
        </tr>`).join('');
    const totalAmount = books.reduce((acc, obj) => acc + +obj['price'] * +obj['qty'], 0);
    const shippingFee = +document.querySelector(".shipping-fee").textContent.trim().split(" ")[0].trim();
    document.querySelector(".total-amount").textContent = totalAmount + shippingFee + ' VND';
    orderList.insertAdjacentHTML('beforeend', html);
}

orderContainer.querySelectorAll(".order-item").forEach(orderItem => {
    const obj = {
        'book_id': orderItem.getAttribute("id"),
        'price': orderItem.querySelector(".order-item-price").textContent.trim().split(".")[0],
        'discount': orderItem.querySelector(".order-item-discount").textContent,
        'title': orderItem.querySelector(".order-item-name").textContent,
        'qty': orderItem.querySelector(`[input-id="${orderItem.getAttribute("id")}"]`).value
    }
    initialOrderItemsState[obj["book_id"]] = obj;
    currentOrderItemsState[obj["book_id"]] = obj;
});
