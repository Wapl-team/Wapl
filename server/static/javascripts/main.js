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
  dates.forEach((date, i) => {
    // 삼한연산자 [조건문] ? [참일 때 실행] : [거짓일 때 실행]
    const condition =
      i >= firstDateIndex && i < lastDateIndex + 1 ? "this" : "other";
    //this
    //other

    dates[i] = `<div class="date"><p class="${condition}">${date}</p></div>`;
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

const meetingPK = document.querySelector(".meeting-pk").innerHTML;
const meetingName = document.querySelector(".meeting-name").innerHTML;
makeCalendar(meetingName, meetingPK);

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
  const url = "/create-private-plan";
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
  const selectObj = document.querySelectorAll("#share");

  data = selectObj.item(0).options;
  shareMeetingList = [];
  for (let i = 0; i < data.length; i++) {
    if (data[i].selected == true) {
      shareMeetingList.push(data[i].value);
    }
  }

  requestNewPlan.send(
    JSON.stringify({
      username: username,
      title: title,
      location: location,
      startTime: startTime,
      endTime: endTime,
      content: content,
      shareMeetings: shareMeetingList,
    })
  );
};

requestNewPlan.onreadystatechange = () => {
  if (requestNewPlan.readyState === XMLHttpRequest.DONE) {
    if (requestNewPlan.status < 400) {
      const { planName, startTime, endTime, pk, userimg } = JSON.parse(
        requestNewPlan.response
      );

      const newStartYear = startTime.slice(0, 4);
      const newStartMonth = startTime.slice(5, 7);
      const newStartDate = parseInt(startTime.slice(8, 10));

      const newEndYear = endTime.slice(0, 4);
      const newEndMonth = endTime.slice(5, 7);
      const newEndDate = parseInt(endTime.slice(8, 10));

      const currentPreview =
        document.querySelector(".date-onclick").childNodes[0].innerText;

      if (
        newStartYear <= currentYear &&
        currentYear <= newEndYear &&
        newStartMonth <= currentMonth &&
        currentMonth <= newEndMonth
      ) {
        const dateArray = document.querySelectorAll(".date, .date-onclick");
        dateArray.forEach((date) => {
          const thisdate = date.childNodes[0].innerText;
          if (
            parseInt(date.childNodes[0].innerText) <= newEndDate &&
            newStartDate <= parseInt(date.childNodes[0].innerText) &&
            date.childNodes[0].classList.contains("this")
          ) {
            if (
              !date.childNodes[1] ||
              !date.childNodes[1].classList.contains("private")
            ) {
              const newimg = document.createElement("img");
              newimg.classList.add("private");
              newimg.classList.add("profileImagePlan");
              newimg.src = `${userimg}`;
              newimg.style.width = "15px";
              date.childNodes[0].after(newimg);
            }
          }
        });
        if (currentPreview >= newStartDate && currentPreview <= newEndDate) {
          const timeline = document.querySelector(".detail-timeline");
          const memberlist = document.querySelector(".detail-member");

          if (timeline.childNodes.length == 0) {
            console.log("1");
            const newmember = document.createElement("div");
            memberlist.innerHTML = "";
            newmember.innerHTML = `<img class="profileImagePreview" src="${userimg}" width="40" />`;
            newmember.style.height = "50px";
            newmember.style.width = "50px";
            memberlist.appendChild(newmember);
            timeline.innerHTML = `<div class="detail-time">
          <div>0</div>
          <div>1</div>
          <div>2</div>
          <div>3</div>
          <div>4</div>
          <div>5</div>
          <div>6</div>
          <div>7</div>
          <div>8</div>
          <div>9</div>
          <div>10</div>
          <div>11</div>
          <div>12</div>
          <div>13</div>
          <div>14</div>
          <div>15</div>
          <div>16</div>
          <div>17</div>
          <div>18</div>
          <div>19</div>
          <div>20</div>
          <div>21</div>
          <div>22</div>
          <div>23</div>
        </div>`;
            let start = "";
            let hours = "";
            let minutes = "";
            if (parseInt(newEndDate) == parseInt(currentPreview)) {
              if (parseInt(newStartDate) < parseInt(currentPreview)) {
                // 앞쪽에서 부터 겹치는 경우
                start = 0;
                hours = endTime.slice(11, 13);
                minutes = endTime.slice(14, 16);
              } else if (parseInt(newStartDate) == parseInt(currentPreview)) {
                // 가운데 있는 경우

                start =
                  parseInt(startTime.slice(11, 13) * 60) +
                  parseInt(startTime.slice(14, 16));
                hours = endTime.slice(11, 13) - startTime.slice(11, 13);
                minutes = endTime.slice(14, 16) - startTime.slice(14, 16);
              }
            } else if (parseInt(newEndDate) > parseInt(currentPreview)) {
              if (parseInt(newStartDate) == parseInt(currentPreview)) {
                // 뒤로 겹치는 경우
                start =
                  parseInt(startTime.slice(11, 13) * 60) +
                  parseInt(startTime.slice(14, 16));
                if (startTime.slice(14, 16) == "00") {
                  minutes = "00";
                  hours = "24" - startTime.slice(11, 13);
                } else {
                  minutes = "60" - startTime.slice(14, 16);
                  hours = "23" - startTime.slice(11, 13);
                }
              } else if (parseInt(newStartDate) < parseInt(currentPreview)) {
                // 통으로 겹치는 경우
                start = 0;
                hours = "24";
                minutes = "00";
              }
            }
            let newDiv = document.createElement("div");
            newDiv.classList.add("private");
            newDiv.style.height = "50px";
            let newplan = document.createElement("a");
            const width = parseInt(hours) * 60 + parseInt(minutes);
            newplan.href = `plan/${pk}`;
            newplan.style.position = "absolute";
            newplan.style.width = `${width}px`;
            newplan.style.left = `${start}px`;
            newplan.style.border = "1px solid black";
            newplan.style.backgroundColor = "white";
            newplan.style.color = "black";
            newplan.style.height = "50px";
            newplan.innerText = `${planName}`;
            newDiv.appendChild(newplan);
            timeline.appendChild(newDiv);
          } else if (timeline.childNodes[1].classList.contains("private")) {
            console.log("2");
            let start = "";
            let hours = "";
            let minutes = "";
            if (parseInt(newEndDate) == parseInt(currentPreview)) {
              if (parseInt(newStartDate) < parseInt(currentPreview)) {
                // 앞쪽에서 부터 겹치는 경우
                start = 0;
                hours = endTime.slice(11, 13);
                minutes = endTime.slice(14, 16);
              } else if (parseInt(newStartDate) == parseInt(currentPreview)) {
                // 가운데 있는 경우

                start =
                  parseInt(startTime.slice(11, 13) * 60) +
                  parseInt(startTime.slice(14, 16));
                hours = endTime.slice(11, 13) - startTime.slice(11, 13);
                minutes = endTime.slice(14, 16) - startTime.slice(14, 16);
              }
            } else if (parseInt(newEndDate) > parseInt(currentPreview)) {
              if (parseInt(newStartDate) == parseInt(currentPreview)) {
                // 뒤로 겹치는 경우
                start =
                  parseInt(startTime.slice(11, 13) * 60) +
                  parseInt(startTime.slice(14, 16));
                if (startTime.slice(14, 16) == "00") {
                  minutes = "00";
                  hours = "24" - startTime.slice(11, 13);
                } else {
                  minutes = "60" - startTime.slice(14, 16);
                  hours = "23" - startTime.slice(11, 13);
                }
              } else if (parseInt(newStartDate) < parseInt(currentPreview)) {
                // 통으로 겹치는 경우
                start = 0;
                hours = "24";
                minutes = "00";
              }
            }
            let newplan = document.createElement("a");
            const width = parseInt(hours) * 60 + parseInt(minutes);
            newplan.href = `plan/${pk}`;
            newplan.style.position = "absolute";
            newplan.style.width = `${width}px`;
            newplan.style.left = `${start}px`;
            newplan.style.border = "1px solid black";
            newplan.style.backgroundColor = "white";
            newplan.style.color = "black";
            newplan.style.height = "50px";
            newplan.innerText = `${planName}`;
            timeline.childNodes[1].appendChild(newplan);
          } else {
            console.log("3");
            const newmember = document.createElement("div");
            newmember.innerHTML = `<img class="profileImagePreview" src="${userimg}" width="40" />`;
            newmember.style.height = "50px";
            newmember.style.width = "50px";
            memberlist.firstChild.before(newmember);

            let start = "";
            let hours = "";
            let minutes = "";
            if (parseInt(newEndDate) == parseInt(currentPreview)) {
              if (parseInt(newStartDate) < parseInt(currentPreview)) {
                // 앞쪽에서 부터 겹치는 경우
                start = 0;
                hours = endTime.slice(11, 13);
                minutes = endTime.slice(14, 16);
              } else if (parseInt(newStartDate) == parseInt(currentPreview)) {
                // 가운데 있는 경우

                start =
                  parseInt(startTime.slice(11, 13) * 60) +
                  parseInt(startTime.slice(14, 16));
                hours = endTime.slice(11, 13) - startTime.slice(11, 13);
                minutes = endTime.slice(14, 16) - startTime.slice(14, 16);
              }
            } else if (parseInt(newEndDate) > parseInt(currentPreview)) {
              if (parseInt(newStartDate) == parseInt(currentPreview)) {
                // 뒤로 겹치는 경우
                start =
                  parseInt(startTime.slice(11, 13) * 60) +
                  parseInt(startTime.slice(14, 16));
                if (startTime.slice(14, 16) == "00") {
                  minutes = "00";
                  hours = "24" - startTime.slice(11, 13);
                } else {
                  minutes = "60" - startTime.slice(14, 16);
                  hours = "23" - startTime.slice(11, 13);
                }
              } else if (parseInt(newStartDate) < parseInt(currentPreview)) {
                // 통으로 겹치는 경우
                start = 0;
                hours = "24";
                minutes = "00";
              }
            }
            let newDiv = document.createElement("div");
            newDiv.classList.add("private");
            newDiv.style.height = "50px";
            let newplan = document.createElement("a");
            const width = parseInt(hours) * 60 + parseInt(minutes);
            newplan.href = `plan/${pk}`;
            newplan.style.position = "absolute";
            newplan.style.width = `${width}px`;
            newplan.style.left = `${start}px`;
            newplan.style.border = "1px solid black";
            newplan.style.backgroundColor = "white";
            newplan.style.color = "black";
            newplan.style.height = "50px";
            newplan.innerText = `${planName}`;
            newDiv.appendChild(newplan);
            timeline.childNodes[1].before(newDiv);
          }
        }
      }
      document.getElementById("plan_title").value = "";
      document.getElementById("plan_location").value = "";
      document.getElementById("plan_startTime").value = "";
      document.getElementById("plan_endTime").value = "";
      document.getElementById("plan_content").value = "";
    }
  }
};

function openToggle() {
  document.getElementById("sidebar").style.width = "250px";
  document.getElementById("sidebar").style.border = "2px solid orange";
  document.getElementById("sidebar").style.borderLeft = "none";
  document.getElementById("sidebar").style.borderTop = "none";
  document.getElementById("sidebar").style.borderBottom = "none";
}

function closeToggle() {
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("sidebar").style.border = "none";
  document.getElementById("sidebar").style.borderLeft = "none";
  document.getElementById("sidebar").style.borderTop = "none";
  document.getElementById("sidebar").style.borderBottom = "none";
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
};

window.onload = function () {
  const requestPlan = new XMLHttpRequest();
  const url = "/view_plan/";
  requestPlan.open("POST", url, true);
  requestPlan.setRequestHeader(
    "Content-Type",
    "applcation/x-www-form-urlencoded"
  );

  //meeting: 현재 유저가 보고 있는 모임 이름(meeting_name)
  requestPlan.send(
    JSON.stringify({
      year: currentYear,
      month: currentMonth,
    })
  );
  requestPlan.onreadystatechange = () => {
    if (requestPlan.readyState === XMLHttpRequest.DONE) {
      if (requestPlan.status < 400) {
        const { public_plans, private_plans, userimg, meetingimg } = JSON.parse(
          requestPlan.response
        );

        const publicPlansArray = JSON.parse(public_plans);
        const privatePlansArray = JSON.parse(private_plans);
        // let isPlan = new Array(
        //   new Date(currentYear, currentMonth, 0).getDate()
        // ).fill(false);
        // plansArray.forEach((plan) => {
        //   const startDay = parseInt(
        //     plan.fields.startTime[8] + plan.fields.startTime[9]
        //   );
        //   const endDay = parseInt(
        //     plan.fields.endTime[8] + plan.fields.endTime[9]
        //   );
        //   for (let i = startDay; i <= endDay; i++) {
        //     isPlan[i] = true;
        //   }
        // });
        const currentDays = document.querySelectorAll(".this");
        currentDays.forEach((day) => {
          privatePlansArray.forEach((plan) => {
            const startTime = new Date(plan.fields.startTime);
            const endTime = new Date(plan.fields.endTime);
            const today = new Date(
              currentYear,
              currentMonth - 1,
              day.innerText
            );
            if (
              startTime.setHours(0, 0, 0, 0) <= today &&
              today <= endTime.setHours(0, 0, 0, 0)
            ) {
              if (day.nextSibling == null) {
                const newImg = document.createElement("img");
                newImg.classList.add(`private`);
                newImg.classList.add(`profileImagePlan`);
                newImg.src = `${userimg}`;
                newImg.style.width = "15px";
                day.parentElement.appendChild(newImg);
                // day.after(newImg);
              }
            }
          });
          let already = [];
          publicPlansArray.forEach((plan) => {
            const startTime = new Date(plan.fields.startTime);
            const endTime = new Date(plan.fields.endTime);
            const today = new Date(
              currentYear,
              currentMonth - 1,
              day.innerText
            );
            if (
              startTime.setHours(0, 0, 0, 0) <= today &&
              today <= endTime.setHours(0, 0, 0, 0)
            ) {
              if (already.indexOf(`${plan.fields.meetings}`) == -1) {
                const newImg = document.createElement("img");
                meetingimg[plan.fields.meetings];
                newImg.src = `${meetingimg[plan.fields.meetings]}`;
                newImg.classList.add("profileImagePlan");
                newImg.alt = `${plan.fields.title}`;
                newImg.style.width = "15px";
                day.parentElement.appendChild(newImg);
                already.push(`${plan.fields.meetings}`);
              }
            }
          });
        });
      }
    }
  };
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
  let prevClickDate = document.querySelector(".today").parentNode;
  prevClickDate.classList.add("date-onclick");
  const requestExplan = new XMLHttpRequest();
  function viewDetail() {
    const day = this.childNodes[0].innerText;
    const url = "/view_explan/";
    requestExplan.open("POST", url, true);
    requestExplan.setRequestHeader(
      "Content-Type",
      "applcation/x-www-form-urlencoded"
    );
    requestExplan.send(
      JSON.stringify({
        year: currentYear,
        month: currentMonth,
        day: day,
      })
    );
    requestExplan.onreadystatechange = () => {
      if (requestExplan.readyState === XMLHttpRequest.DONE) {
        if (requestExplan.status < 400) {
          const { public_plans, private_plans, today, userimg, meetingimg } =
            JSON.parse(requestExplan.response);
          const publicPlansArray = JSON.parse(public_plans);
          const privatePlansArray = JSON.parse(private_plans);
          const timeline = document.querySelector(".detail-timeline");
          const memberlist = document.querySelector(".detail-member");
          if (publicPlansArray.length != 0 || privatePlansArray.length != 0) {

            memberlist.innerHTML = "";
            timeline.innerHTML = `<div class="detail-time">
          <div>0</div>
          <div>1</div>
          <div>2</div>
          <div>3</div>
          <div>4</div>
          <div>5</div>
          <div>6</div>
          <div>7</div>
          <div>8</div>
          <div>9</div>
          <div>10</div>
          <div>11</div>
          <div>12</div>
          <div>13</div>
          <div>14</div>
          <div>15</div>
          <div>16</div>
          <div>17</div>
          <div>18</div>
          <div>19</div>
          <div>20</div>
          <div>21</div>
          <div>22</div>
          <div>23</div>
        </div>`;
            if (privatePlansArray.length != 0) {
              let newDiv = document.createElement("div");
              newDiv.classList.add("private");
              newDiv.style.height = "50px";
              const newmember = document.createElement("div");
              newmember.innerHTML = `<img class="profileImagePreview"src="${userimg}" width="40" />`;
              newmember.style.height = "50px";
              newmember.style.width = "50px";
              memberlist.appendChild(newmember);

              privatePlansArray.forEach((plan) => {
                endTime = plan.fields.endTime;
                endDay = endTime.slice(8, 10);
                startTime = plan.fields.startTime;
                startDay = startTime.slice(8, 10);
                let start = "";
                let hours = "";
                let minutes = "";
                if (parseInt(endDay) == parseInt(today)) {
                  if (parseInt(startDay) < parseInt(today)) {
                    // 앞쪽에서 부터 겹치는 경우
                    start = 0;
                    hours = endTime.slice(11, 13);
                    minutes = endTime.slice(14, 16);
                  } else if (parseInt(startDay) == parseInt(today)) {
                    // 가운데 있는 경우

                    start =
                      parseInt(startTime.slice(11, 13) * 60) +
                      parseInt(startTime.slice(14, 16));
                    hours = endTime.slice(11, 13) - startTime.slice(11, 13);
                    minutes = endTime.slice(14, 16) - startTime.slice(14, 16);
                  }
                } else if (parseInt(endDay) > parseInt(today)) {
                  if (parseInt(startDay) == parseInt(today)) {
                    // 뒤로 겹치는 경우
                    start =
                      parseInt(startTime.slice(11, 13) * 60) +
                      parseInt(startTime.slice(14, 16));
                    if (startTime.slice(14, 16) == "00") {
                      minutes = "00";
                      hours = "24" - startTime.slice(11, 13);
                    } else {
                      minutes = "60" - startTime.slice(14, 16);
                      hours = "23" - startTime.slice(11, 13);
                    }
                  } else if (parseInt(startDay) < parseInt(today)) {
                    // 통으로 겹치는 경우
                    start = 0;
                    hours = "24";
                    minutes = "00";
                  }
                }
                newDiv.style.height = "50px";
                let newplan = document.createElement("a");
                const width = parseInt(hours) * 60 + parseInt(minutes);
                newplan.href = `plan/${plan.pk}`;
                newplan.style.position = "absolute";
                newplan.style.width = `${width}px`;
                newplan.style.left = `${start}px`;
                newplan.style.border = "1px solid black";
                newplan.style.backgroundColor = "white";
                newplan.style.color = "black";
                newplan.style.height = "50px";
                newplan.innerText = `${plan.fields.title}`;
                newDiv.appendChild(newplan);
                timeline.appendChild(newDiv);
              });
            }
            let already = [];
            publicPlansArray.forEach((plan) => {
              if (already.indexOf(`${plan.fields.meetings}`) == -1) {
                const newmember = document.createElement("div");
                newmember.innerHTML = `<img class="profileImagePreview"src="${
                  meetingimg[plan.fields.meetings]
                }" width="40" />`;
                newmember.style.height = "50px";
                newmember.style.width = "50px";
                memberlist.appendChild(newmember);
                let newDiv = document.createElement("div");
                newDiv.style.height = "50px";
                newDiv.classList.add(`meeting-${plan.fields.meetings}`);
                timeline.appendChild(newDiv);
                already.push(`${plan.fields.meetings}`);
              }
              endTime = plan.fields.endTime;
              endDay = endTime.slice(8, 10);
              startTime = plan.fields.startTime;
              startDay = startTime.slice(8, 10);
              let start = "";
              let hours = "";
              let minutes = "";
              if (parseInt(endDay) == parseInt(today)) {
                if (parseInt(startDay) < parseInt(today)) {
                  // 앞쪽에서 부터 겹치는 경우
                  start = 0;
                  hours = endTime.slice(11, 13);
                  minutes = endTime.slice(14, 16);
                } else if (parseInt(startDay) == parseInt(today)) {
                  // 가운데 있는 경우

                  start =
                    parseInt(startTime.slice(11, 13) * 60) +
                    parseInt(startTime.slice(14, 16));
                  hours = endTime.slice(11, 13) - startTime.slice(11, 13);
                  minutes = endTime.slice(14, 16) - startTime.slice(14, 16);
                }
              } else if (parseInt(endDay) > parseInt(today)) {
                if (parseInt(startDay) == parseInt(today)) {
                  // 뒤로 겹치는 경우
                  start =
                    parseInt(startTime.slice(11, 13) * 60) +
                    parseInt(startTime.slice(14, 16));
                  if (startTime.slice(14, 16) == "00") {
                    minutes = "00";
                    hours = "24" - startTime.slice(11, 13);
                  } else {
                    minutes = "60" - startTime.slice(14, 16);
                    hours = "23" - startTime.slice(11, 13);
                  }
                } else if (parseInt(startDay) < parseInt(today)) {
                  // 통으로 겹치는 경우
                  start = 0;
                  hours = "24";
                  minutes = "00";
                }
              }

              let newplan = document.createElement("a");
              const width = parseInt(hours) * 60 + parseInt(minutes);
              newplan.href = `plan/${plan.pk}`;
              newplan.style.position = "absolute";
              newplan.style.width = `${width}px`;
              newplan.style.left = `${start}px`;
              newplan.style.border = "1px solid black";
              newplan.style.backgroundColor = "white";
              newplan.style.color = "black";
              newplan.style.height = "50px";
              newplan.innerText = `${plan.fields.title}`;
              document
                .querySelector(`.meeting-${plan.fields.meetings}`)
                .appendChild(newplan);
            });
          } else {
            timeline.innerHTML = "";
            memberlist.innerHTML = "";
          }
        }
      }
    };
    prevClickDate.classList.remove("date-onclick");
    prevClickDate.classList.add("date");
    this.classList.remove("date");
    this.classList.add("date-onclick");
    prevClickDate = this;
  }
  let dateTarget = document.querySelectorAll(".date");
  dateTarget.forEach((target) => target.addEventListener("click", viewDetail));
};

const makeMeetingList = (meetingList) => {
  const menu = document.querySelector("#share");

  let contentString = "";
  meetingList.forEach((meeting) => {
    contentString += `<option value="${meeting.fields.meeting_name}">${meeting.fields.meeting_name}</option>`;
  });

  menu.innerHTML = contentString;
};
