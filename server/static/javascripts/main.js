// const date = new Date(); //현재 날짜 객체 만들기
// const date2 = new Date(2023, 09, 11); //지정 날짜 객체 만들기

// // 년, 달, 월, 요일 가져오기
// const viewYear = date.getFullYear(); // 년도 가져오기
// const viewMonth = date.getMonth(); // 달 가져오기
// const viewDate = date.getDate(); // 일 가져오기
// const viewDay = date.getDay(); // 요일 가져오기

// 캘린더 만드는 함수 만들기

let date = new Date();
let currentYear = date.getFullYear();
let currentMonth = date.getMonth();

const makeCalendar = () => {
  // 캘린더에 보이는 년도와 달을 보여주기 위해
  const viewYear = date.getFullYear();
  const viewMonth = date.getMonth();

  currentYear = viewYear;
  currentMonth = viewMonth + 1;

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
  // 지금 보여지는 달력에 나타나는 일들
  const dates = prevDates.concat(thisDates, nextDates);

  const firstDateIndex = dates.indexOf(1);
  const lastDateIndex = dates.lastIndexOf(thisDate);

  const requestPlan = new XMLHttpRequest();
  const url = "/view_plan/";
  requestPlan.open("POST", url, true);
  requestPlan.setRequestHeader(
    "Content-Type",
    "applcation/x-www-form-urlencoded"
  );

  //meeting: 현재 유저가 보고 있는 모임 이름(meeting_name)
  requestPlan.send(
    JSON.stringify({ year: viewYear, month: viewMonth, meeting: " " })
  );

  requestPlan.onreadystatechange = () => {
    if (requestPlan.readyState === XMLHttpRequest.DONE) {
      if (requestPlan.status < 400) {
        const { plans, userimg } = JSON.parse(requestPlan.response);
        const plansArray = JSON.parse(plans);
        let isPlan = new Array(dates.length).fill(false);
        plansArray.forEach((plan) => {
          const startDay = parseInt(
            plan.fields.startTime[8] + plan.fields.startTime[9]
          );
          const endDay = parseInt(
            plan.fields.endTime[8] + plan.fields.endTime[9]
          );
          for (let i = startDay; i <= endDay; i++) {
            isPlan[i + firstDateIndex - 1] = true;
          }
        });

        dates.forEach((date, i) => {
          // 삼한연산자 [조건문] ? [참일 때 실행] : [거짓일 때 실행]
          const condition =
            i >= firstDateIndex && i < lastDateIndex + 1 ? "this" : "other";
          //this
          //other
          const planning =
            isPlan[i] == true ? `<img src="${userimg}" width="15" />` : "";

          dates[
            i
          ] = `<div class="date"><span class="${condition}">${date} ${planning}</span></div>`;
        });

        document.querySelector(".dates").innerHTML = dates.join("");

        const today = new Date();

        if (
          viewMonth === today.getMonth() &&
          viewYear === today.getFullYear()
        ) {
          for (let date of document.querySelectorAll(".this")) {
            if (+date.innerText === today.getDate()) {
              date.classList.add("today");
              break;
            }
          }
        }
      }
    }
  };
};

makeCalendar();

// // 이전 달 그리는 함수
// const prevMonth = () => {
//   date.setDate(1);
//   date.setMonth(date.getMonth() - 1);
//   makeCalendar();
// };

// // 다음 달 그리는 함수
// const nextMonth = () => {
//   date.setDate(1);
//   date.setMonth(date.getMonth() + 1);
//   makeCalendar();
// };

// 현재 달 그리는 함수
const curMonth = () => {
  date = new Date();
  makeCalendar();
};

const requestNewPlan = new XMLHttpRequest();

const plan_create = (username) => {
  const url = "/create";
  requestNewPlan.open("POST", url, true);
  requestNewPlan.setRequestHeader(
    "Content-Type",
    "applcation/x-www-form-urlencoded"
  );

  const title = document.getElementById("plan_title").value;
  const location = document.getElementById("plan_location").value;
  const startTime = document.getElementById("plan_startTime").value;
  const endTime = document.getElementById("plan_endTime").value;
  const content = document.getElementById("plan_content").value;
  requestNewPlan.send(
    JSON.stringify({
      username: username,
      title: title,
      location: location,
      startTime: startTime,
      endTime: endTime,
      content: content,
    })
  );
};

requestNewPlan.onreadystatechange = () => {
  if (requestNewPlan.readyState === XMLHttpRequest.DONE) {
    if (requestNewPlan.status < 400) {
      const { startTime, endTime, userimg } = JSON.parse(
        requestNewPlan.response
      );
      const newStartYear = startTime.slice(0, 4);
      const newStartMonth = startTime.slice(5, 7);
      const newStartDate = parseInt(startTime.slice(8, 10));

      const newEndYear = endTime.slice(0, 4);
      const newEndMonth = endTime.slice(5, 7);
      const newEndDate = parseInt(endTime.slice(8, 10));

      if (
        newStartYear <= currentYear &&
        currentYear <= newEndYear &&
        newStartMonth <= currentMonth &&
        currentMonth <= newEndMonth
      ) {
        console.log("Here");
        const dateArray = document.querySelectorAll(".date");
        dateArray.forEach((date) => {
          const thisdate = date.childNodes[0].innerText;
          if (
            parseInt(date.childNodes[0].innerText) <= newEndDate &&
            newStartDate <= parseInt(date.childNodes[0].innerText) &&
            date.childNodes[0].classList.contains("this")
          ) {
            date.childNodes[0].innerHTML = `${thisdate}  <img src="${userimg}" width="15" />`;
          }
        });
      }
    }
  }
};

function openToggle() {
  document.getElementById("sidebar").style.width = "250px";
}

function closeToggle() {
  document.getElementById("sidebar").style.width = "0";
}

const modalButton = document.querySelector(".modalButton");
const modal = document.querySelector(".modal");
const closeModal = document.querySelector(".closeModal");
const closeModal2 = document.querySelector(".closeModal2");

modalButton.addEventListener("click", () => {
  modal.classList.remove("hidden");
});

closeModal.addEventListener("click", () => {
  modal.classList.add("hidden");
});
closeModal2.addEventListener("click", () => {
  modal.classList.add("hidden");
});
/*

  일정 삭제 클릭 시 실행 함수
  선택한 일정의 id 값을 인자로 넘김
  method: POST
*/
const plan_delete = async (id) => {
  const url = "/delete";
  await axios.post(url, {
    id,
  });
};

/*
  일정 수정 버튼 클릭 시 실행 함수
  일정 생성과 로직은 동일하며 추가로 일정 객체의 id 값을 추가로 넘김
  순서: startTime, endTime, location, title, content (이후 데이터 추가 시 순서 주의)
  method: POST
  return: err_msg
          에러 메세지 접근 방법: err_msg.data.{모델 필드 이름}_err
          에러가 아닌 경우 value 값에 "" 이 둘어가 있음.
          ex) err_msg.data.time_err

*/
const plan_update = async (id) => {
  const url = "/update";
  inputs = document.getElementsByTagName("input");
  const data = {
    id,
    startTime: inputs[0].value + " " + inputs[1].value,
    endTime: inputs[0].value + " " + inputs[2].value,
    location: inputs[3].value,
    title: inputs[4].value,
    content: inputs[5].value,
  };

  const err_msg = await axios.post(url, data);
  console.log(err_msg.data.time_err);
};

window.onload = function () {
  /*
일정 생성 클릭 시 실행 함수
input 태그를 배열로 가져와(inputs) 순서대로 변수에 저장
순서: startTime, endTime, location, title, content (이후 데이터 추가 시 순서 주의)
method: POST
return: err_msg
        에러 메세지 접근 방법: err_msg.data.{모델 필드 이름}_err
        에러가 아닌 경우 value 값에 "" 이 둘어가 있음.
        ex) err_msg.data.time_err
*/
  // let prevClickDate = document.querySelector(".today").parentNode;
  // prevClickDate.classList.add("date-onclick");
  // const requestExplan = new XMLHttpRequest();
  // function viewDetail() {
  //   const detailMember = document.querySelector(".detail-member");
  //   const day = this.childNodes[0].innerText;
  //   const url = "/view_explan/";
  //   requestExplan.open("POST", url, true);
  //   requestExplan.setRequestHeader(
  //     "Content-Type",
  //     "applcation/x-www-form-urlencoded"
  //   );
  //   requestExplan.send(
  //     JSON.stringify({
  //       year: currentYear,
  //       month: currentMonth,
  //       day: day,
  //       meetingName: "친구들", //-> 모임 이름 넣는 부분
  //     })
  //   );
  //   requestExplan.onreadystatechange = () => {
  //     if (requestExplan.readyState === XMLHttpRequest.DONE) {
  //       if (requestExplan.status < 400) {
  //         const { plans, username } = JSON.parse(requestExplan.response);
  //         const plansArray = JSON.parse(plans);
  //         const timeline = document.querySelector(".detail-timeline");
  //         const memberlist = document.querySelector(".detail-member");
  //         const newmember = document.createElement("div");
  //         memberlist.innerHTML = "";
  //         newmember.innerText = `${username}`;
  //         newmember.style.height = "50px";
  //         memberlist.appendChild(newmember);
  //         timeline.innerHTML = `<div class="detail-time">
  //         <div>0</div>
  //         <div>1</div>
  //         <div>2</div>
  //         <div>3</div>
  //         <div>4</div>
  //         <div>5</div>
  //         <div>6</div>
  //         <div>7</div>
  //         <div>8</div>
  //         <div>9</div>
  //         <div>10</div>
  //         <div>11</div>
  //         <div>12</div>
  //         <div>13</div>
  //         <div>14</div>
  //         <div>15</div>
  //         <div>16</div>
  //         <div>17</div>
  //         <div>18</div>
  //         <div>19</div>
  //         <div>20</div>
  //         <div>21</div>
  //         <div>22</div>
  //         <div>23</div>
  //         <div>24</div>
  //       </div>`;
  //         plansArray.forEach((plan) => {
  //           startTime = plan.fields.startTime;
  //           endTime = plan.fields.endTime;
  //           hours = endTime.slice(11, 13) - startTime.slice(11, 13);
  //           minutes = endTime.slice(14, 16) - startTime.slice(14, 16);
  //           let newplan = document.createElement("a");
  //           const start =
  //             parseInt(startTime.slice(11, 13) * 60) +
  //             parseInt(startTime.slice(14, 16));
  //           const width = hours * 60 + minutes;
  //           newplan.href = `plan/${plan.pk}`;
  //           newplan.style.position = "absolute";
  //           newplan.style.width = `${width}px`;
  //           newplan.style.left = `${start}px`;
  //           newplan.style.border = "1px solid black";
  //           newplan.style.backgroundColor = "black";
  //           newplan.style.color = "white";
  //           newplan.style.height = "50px";
  //           newplan.innerText = `${plan.fields.title}`;
  //           timeline.appendChild(newplan);
  //         });
  //       }
  //     }
  //   };
  //   prevClickDate.classList.remove("date-onclick");
  //   prevClickDate.classList.add("date");
  //   this.classList.remove("date");
  //   this.classList.add("date-onclick");
  //   prevClickDate = this;
  // }
  // let dateTarget = document.querySelectorAll(".date");
  // dateTarget.forEach((target) => target.addEventListener("click", viewDetail));
};
