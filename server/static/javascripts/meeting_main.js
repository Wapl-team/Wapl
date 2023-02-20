// 캘린더 만드는 함수 만들기

let date = new Date();
let currentYear = date.getFullYear();
let currentMonth = date.getMonth();

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
  
  document.getElementById("sidebar").style.visibility="visible";
  document.getElementById("sidebar").style.transition="all 0.1s";
  document.getElementById("sidebar").style.opacity="1";
}

function closeToggle() {
  // document.getElementById("sidebar").style.width = "0";
  // document.getElementById("sidebar").style.paddingTop = "0";
  // document.getElementById("sidebar").style.paddingBottom = "0";
  document.getElementById("sidebar").style.visibility = "hidden";
  document.getElementById("sidebar").style.transition = "all 0.1s";
  document.getElementById("sidebar").style.opacity = "0";
  document.getElementById("sidebar").style.paddingTop="1rem";
  document.getElementById("sidebar").style.paddingBottom="3rem";
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
const meetingPK = document.querySelector(".meeting-pk").innerHTML;
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

const modalButton = document.querySelector(".modalButton");
const modal = document.querySelector(".modal");
const modal_content = document.querySelector(".modal__content");
const closeModal = document.querySelector(".closeModal_x");
const closeModal2 = document.querySelector(".closeModal2");

modal.addEventListener("click", (e) => {
  if (e.target == modal) {
    modal.classList.add("hidden");
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
//새로운 팀 일정 추가하는 함수:
// ajax 사용해서 썸네일 띄우고
// 현재 보고있는 preview 날짜에 일정 추가시 ajax
const plan_create = (meeting_pk) => {
  const requestNewPlan = new XMLHttpRequest();
  const url = "/create-public-plan";
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
      meeting_pk: meeting_pk,
    })
  );
  requestNewPlan.onreadystatechange = () => {
    if (requestNewPlan.readyState === XMLHttpRequest.DONE) {
      if (requestNewPlan.status < 400) {
        const { plan, meeting_img, err_msg, meeting_name } = JSON.parse(
          requestNewPlan.response
        );
        //validation 통과한 경우
        if (plan != null && meeting_img != null) {
          const start_date = new Date(startTime);
          const end_date = new Date(endTime);

          const current_preview = new Date(
            currentYear,
            currentMonth - 1,
            document.querySelector(".date-onclick").childNodes[0].innerText
          );

          let this_date = new Date(
            start_date.getFullYear(),
            start_date.getMonth(),
            start_date.getDate()
          );

          //새로운 일정이 내가 현재보고있는 달력의 일정이라면 썸네일 추가
          while (true) {
            if (
              this_date.getFullYear() == viewYear &&
              this_date.getMonth() + 1 == viewMonth
            ) {
              const day = document.querySelector(`.day-${this_date.getDate()}`);
              if (
                !day.nextSibling ||
                !day.nextSibling.classList.contains("public")
              ) {
                const newimg = document.createElement("img");
                newimg.classList.add("public");
                newimg.classList.add("profileImagePlan");
                newimg.src = `${meeting_img}`;
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
              this_date.getFullYear() == end_date.getFullYear() &&
              this_date.getMonth() == end_date.getMonth() &&
              this_date.getDate() == end_date.getDate()
            ) {
              break;
            } else {
              this_date.setDate(this_date.getDate() + 1);
            }
          }
          // 새로운 일정이 내가 현재 보고 있는 날짜에 포함된다면 preview 추가
          const current_dateonly = new Date(current_preview).setHours(
            0,
            0,
            0,
            0
          );
          const start_dateonly = new Date(start_date).setHours(0, 0, 0, 0);
          const end_dateonly = new Date(end_date).setHours(0, 0, 0, 0);

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
                timeline.childNodes[0].classList.contains("public-timeline")
              ) {
                [start, hours, minutes] = calcTime(
                  start_date,
                  end_date,
                  current_preview.getDate()
                );
                let new_plan = document.createElement("a");
                const width = parseInt(hours) * 60 + parseInt(minutes);
                new_plan.href = `/pubplan/${plan.id}`;
                new_plan.style.position = "absolute";
                new_plan.style.width = `${(width * 100) / 1440}%`;
                new_plan.style.left = `${(start * 100) / 1440}%`;
                // new_plan.style.border = "1px solid orange";
                new_plan.style.backgroundColor = "#FBFBFB";
                new_plan.style.color = "black";
                new_plan.style.height = "50px";
                new_plan.style.padding = "8px";
                new_plan.style.color = "#1A2634";
                new_plan.style.height = "40px";
                new_plan.style.borderRadius = "10px";
                new_plan.style.boxShadow = "1px 1px 2px rgb(0 0 0 / 14%)";
                new_plan.style.padding = "11px";
                new_plan.style.fontSize = "0.7rem";
                new_plan.style.overflow = "hidden";
                new_plan.style.whiteSpace = "nowrap";
                new_plan.style.textOverflow = "ellipsis";
                new_plan.innerText = `${plan.title}`;
                timeline.childNodes[0].appendChild(new_plan);
              }
              // timeline에 팀일정만 있는경우
              else {
                // 개인 일정 라인추가
                const new_member = document.createElement("div");
                new_member.innerHTML = `<img class="profileImagePreview" src="${meeting_img}" border-radius="25px" width="32px" height="32px" />`;

                const new_user_name = document.createElement("p");
                new_user_name.classList.add("profile-user-name");
                new_user_name.textContent = `${meeting_name}`;
                new_member.appendChild(new_user_name);

                new_member.style.height = "50px";
                new_member.style.width = "43px";
                memberlist.firstChild.before(new_member);

                [start, hours, minutes] = calcTime(
                  start_date,
                  end_date,
                  current_preview.getDate()
                );

                // 추가한 일정 타임라인 추가
                let new_div = document.createElement("div");
                new_div.classList.add("private");
                new_div.style.height = "50px";
                let new_plan = document.createElement("a");
                const width = parseInt(hours) * 60 + parseInt(minutes);
                new_plan.href = `/pubplan/${plan.id}`;
                new_plan.style.position = "absolute";
                new_plan.style.width = `${(width * 100) / 1440}%`;
                new_plan.style.left = `${(start * 100) / 1440}%`;
                // new_plan.style.border = "1px solid orange";
                new_plan.style.backgroundColor = "#FBFBFB";
                new_plan.style.color = "black";
                new_plan.style.height = "50px";
                new_plan.style.borderRadius = "20px";
                new_plan.style.padding = "8px";
                new_plan.style.color = "#1A2634";
                new_plan.style.height = "40px";
                new_plan.style.borderRadius = "10px";
                new_plan.style.boxShadow = "1px 1px 2px rgb(0 0 0 / 14%)";
                new_plan.style.padding = "11px";
                new_plan.style.fontSize = "0.7rem";
                new_plan.style.overflow = "hidden";
                new_plan.style.whiteSpace = "nowrap";
                new_plan.style.textOverflow = "ellipsis";
                new_plan.innerText = `${plan.title}`;
                new_div.appendChild(new_plan);
                timeline.childNodes[0].before(new_div);
              }
            }
            // timeline에 아무일정도 없는 경우
            else {
              // 개인 일정 라인추가
              const new_member = document.createElement("div");
              new_member.innerHTML = `<img class="profileImagePreview" src="${meeting_img}" border-radius="25px" width="32px" height="32px" />`;

              const new_user_name = document.createElement("p");
              new_user_name.classList.add("profile-user-name");
              new_user_name.textContent = `${meeting_name}`;
              new_member.appendChild(new_user_name);

              new_member.style.height = "50px";
              new_member.style.width = "43px";
              memberlist.appendChild(new_member);

              [start, hours, minutes] = calcTime(
                start_date,
                end_date,
                current_preview.getDate()
              );

              let new_div = document.createElement("div");
              new_div.classList.add("public-timeline");
              new_div.style.height = "50px";
              let new_plan = document.createElement("a");
              const width = parseInt(hours) * 60 + parseInt(minutes);
              new_plan.href = `/pubplan/${plan.id}`;
              new_plan.style.position = "absolute";
              new_plan.style.width = `${(width * 100) / 1440}%`;
              new_plan.style.left = `${(start * 100) / 1440}%`;
              // new_plan.style.border = "1px solid orange";
              new_plan.style.backgroundColor = "#FBFBFB";
              new_plan.style.color = "black";
              new_plan.style.height = "50px";
              new_plan.style.borderRadius = "20px";
              new_plan.style.padding = "8px";
              new_plan.style.color = "#1A2634";
              new_plan.style.height = "40px";
              new_plan.style.borderRadius = "10px";
              new_plan.style.boxShadow = "1px 1px 2px rgb(0 0 0 / 14%)";
              new_plan.style.padding = "11px";
              new_plan.style.fontSize = "0.7rem";
              new_plan.style.overflow = "hidden";
              new_plan.style.whiteSpace = "nowrap";
              new_plan.style.textOverflow = "ellipsis";
              new_plan.innerText = `${plan.title}`;
              new_div.appendChild(new_plan);
              timeline.appendChild(new_div);
            }
          }
        } else {
          // validation 통과 못할 시 이쪽으로 옴
          alert(err_msg);
        }

        clearPlanForm();
      }
    }
  };
};

window.onload = function () {
  const requestPlan = new XMLHttpRequest();
  const url = "/view_team_plan/";
  requestPlan.open("POST", url, true);
  requestPlan.setRequestHeader(
    "Content-Type",
    "applcation/x-www-form-urlencoded"
  );

  //meeting: 현재 유저가 보고 있는 모임 이름(meeting_name)
  requestPlan.send(
    JSON.stringify({
      meetingPK: meetingPK,
    })
  );
  requestPlan.onreadystatechange = () => {
    if (requestPlan.readyState === XMLHttpRequest.DONE) {
      if (requestPlan.status < 400) {
        const { public_plans, private_plans, user_img, meeting_img } =
          JSON.parse(requestPlan.response);
        const public_plans_array = JSON.parse(public_plans);
        const private_plans_array = JSON.parse(private_plans);
        const month_dates = document.querySelectorAll(".this");

        month_dates.forEach((day) => {
          let count = 0;
          public_plans_array.forEach((plan) => {
            const start_time = new Date(plan.fields.startTime);
            const end_time = new Date(plan.fields.endTime);
            const today = new Date(
              currentYear,
              currentMonth - 1,
              day.innerText
            );
            if (
              start_time.setHours(0, 0, 0, 0) <= today &&
              today <= end_time.setHours(0, 0, 0, 0)
            ) {
              if (day.nextSibling == null) {
                const new_img = document.createElement("img");
                new_img.classList.add("public");
                new_img.classList.add("profileImagePlan");
                new_img.src = `${meeting_img}`;
                new_img.style.width = "12px";
                new_img.style.height = "12px";
                new_img.style.margin = "0px 1px";
                day.parentElement.appendChild(new_img);
                count += 1;
              }
            }
          });
          let already = [];
          private_plans_array.forEach((plan) => {
            const start_time = new Date(plan.fields.startTime);
            const end_time = new Date(plan.fields.endTime);
            const today = new Date(
              currentYear,
              currentMonth - 1,
              day.innerText
            );
            if (
              start_time.setHours(0, 0, 0, 0) <= today &&
              today <= end_time.setHours(0, 0, 0, 0)
            ) {
              if (already.indexOf(`${plan.fields.owner}`) == -1) {
                if (count <= 3) {
                  const new_img = document.createElement("img");
                  new_img.src = `${user_img[plan.fields.owner]}`;
                  new_img.classList.add("profileImagePlan");
                  new_img.style.width = "12px";
                  new_img.style.height = "12px";
                  new_img.style.margin = "0px 1px";
                  day.parentElement.appendChild(new_img);
                  already.push(`${plan.fields.owner}`);
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

  // onclick시 달력 아래에 타임라인 출력
  const requestExplan = new XMLHttpRequest();
  function viewDetail() {
    const day = this.childNodes[0].innerText;
    const url = "/view_team_explan/";
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
        meetingPK: meetingPK,
      })
    );
    requestExplan.onreadystatechange = () => {
      if (requestExplan.readyState === XMLHttpRequest.DONE) {
        if (requestExplan.status < 400) {
          const {
            public_plans,
            private_plans,
            share_list,
            meeting_name,
            user_name,
            user_img,
            meeting_img,
            login_user_id,
          } = JSON.parse(requestExplan.response);

          const public_plans_array = JSON.parse(public_plans);
          const prviate_plans_array = JSON.parse(private_plans);
          const share_list_array = JSON.parse(share_list);
          memberlist.innerHTML = "";
          timeline.innerHTML = ``;

          let already = [];

          public_plans_array.forEach((plan) => {
            if (already.indexOf("public") == -1) {
              let new_div = document.createElement("div");
              new_div.classList.add("public-timeline");
              new_div.style.height = "50px";
              timeline.appendChild(new_div);
              const new_member = document.createElement("div");
              new_member.innerHTML = `<img class="profileImagePreview"src="${meeting_img}" border-radius="25px" width="32px" height="32px" />`;

              const new_meeting_name = document.createElement("p");
              new_meeting_name.classList.add("profile-user-name");
              new_meeting_name.textContent = `${meeting_name}`;
              new_member.appendChild(new_meeting_name);

              new_member.style.height = "50px";
              new_member.style.width = "43px";
              memberlist.appendChild(new_member);
              already.push("public");
            }
            const start_date = new Date(plan.fields.startTime);
            const end_date = new Date(plan.fields.endTime);

            let start = "";
            let hours = "";
            let minutes = "";

            [start, hours, minutes] = calcTime(start_date, end_date, day);

            let new_plan = document.createElement("a");
            const width = parseInt(hours) * 60 + parseInt(minutes);
            new_plan.href = `/pubplan/${plan.pk}`;
            new_plan.style.position = "absolute";
            new_plan.style.width = `${(width * 100) / 1440}%`;
            new_plan.style.left = `${(start * 100) / 1440}%`;
            // new_plan.style.border = "1px solid orange";
            new_plan.style.backgroundColor = "#FBFBFB";
            new_plan.style.color = "#1A2634";
            new_plan.style.height = "40px";
            new_plan.style.borderRadius = "10px";
            new_plan.style.boxShadow = "1px 1px 2px rgb(0 0 0 / 14%)";
            new_plan.style.padding = "11px";
            new_plan.style.fontSize = "0.7rem";
            new_plan.style.overflow = "hidden";
            new_plan.style.whiteSpace = "nowrap";
            new_plan.style.textOverflow = "ellipsis";
            new_plan.innerText = `${plan.fields.title}`;
            document.querySelector(".public-timeline").appendChild(new_plan);
          });

          prviate_plans_array.forEach((plan, i) => {
            if (already.indexOf(`${plan.fields.owner}`) == -1) {
              const new_member = document.createElement("div");
              new_member.innerHTML = `<img class="profileImagePreview"src="${
                user_img[plan.fields.owner]
              }" border-radius="25px" width="32px" height="32px" />`;

              const new_user_name = document.createElement("p");
              new_user_name.classList.add("profile-user-name");
              new_user_name.textContent = `${user_name[plan.fields.owner]}`;
              new_member.appendChild(new_user_name);

              new_member.style.height = "50px";
              new_member.style.width = "43px";
              memberlist.appendChild(new_member);
              let new_div = document.createElement("div");
              new_div.style.height = "50px";
              new_div.classList.add(`user-${plan.fields.owner}`);
              timeline.appendChild(new_div);
              already.push(`${plan.fields.owner}`);
            }
            const start_date = new Date(plan.fields.startTime);
            const end_date = new Date(plan.fields.endTime);

            let start = "";
            let hours = "";
            let minutes = "";

            [start, hours, minutes] = calcTime(start_date, end_date, day);

            let new_plan = document.createElement("a");
            const width = parseInt(hours) * 60 + parseInt(minutes);

            new_plan.style.position = "absolute";
            new_plan.style.width = `${(width * 100) / 1440}%`;
            new_plan.style.left = `${(start * 100) / 1440}%`;
            // new_plan.style.border = "1px solid orange";
            new_plan.style.backgroundColor = "#FBFBFB";
            new_plan.style.color = "#1A2634";
            new_plan.style.height = "40px";
            new_plan.style.borderRadius = "10px";
            new_plan.style.boxShadow = "1px 1px 2px rgb(0 0 0 / 14%)";
            new_plan.style.padding = "11px";
            new_plan.style.fontSize = "0.7rem";
            new_plan.innerText = `${plan.fields.title}`;
            new_plan.style.overflow = "hidden";
            new_plan.style.whiteSpace = "nowrap";
            new_plan.style.textOverflow = "ellipsis";
            if (share_list_array[i].fields.is_share == "open") {
              new_plan.innerText = `${plan.fields.title}`;
              new_plan.href = `/plan/${plan.pk}`;
            } else if (share_list_array[i].fields.is_share == "untitled") {
              if (login_user_id == plan.fields.owner) {
                new_plan.innerText = `${plan.fields.title}`;
                new_plan.href = `/plan/${plan.pk}`;
              }else{
                new_plan.innerText = `${user_name[plan.fields.owner]}의 일정`;
                new_plan.style.touchAction = "none";
              }        
            } else {
              new_plan.innerText = `${user_name[plan.fields.owner]}의 일정`;
              new_plan.style.touchAction = "none";
            }

            document
              .querySelector(`.user-${plan.fields.owner}`)
              .appendChild(new_plan);
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
  let date_target = document.querySelectorAll(".this");
  date_target.forEach((target) =>
    target.parentNode.addEventListener("click", viewDetail)
  );
  document.querySelector(".today").parentNode.click();
};
