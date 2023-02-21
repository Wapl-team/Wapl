let date = new Date();
let currentYear = date.getFullYear();
let currentMonth = date.getMonth() + 1;

const timeline = document.querySelector(".timeline");
const memberlist = document.querySelector(".detail-member");
const detailtime = document.querySelector(".detail-time");

// 타임라인 바 길이 계산 함수
function calcTime(startDatetime, endDatetime, currentDatetime) {
  let start = "";
  let hours = "";
  let minutes = "";

  const startDate = new Date(startDatetime);
  startDate.setHours(0, 0, 0, 0);
  const endDate = new Date(endDatetime);
  endDate.setHours(0, 0, 0, 0);

  const currentDate = new Date(viewYear, viewMonth - 1, currentDatetime);

  if (
    endDate.getFullYear() == currentDate.getFullYear() &&
    endDate.getMonth() == currentDate.getMonth() &&
    endDate.getDate() == currentDate.getDate()
  ) {
    // 앞쪽에서부터 겹치는 경우

    if (startDate < currentDate) {
      start = 0;
      hours = endDatetime.getHours();
      minutes = endDatetime.getMinutes();
    }
    // 가운데에 있는 경우
    else if (
      startDate.getFullYear() == currentDate.getFullYear() &&
      startDate.getMonth() == currentDate.getMonth() &&
      startDate.getDate() == currentDate.getDate()
    ) {
      start =
        parseInt(startDatetime.getHours() * 60) +
        parseInt(startDatetime.getMinutes());
      hours = endDatetime.getHours() - startDatetime.getHours();
      minutes = endDatetime.getMinutes() - startDatetime.getMinutes();
    }
  } else if (endDate > currentDate) {
    // 뒤로 겹치는 경우

    if (
      startDate.getFullYear() == currentDate.getFullYear() &&
      startDate.getMonth() == currentDate.getMonth() &&
      startDate.getDate() == currentDate.getDate()
    ) {
      start =
        parseInt(startDatetime.getHours() * 60) +
        parseInt(startDatetime.getMinutes());
      if (startDatetime.getMinutes() == "00") {
        minutes = "00";
        hours = "24" - startDatetime.getHours();
      } else {
        minutes = "60" - startDatetime.getMinutes();
        hours = "23" - startDatetime.getHours();
      }
    }
    // 통으로 겹치는 경우
    else if (startDate < currentDate) {
      start = 0;
      hours = "24";
      minutes = "00";
    }
  }
  return [start, hours, minutes];
}

function clearPlanForm() {
  document.getElementById("plan_title").value = "";
  document.getElementById("plan_location").value = "";
  document.getElementById("plan_startTime").value = "";
  document.getElementById("plan_endTime").value = "";
  document.getElementById("plan_content").value = "";
}
function openToggle() {
  // document.getElementById("sidebar").style.width = "250px";
  // document.getElementById("sidebar").style.paddingTop = "2rem";
  // document.getElementById("sidebar").style.paddingBottom = "2rem";
  document.getElementById("sidebar").style.visibility = "visible";
  document.getElementById("sidebar").style.transition = "all 0.1s";
  document.getElementById("sidebar").style.opacity = "1";
}

function closeToggle() {
  // document.getElementById("sidebar").style.width = "0";
  // document.getElementById("sidebar").style.paddingTop = "0";
  // document.getElementById("sidebar").style.paddingBottom = "0";
  document.getElementById("sidebar").style.visibility = "hidden";
  document.getElementById("sidebar").style.transition = "all 0.1s";
  document.getElementById("sidebar").style.opacity = "0";
  document.getElementById("sidebar").style.paddingTop = "1rem";
  document.getElementById("sidebar").style.paddingBottom = "3rem";
}
const navBtn = document.querySelector(".nav_bar_button");
const sidebarMenu = document.querySelector(".sidebar-menu");
const closeBtn = document.querySelector(".closeBtn");
const mainCalendar = document.querySelector(".main");
const meetingName = document.querySelector(".meeting-name");
const displayYM = document.querySelector(".year_month_display");

navBtn.addEventListener("click", () => {
  openToggle();
});

closeBtn.addEventListener("click", () => {
  closeToggle();
});

sidebarMenu.addEventListener("click", (e) => {
  closeToggle();
});

mainCalendar.addEventListener("click", (e) => {
  closeToggle();
});

meetingName.addEventListener("click", (e) => {
  closeToggle();
});
displayYM.addEventListener("click", (e) => {
  closeToggle();
});

// const makeMeetingList = (meetingList) => {
//   const menu = document.querySelector("#share");

//   let contentString = "";
//   meetingList.forEach((meeting) => {
//     contentString += `<option value="${meeting.fields.meeting_name}">${meeting.fields.meeting_name}</option>`;
//   });
//   menu.innerHTML = contentString;
// };

// 캘린더에 보이는 년도와 달을 보여주기 위해
// const viewYear = date.getFullYear();
// const viewMonth = date.getMonth();
const makeCalendar = (viewYear, viewMonth) => {
  currentYear = viewYear;
  currentMonth = viewMonth;
  viewMonth -= 1;

  // 캘린더 년도 달 채우기
  // document.querySelector(".year-month").textContent = `${viewYear}년 ${
  //   viewMonth + 1
  // }월`;

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
    const date_condition =
      i >= firstDateIndex && i < lastDateIndex + 1 ? `day-${date}` : "";
    //this
    //other

    dates[
      i
    ] = `<div class="date"><p class="${condition} ${date_condition}">${date}</p></div>`;
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
  } else {
    document.querySelector(".day-1").classList.add("today");
  }
};

const viewDate = document.querySelector(".year-month").innerHTML.split("년");
const viewYear = parseInt(viewDate[0]);
const viewMonth = parseInt(viewDate[1].substring(0, 2));

console.log(viewMonth, viewYear);
makeCalendar(viewYear, viewMonth);

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
// const curMonth = () => {
//   date = new Date();
//   makeCalendar();
// };

// 일정 생성 모달 관련
const modalButton = document.querySelector(".modalButton");
const modal = document.querySelector(".modal");
const modal_content = document.querySelector(".modal__content");
const closeModal = document.querySelector(".closeModal_x");
const closeModal2 = document.querySelector(".closeModal2");
const share = document.querySelector(".share");
const modal_share = document.querySelector(".modal-share");
const share_box = document.querySelector(".share-box");

share.addEventListener("click", () => {
  modal_share.classList.remove("hidden");
});

modal.addEventListener("click", (e) => {
  if (e.target == modal) {
    modal.classList.add("hidden");
  }
});

modal_share.addEventListener("click", (e) => {
  if (e.target == modal_share) {
    modal_share.classList.add("hidden");
  }
});

modalButton.addEventListener("click", () => {
  modal.classList.remove("hidden");
});

// closeModal.addEventListener("click", () => {
//   modal.classList.add("hidden");
// });
closeModal2.addEventListener("click", () => {
  modal.classList.add("hidden");
});

let shareOBJ = {};

const share_save = () => {
  const share_select = document.querySelectorAll(".share-select input");
  share_select.forEach((share) => {
    if (share.checked == true) {
      shareOBJ[share.id.split("-")[0]] = share.id.split("-")[1];
    }
  });
  modal_share.classList.add("hidden");
};

// 새로운 일정 추가하는 함수:
// ajax사용해서 thumbnail 띄우고
// 현재 보고있는 preview에 일정 추가시 해당 preview에도 ajax
const plan_create = () => {
  const requestNewPlan = new XMLHttpRequest();
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

  requestNewPlan.send(
    JSON.stringify({
      title: title,
      location: location,
      startTime: startTime,
      endTime: endTime,
      content: content,
      shareMeetings: shareOBJ,
    })
  );

  requestNewPlan.onreadystatechange = () => {
    if (requestNewPlan.readyState === XMLHttpRequest.DONE) {
      if (requestNewPlan.status < 400) {
        const { plan, userimg, username, err_msg } = JSON.parse(
          requestNewPlan.response
        );

        //validation 통과하여 일정 등록이 가능한 경우
        if (plan != null && userimg != null) {
          shareOBJ = {};
          const startDate = new Date(startTime);
          const endDate = new Date(endTime);

          const current_preview = new Date(
            currentYear,
            currentMonth - 1,
            document.querySelector(".date-onclick").childNodes[0].innerText
          );

          let this_date = new Date(
            startDate.getFullYear(),
            startDate.getMonth(),
            startDate.getDate()
          );

          while (true) {
            if (
              this_date.getFullYear() == viewYear &&
              this_date.getMonth() + 1 == viewMonth
            ) {
              const day = document.querySelector(`.day-${this_date.getDate()}`);
              if (
                !day.nextSibling ||
                !day.nextSibling.classList.contains("private")
              ) {
                const newimg = document.createElement("img");
                newimg.classList.add("private");
                newimg.classList.add("profileImagePlan");
                newimg.src = `${userimg}`;
                newimg.style.width = "12px";
                newimg.style.height = "12px";
                newimg.style.margin = "0px 1px";
                day.after(newimg);
                if (day.parentNode.childNodes.length == 6) {
                  day.parentNode.childNodes[5].remove();
                  const thumbnail_overflow = document.createElement("div");
                  thumbnail_overflow.style.width = "30px";
                  thumbnail_overflow.style.height = "12px";
                  thumbnail_overflow.style.margin = "0px 1px";
                  thumbnail_overflow.style.fontSize = "0.7rem";
                  thumbnail_overflow.classList.add(
                    `thumbnail-overflow-${day.innerText}`
                  );
                  thumbnail_overflow.style.borderRadius = "5px";
                  thumbnail_overflow.style.backgroundColor = "white";
                  thumbnail_overflow.style.boxShadow =
                    "1px 1px 2px rgb(0 0 0 / 14%)";
                  thumbnail_overflow.innerText = "+1";
                  day.parentElement.appendChild(thumbnail_overflow);
                } else if (day.parentNode.childNodes.length > 6) {
                  day.parentNode.childNodes[5].remove();
                  document.querySelector(
                    `.thumbnail-overflow-${day.innerText}`
                  ).innerText = `+${day.parentNode.childNodes.length - 4}`;
                }
              }
            }
            if (
              this_date.getFullYear() == endDate.getFullYear() &&
              this_date.getMonth() == endDate.getMonth() &&
              this_date.getDate() == endDate.getDate()
            ) {
              break;
            } else {
              this_date.setDate(this_date.getDate() + 1);
            }
          }

          const current_dateonly = new Date(current_preview).setHours(
            0,
            0,
            0,
            0
          );
          const start_dateonly = new Date(startDate).setHours(0, 0, 0, 0);
          const end_dateonly = new Date(endDate).setHours(0, 0, 0, 0);

          // 새로운 일정이 내가 현재 보고 있는 날짜에 포함된다면 preview 추가
          if (
            current_dateonly >= start_dateonly &&
            current_dateonly <= end_dateonly
          ) {
            let start = "";
            let hours = "";
            let minutes = "";
            if (timeline.childNodes[0]) {
              // 이미 timeline에 개인일정이 있는 경우
              if (
                timeline.childNodes[0].classList.contains("private-timeline")
              ) {
                [start, hours, minutes] = calcTime(
                  startDate,
                  endDate,
                  current_preview.getDate()
                );
                let newplan = document.createElement("a");
                const width = parseInt(hours) * 60 + parseInt(minutes);
                newplan.href = `plan/${plan.id}`;
                newplan.style.position = "absolute";
                newplan.style.width = `${(width * 100) / 1440}%`;
                newplan.style.left = `${(start * 100) / 1440}%`;
                // newplan.style.border = "1px solid orange";
                newplan.style.backgroundColor = "#FBFBFB";
                newplan.style.color = "#1A2634";
                newplan.style.height = "40px";
                newplan.style.borderRadius = "10px";
                newplan.style.boxShadow = "1px 1px 2px rgb(0 0 0 / 14%)";
                newplan.style.padding = "11px";
                newplan.style.fontSize = "0.7rem";
                newplan.style.overflow = "hidden";
                newplan.style.whiteSpace = "nowrap";
                newplan.style.textOverflow = "ellipsis";
                newplan.innerText = `${plan.title}`;
                timeline.childNodes[0].appendChild(newplan);
              }
              // timeline에 팀일정만 있는경우
              else {
                // 개인 일정 라인추가
                const newmember = document.createElement("div");
                newmember.innerHTML = `<img class="profileImagePreview" src="${userimg}" border-radius="25px" width="32px" height="32px"/>`;
                newmember.style.height = "50px";
                newmember.style.width = "43px";
                const new_user_name = document.createElement("p");
                new_user_name.classList.add("profile-user-name");
                new_user_name.textContent = `${username}`;
                newmember.appendChild(new_user_name);
                memberlist.firstChild.before(newmember);

                [start, hours, minutes] = calcTime(
                  startDate,
                  endDate,
                  current_preview.getDate()
                );

                // 추가한 일정 타임라인 추가
                let newDiv = document.createElement("div");
                newDiv.classList.add("private");
                newDiv.style.height = "50px";
                let newplan = document.createElement("a");
                const width = parseInt(hours) * 60 + parseInt(minutes);
                newplan.href = `plan/${plan.id}`;
                newplan.style.position = "absolute";
                newplan.style.width = `${(width * 100) / 1440}%`;
                newplan.style.left = `${(start * 100) / 1440}%`;
                // newplan.style.border = "1px solid orange";
                newplan.style.backgroundColor = "#FBFBFB";
                newplan.style.color = "#1A2634";
                newplan.style.height = "40px";
                newplan.style.borderRadius = "10px";
                newplan.style.boxShadow = "1px 1px 2px rgb(0 0 0 / 14%)";
                newplan.style.padding = "11px";
                newplan.style.fontSize = "0.7rem";
                newplan.style.overflow = "hidden";
                newplan.style.whiteSpace = "nowrap";
                newplan.style.textOverflow = "ellipsis";
                newplan.innerText = `${plan.title}`;
                newDiv.appendChild(newplan);
                timeline.childNodes[0].before(newDiv);
              }
            }
            // timeline에 아무일정도 없는 경우
            else {
              // 개인 일정 라인추가
              const newmember = document.createElement("div");
              newmember.innerHTML = `<img class="profileImagePreview" src="${userimg}" border-radius="25px" width="32px" height="32px"/>`;
              newmember.style.height = "50px";
              newmember.style.width = "43px";
              const new_user_name = document.createElement("p");
              new_user_name.classList.add("profile-user-name");
              new_user_name.textContent = `${username}`;
              newmember.appendChild(new_user_name);
              memberlist.appendChild(newmember);

              [start, hours, minutes] = calcTime(
                startDate,
                endDate,
                current_preview.getDate()
              );

              let newDiv = document.createElement("div");
              newDiv.classList.add("private-timeline");
              newDiv.style.height = "50px";
              let newplan = document.createElement("a");
              const width = parseInt(hours) * 60 + parseInt(minutes);
              newplan.href = `plan/${plan.id}`;
              newplan.style.position = "absolute";
              newplan.style.width = `${(width * 100) / 1440}%`;
              newplan.style.left = `${(start * 100) / 1440}%`;
              // newplan.style.border = "1px solid orange";
              newplan.style.backgroundColor = "#FBFBFB";
              newplan.style.color = "#1A2634";
              newplan.style.height = "40px";
              newplan.style.borderRadius = "10px";
              newplan.style.boxShadow = "1px 1px 2px rgb(0 0 0 / 14%)";
              newplan.style.padding = "11px";
              newplan.style.fontSize = "0.7rem";
              newplan.style.overflow = "hidden";
              newplan.style.whiteSpace = "nowrap";
              newplan.style.textOverflow = "ellipsis";
              newplan.innerText = `${plan.title}`;
              newDiv.appendChild(newplan);
              timeline.appendChild(newDiv);
            }
          }
        } else {
          //view에서 validation 통과 못하면 이쪽으로 옴
          alert(err_msg);
        }
      }
      clearPlanForm();
    }
  };
};

window.onload = function () {
  // 달력 모두 load 됐을 시 해당 달 thumbnail 출력
  const requestPlan = new XMLHttpRequest();
  const url = "/view_plan/";
  requestPlan.open("POST", url, true);
  requestPlan.setRequestHeader(
    "Content-Type",
    "applcation/x-www-form-urlencoded"
  );

  requestPlan.send(
    JSON.stringify({
      year: currentYear,
      month: currentMonth,
    })
  );
  requestPlan.onreadystatechange = () => {
    if (requestPlan.readyState === XMLHttpRequest.DONE) {
      if (requestPlan.status < 400) {
        const {
          public_plans,
          private_plans,
          userimg,
          meetingimg,
          meetingList,
          attend_dict,
        } = JSON.parse(requestPlan.response);
        // makeMeetingList(JSON.parse(meetingList));

        const publicPlansArray = JSON.parse(public_plans);
        const privatePlansArray = JSON.parse(private_plans);

        const thismonthDates = document.querySelectorAll(".this");
        // 현재 달력의 갈 날짜를 돌면서
        // 각 plan에 포함되는지 확인한 후
        // 확인된 날짜에서 thumbnail 추가
        // 개인일정이 위쪽에 와야하므로 먼저 추가
        thismonthDates.forEach((day) => {
          let count = 0;

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
                newImg.style.width = "12px";
                newImg.style.height = "12px";
                newImg.style.margin = "0px 1px";
                day.parentElement.appendChild(newImg);
                count += 1;
              }
            }
          });
          // 이미 추가된 모임의 썸네일인지 확인
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
                if (count <= 3) {
                  const newImg = document.createElement("img");
                  meetingimg[plan.fields.meetings];
                  newImg.src = `${meetingimg[plan.fields.meetings]}`;
                  newImg.classList.add("profileImagePlan");
                  newImg.style.width = "12px";
                  newImg.style.height = "12px";
                  newImg.style.margin = "0px 1px";
                  if (attend_dict[plan.pk] == "standby") {
                    newImg.style.border = "1px solid red";
                  }
                  day.parentElement.appendChild(newImg);
                  already.push(`${plan.fields.meetings}`);
                  count += 1;
                } else if (count == 4) {
                  const thumbnail_overflow = document.createElement("div");
                  thumbnail_overflow.style.width = "30px";
                  thumbnail_overflow.style.height = "12px";
                  thumbnail_overflow.style.margin = "0px 1px";
                  thumbnail_overflow.style.fontSize = "0.7rem";
                  thumbnail_overflow.classList.add(
                    `thumbnail-overflow-${day.innerText}`
                  );
                  thumbnail_overflow.style.borderRadius = "5px";
                  thumbnail_overflow.style.backgroundColor = "white";
                  thumbnail_overflow.style.boxShadow =
                    "1px 1px 2px rgb(0 0 0 / 14%)";
                  thumbnail_overflow.innerText = "+1";
                  day.parentElement.appendChild(thumbnail_overflow);
                  count += 1;
                } else {
                  document.querySelector(
                    `.thumbnail-overflow-${day.innerText}`
                  ).innerText = `+${count - 3}`;
                  count += 1;
                }
              }
            }
          });
        });
      }
    }
  };

  // 전에 선택되었던 날짜 확인
  // date-onclick 없애기 위함
  let prevClickDate = document.querySelector(".today").parentNode;
  prevClickDate.classList.add("date-onclick");

  // onclick시 달력 아래에 타임라인 출력
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
          const {
            public_plans,
            private_plans,
            today,
            userimg,
            meetingimg,
            private_user_names,
            public_user_names,
            attend_dict,
          } = JSON.parse(requestExplan.response);
          const publicPlansArray = JSON.parse(public_plans);
          const privatePlansArray = JSON.parse(private_plans);
          memberlist.innerHTML = "";
          timeline.innerHTML = ``;

          // 이미 타임라인에 있는 라인인지 확인
          let already = [];
          privatePlansArray.forEach((plan) => {
            if (already.indexOf(`private`) == -1) {
              let newDiv = document.createElement("div");
              newDiv.classList.add("private-timeline");
              newDiv.style.height = "50px";
              timeline.appendChild(newDiv);
              const newmember = document.createElement("div");
              newmember.innerHTML = `<img class="profileImagePreview "src="${userimg}" border-radius="25px" width="32px" height="32px" />`;

              const new_user_name = document.createElement("p");
              new_user_name.classList.add("profile-user-name");
              new_user_name.textContent = `${
                private_user_names[plan.fields.owner]
              }`;
              newmember.appendChild(new_user_name);

              newmember.style.height = "50px";
              newmember.style.width = "43px";
              memberlist.appendChild(newmember);
              already.push(`private`);
            }
            const startDate = new Date(plan.fields.startTime);
            const endDate = new Date(plan.fields.endTime);

            let start = "";
            let hours = "";
            let minutes = "";

            [start, hours, minutes] = calcTime(startDate, endDate, today);

            let newplan = document.createElement("a");
            const width = parseInt(hours) * 60 + parseInt(minutes);
            newplan.href = `plan/${plan.pk}`;
            newplan.style.position = "absolute";
            newplan.style.width = `${(width * 100) / 1440}%`;
            newplan.style.left = `${(start * 100) / 1440}%`;
            // newplan.style.border = "1px solid orange";
            newplan.style.backgroundColor = "#FBFBFB";
            newplan.style.color = "#1A2634";
            newplan.style.height = "40px";
            newplan.style.borderRadius = "10px";
            newplan.style.boxShadow = "1px 1px 2px rgb(0 f0 0 / 14%)";

            newplan.style.padding = "11px";
            newplan.style.fontSize = "0.7rem";
            newplan.style.overflow = "hidden";
            newplan.style.whiteSpace = "nowrap";
            newplan.style.textOverflow = "ellipsis";
            newplan.innerText = `${plan.fields.title}`;
            document.querySelector(".private-timeline").appendChild(newplan);
          });

          publicPlansArray.forEach((plan) => {
            if (already.indexOf(`${plan.fields.meetings}`) == -1) {
              const newmember = document.createElement("div");
              newmember.innerHTML = `<img class="profileImagePreview"src="${
                meetingimg[plan.fields.meetings]
              }" width="32px" height="32px" border-radius="25px" />`;

              const new_user_name = document.createElement("p");
              new_user_name.classList.add("profile-user-name");
              new_user_name.textContent = `${
                public_user_names[plan.fields.meetings]
              }`;
              newmember.appendChild(new_user_name);

              newmember.style.height = "50px";
              newmember.style.width = "43px";
              memberlist.appendChild(newmember);
              let newDiv = document.createElement("div");
              newDiv.style.height = "50px";
              newDiv.classList.add(`meeting-${plan.fields.meetings}`);
              timeline.appendChild(newDiv);
              already.push(`${plan.fields.meetings}`);
            }
            const startDate = new Date(plan.fields.startTime);
            const endDate = new Date(plan.fields.endTime);

            let start = "";
            let hours = "";
            let minutes = "";

            [start, hours, minutes] = calcTime(startDate, endDate, today);

            let newplan = document.createElement("a");
            const width = parseInt(hours) * 60 + parseInt(minutes);
            newplan.href = `/pubplan/${plan.pk}`;
            newplan.style.position = "absolute";
            newplan.style.width = `${(width * 100) / 1440}%`;
            newplan.style.left = `${(start * 100) / 1440}%`;
            // newplan.style.border = "1px solid orange";
            if (attend_dict[plan.pk] == "standby") {
              newplan.style.border = "1px solid red";
            }
            newplan.style.backgroundColor = "#FBFBFB";
            newplan.style.color = "#1A2634";
            newplan.style.height = "40px";
            newplan.style.borderRadius = "10px";
            newplan.style.boxShadow = "1px 1px 2px rgb(0 0 0 / 14%)";
            newplan.style.padding = "11px";
            newplan.style.fontSize = "0.7rem";
            newplan.style.overflow = "hidden";
            newplan.style.whiteSpace = "nowrap";
            newplan.style.textOverflow = "ellipsis";
            newplan.innerText = `${plan.fields.title}`;
            document
              .querySelector(`.meeting-${plan.fields.meetings}`)
              .appendChild(newplan);
          });
        }
      }
    };
    prevClickDate.classList.remove("date-onclick");
    prevClickDate.classList.add("date");
    this.classList.remove("date");
    this.classList.add("date-onclick");
    prevClickDate = this;
  }

  // 이번달의 각 날짜에 onclick 이벤트 추가
  let dateTarget = document.querySelectorAll(".this");
  dateTarget.forEach((target) =>
    target.parentNode.addEventListener("click", viewDetail)
  );
  document.querySelector(".today").parentNode.click();
};
