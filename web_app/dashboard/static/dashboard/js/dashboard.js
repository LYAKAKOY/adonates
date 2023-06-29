let btnSide = document.querySelector('#btnside');
let sidebar = document.querySelector('.sidebar');
let diagramItems = document.querySelectorAll('.diagram__item');
let diagramDays = document.querySelectorAll('.diagram__day');
let diagramItemsSelected = document.querySelectorAll('.diagram__item.selected::before');
let moneyCount = document.querySelectorAll('.money-count');


btnSide.onclick = function () {
    sidebar.classList.toggle('active');
    sidebar.classList.toggle('toggle');
};

const xhr = new XMLHttpRequest();
xhr.open('GET', '/api/v1/donates_for_week/', true);

xhr.onload = function() {
  if (xhr.status === 200) {
    const response = JSON.parse(xhr.responseText);
    const statistics = response.statistics_for_last_week
    const totalSum = statistics.reduce((total, item) => total + item.day_sum, 0);
    let i = 1
    for(let item of moneyCount) {
      item.innerHTML = `${Math.floor(totalSum / (10*i))}P`
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

        let n = (statistics[i].day_sum / totalSum) * 100;
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
    for(let item of diagramItemsSelected) {
      item.style.content = `${statistics[i].day_sum}P ${statistics[i].day.toString().padStart(2, '0')}.${statistics[i].month.toString().padStart(2, '0')}`
    }
  } else {
    console.error('Ошибка запроса: ' + xhr.status);
  }
};

xhr.onerror = function() {
  console.error('Произошла ошибка сети');
};

xhr.send();