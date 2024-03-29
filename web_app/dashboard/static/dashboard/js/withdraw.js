let btnSide = document.querySelector('#btnside');
let sidebar = document.querySelector('.sidebar');
let closeBtn = document.querySelector('.modal-window-close');
let modalWindow = document.querySelector('.modal-window');
const withdrawTitleContainer = document.querySelector('.withdraw__title-container');
const modalBtn = withdrawTitleContainer.querySelector('.button_refactor');
let saveBtn = document.querySelector('.save');
let balance = document.querySelector('.balance__info')

function createFillerModal() {
    let elem = document.createElement('div');
    elem.style.position = 'fixed';
    elem.style.top = 0;
    elem.style.width = '100vw';
    elem.style.height = '100vh';
    elem.style.zIndex = '101';
    elem.style.background = 'rgba(0, 0, 0, 0.2)';
    return elem
}

function createFillerSidebar() {
    let elem = document.createElement('div');
    elem.style.position = 'fixed';
    elem.style.top = 0;
    elem.style.width = '100vw';
    elem.style.height = '100vh';
    elem.style.zIndex = '100';
    elem.style.background = 'rgba(0, 0, 0, 0.2)';
    return elem
}

function noMoreSorry() {};

function createSorry() {
    createSorry = noMoreSorry;
    let message = document.createElement('div');
    message.classList.add('message');
    message.innerHTML = 'Простите, но данный метод оплаты пока не доступен';
    message.style.color = '#fff';
    message.style.marginTop = '15px'
    document.querySelector('.main__field').append(message)
    return message
}

function findOption(select) {
    const option = select.querySelector(`option[value="${select.value}"]`)
    if (option.innerHTML === 'СБП' || option.innerHTML === 'Банковская карта') {
        [...document.querySelectorAll('.subtitle')].forEach(x => x.style.display = 'none');
        [...document.querySelectorAll('.subtitle')][0].style.display = 'block';
        [...document.querySelectorAll('.inp_cash')].forEach(x => x.style.display = 'none');
        if (document.getElementsByClassName('message') !== true) {
            let message = createSorry();
            document.querySelector('.message').style.visibility  = 'visible';
        }
    }
    else {
        for(item of document.querySelectorAll('.subtitle')) {
            item.style.display = 'block';
            [...document.querySelectorAll('.inp_cash')].forEach(x => x.style.display = 'block');
        }
        document.querySelector('.message').style.visibility  = 'hidden';
    }
}

let fillerModal = createFillerModal();
let fillerSidebar = createFillerSidebar();
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        modalWindow.style.display = 'none';
        fillerModal.remove();
        fillerSidebar.remove();
        document.getElementsByTagName('html')[0].style.overflowY = "hidden" ? '' : document.getElementsByTagName('html')[0].style.overflowY = "scroll"
        sidebar.classList.contains('active') ?  sidebar.classList.remove('active', 'toggle')  :  filler.remove()
    }
})

modalBtn.onclick = () => {
    modalWindow.style.display = 'flex';
    document.body.append(fillerModal);
    // document.getElementsByTagName('html')[0].style.overflowY = "hidden";
}

closeBtn.onclick = function() {
    modalWindow.style.display = 'none';
    fillerModal.remove();
    document.getElementsByTagName('html')[0].style.overflowY = "scroll";
}

btnSide.onclick = function () {
    sidebar.classList.toggle('active');
    sidebar.classList.toggle('toggle');
    if (sidebar.classList.contains('active')) {
        document.body.append(fillerSidebar);
        document.getElementsByTagName('html')[0].style.overflowY = "hidden";
    }
    else {
        fillerSidebar.remove();
        document.getElementsByTagName('html')[0].style.overflowY = "scroll";
    }
}

saveBtn.onclick = function() {
    modalWindow.style.display = 'none';
    fillerModal.remove();
}

const Payout = function () {
    const xhr = new XMLHttpRequest();
    xhr.open('GET', '/payout/', true);

    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const payout_status = response.payout_status
            if (payout_status === 'balance equal zero') {
                alert('Простите что-то пошло не так, либо на вашем балансе 0 рублей 🤔')
            }
            else if (payout_status === 'no card') {
                alert('Вы не выбрали никакой способ вывода 😵')
            }
            else {
                alert('Успешный вывод средств. Деньги придут в течении 15 минут 🤑')
                balance.innerHTML = 'Ваш баланс: 0,00Р' +
                    '<a href="#" class="withdraw-button button" onclick="Payout()">Вывести</a>'
            }

        }
    }

    xhr.onerror = function() {
        console.error('Произошла ошибка сети');
    };

    xhr.send();
}

const itemsCont = document.querySelector('.withdraw__inner');
let selectedItem;

itemsCont.onclick = function(event) {
    let target = event.target.closest('.items-container__item');

    if (!target) return;
    if (target.tagName !== 'DIV') return;
    if (!itemsCont.contains(target)) return;
    if (document.querySelector('.selected')) document.querySelector('.selected').classList.remove('selected');

    select(target);

}

function select(item) {
    if(selectedItem) {
        selectedItem.classList.remove('selected');
    }

    selectedItem = item;
    selectedItem.classList.add('selected');
    if(typeof(localStorage) != "undefined"){
        localStorage.value = selectedItem.textContent.trim();
    }
    // console.log(selectedItem.textContent.trim())
    const xhr = new XMLHttpRequest();

    xhr.open('POST', '/payout_method/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function() {
    if (xhr.status === 200) {
        const response = xhr.responseText;
        console.log(response);
        }
    };

    xhr.onerror = function() {
        console.error('Произошла ошибка при отправке запроса');
    };

    const jsonData = JSON.stringify(selectedItem.textContent.trim());
    xhr.send(jsonData);
}

if(localStorage.value) {
    [...(itemsCont.getElementsByClassName('items-container__item'))].forEach(x => x.textContent.trim() === localStorage.value ?
    x.classList.add('selected')
    :  x.classList.remove('selected'))
}
