// const date = new Date(); //현재 날짜 객체 만들기
// const date2 = new Date(2023, 09, 11); //지정 날짜 객체 만들기

// // 년, 달, 월, 요일 가져오기
// const viewYear = date.getFullYear(); // 년도 가져오기
// const viewMonth = date.getMonth(); // 달 가져오기
// const viewDate = date.getDate(); // 일 가져오기
// const viewDay = date.getDay(); // 요일 가져오기

// 캘린더 만드는 함수 만들기

let date = new Date();

const makeCalendar = () => {
  // 캘린더에 보이는 년도와 달을 보여주기 위해
  const viewYear = date.getFullYear();
  const viewMonth = date.getMonth();

  // 캘린더 년도 달 채우기
  document.querySelector(".year-month").textContent = `${viewYear}년 ${
    viewMonth + 1
  }월`;

  // 지난 달 마지막 날짜와 요일
  const prevLast = new Date(viewYear, viewMonth, 0);
  const prevDate = prevLast.getDate();
  const prevDay = prevLast.getDay();

  // 이번 달 마지막 날짜 가져오기
  const thisLast = new Date(viewYear, viewMonth + 1, 0);
  const thisDate = thisLast.getDate();
  const thisDay = thisLast.getDay();

  const prevDates = [];
  const thisDates = [...Array(thisDate + 1).keys()].slice(1);
  const nextDates = [];

  if (prevDay !== 6) {
    for (let i = 0; i < prevDay + 1; i++) {
      prevDates.unshift(prevDate - i);
      // 31-0, 31-1, 31-2, ...
      // 31, 30, 29, 38, ...
    }
  }

  for (let i = 1; i < 7 - thisDay; i++) {
    nextDates.push(i);
  }

  //날짜 그리기

  const dates = prevDates.concat(thisDates, nextDates);

  const firstDateIndex = dates.indexOf(1);
  const lastDateIndex = dates.lastIndexOf(thisDate);

  dates.forEach((date, i) => {
    // 삼한연산자 [조건문] ? [참일 때 실행] : [거짓일 때 실행]
    const condition =
      i >= firstDateIndex && i < lastDateIndex + 1 ? "this" : "other";
    //this
    //other

    dates[
      i
    ] = `<div class="date" ><span class="${condition}">${date}</span></div>`;
  });

  document.querySelector(".dates").innerHTML = dates.join("");

  const today = new Date();

  if (viewMonth === today.getMonth() && viewYear === today.getFullYear()) {
    for (let date of document.querySelectorAll(".this")) {
      if (+date.innerText === today.getDate()) {
        date.classList.add("today");
        break;
      }
    }
  }
};

makeCalendar();

// 이전 달 그리는 함수
const prevMonth = () => {
  date.setDate(1);
  date.setMonth(date.getMonth() - 1);
  makeCalendar();
};

// 다음 달 그리는 함수
const nextMonth = () => {
  date.setDate(1);
  date.setMonth(date.getMonth() + 1);
  makeCalendar();
};

// 현재 달 그리는 함수
const curMonth = () => {
  date = new Date();
  makeCalendar();
};

let prevClickDate = document.querySelector(".today").parentNode;
prevClickDate.classList.add("date-onclick");

function viewDetail() {
  const detailDate = document.querySelector(".detail-timeline p");

  detailDate.innerHTML = this.innerText;
  prevClickDate.classList.remove("date-onclick");
  prevClickDate.classList.add("date");
  this.classList.remove("date");
  this.classList.add("date-onclick");
  prevClickDate = this;
}

let dateTarget = document.querySelectorAll(".date");
dateTarget.forEach((target) => target.addEventListener("click", viewDetail));

function openToggle() {
  document.getElementById("sidebar").style.width = "160px";
}

function closeToggle() {
  document.getElementById("sidebar").style.width = "0";
}
