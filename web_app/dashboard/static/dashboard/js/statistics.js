let btnSide = document.querySelector('#btnside');
let sidebar = document.querySelector('.sidebar');
let diagramItems = document.querySelectorAll('.diagram__item');
let diagramDays = document.querySelectorAll('.diagram__day');
let moneyCount = document.querySelectorAll('.money-count');


function getCoords(elem) {
    let box = elem.getBoundingClientRect();
    console.log(box);
    console.log(window.scrollY);

    return {
        top: box.top + window.scrollY,
        bottom: box.bottom + window.scrollY,
        left: box.left + window.scrollX,
        right: box.right + window.scrollX
    };
}

function createMessage(elem, date, cash) {
    let message = document.createElement('div');
    message.classList.add('tooltip');

    function myFunction(x) {
        if (x.matches) {
            message.style.cssText = 
            `position: absolute; 
            color: #0e0e0e; 
            height: 30px;
            max-width: 55px;
            width: 100%; 
            background: #fff;
            font-size: 9px;
            box-shadow: 10px 5px 20px rgba(0, 0, 0, 0.1); 
            border-radius: 4px;
            text-align: center;`;
        }
        else {
            message.style.cssText = 
            `position: absolute; 
            color: #0e0e0e; 
            height: 38px;
            max-width: 90px;
            width: 100%; 
            background: #fff;
            font-size: 12px;
            box-shadow: 10px 5px 20px rgba(0, 0, 0, 0.1); 
            border-radius: 4px;
            text-align: center;`;
        }
    }
      
    let x = window.matchMedia("(max-width: 550px)")
    myFunction(x)
    x.addListener(myFunction)

    let coords = getCoords(elem);

    message.style.left = coords.left + "px";
    message.style.top = coords.top - 45 + "px";
    console.log(message.style.left);
    console.log(message.style.top);

    message.innerHTML = date + '<br>' + cash;
    return message;
}


function createFiller() {
    let elem = document.createElement('div');
    elem.style.position = 'fixed';
    elem.style.top = 0;
    elem.style.width = '100vw';
    elem.style.height = '100vh';
    elem.style.zIndex = '100';
    elem.style.background = 'rgba(0, 0, 0, 0.2)';
    return elem
}


document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        sidebar.classList.remove('active');
        sidebar.classList.remove('toggle');
        document.getElementsByTagName('html')[0].style.overflowY = "hidden" ? '' : document.getElementsByTagName('html')[0].style.overflowY = "scroll"
        sidebar.classList.contains('active') ? document.body.append(filler) :  filler.remove()
    }
})

let filler = createFiller();
btnSide.onclick = function () {
    sidebar.classList.toggle('active');
    sidebar.classList.toggle('toggle');
    if (sidebar.classList.contains('active')) {
        document.body.append(filler);
        document.getElementsByTagName('html')[0].style.overflow = "hidden";
    }
    else {
        filler.remove();
        document.getElementsByTagName('html')[0].style.overflow = "scroll";
    }
};

const xhr = new XMLHttpRequest();
xhr.open('GET', '/api/v1/donates_for_week/', true);

xhr.onload = function() {
  if (xhr.status === 200) {
    const response = JSON.parse(xhr.responseText);
    const statistics = response.statistics_for_last_week
    const totalSum = statistics.reduce((total, item) => total + item.day_sum, 0);
    let i = 0
    for(let item of moneyCount) {
      let money = Math.floor(totalSum / (2*i))
      item.innerHTML = `${i === 0 ? totalSum: money}P`
      i++
    }
    if (totalSum === 0) {
      for(let item of diagramItems) {
        item.addEventListener('mouseover', function() {
          this.classList.add('selected');
        });
        item.addEventListener('mouseout', function() {
          this.classList.remove('selected');
        });

        item.style.height = `0px`;
        item.style.marginTop = `250px`;
      }
    }
    else {
      i = 0
      for(let item of diagramItems) {
        item.addEventListener('mouseover', function() {
          this.classList.add('selected');
        });
        item.addEventListener('mouseout', function() {
          this.classList.remove('selected');
        });

        let n = (statistics[i].day_sum / totalSum) * 250;
        item.style.height = `${n}px`;
        item.style.marginTop = `${250 - n}px`;
        i++;
      }
    }
    i = 0
    for(let item of diagramDays) {
      item.innerHTML = `${statistics[i].day.toString().padStart(2, '0')}.${statistics[i].month.toString().padStart(2, '0')}`
      i++
    }
    i = 0
    for(let item of diagramItems) {
        let message = createMessage(item,
            `${statistics[i].day.toString().padStart(2, '0')}.${statistics[i].month.toString().padStart(2, '0')}`,
            `${statistics[i].day_sum}P`);
        item.addEventListener('mouseover', function() {
            document.body.append(message);
        });
        item.addEventListener('mouseout', function() {
            message.remove()
        });
        i++
    }
  } else {
    console.error('Ошибка запроса: ' + xhr.status);
  }
};

xhr.onerror = function() {
  console.error('Произошла ошибка сети');
};

xhr.send();