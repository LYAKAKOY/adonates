let closeBtn = document.querySelector('.notification__close');
let notificationBlock = document.querySelector('.notification');


closeBtn.onclick = function () {
    notificationBlock.classList.toggle('closed')
    setTimeout(function() {
        document.querySelector('.notification').remove();
    }, 300);
}
